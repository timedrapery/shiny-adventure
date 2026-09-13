from __future__ import annotations

import base64
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from feedback_service import auth, export
from feedback_service.__main__ import main as cli_main
from feedback_service.app import FeedbackApp
from feedback_service.config import Settings
from feedback_service.storage import Storage
from feedback_service.validation import ValidationError, validate_submission


BODY_HASH = "0199c3d1f32f78ce1cf5ca14669a237ca25c5088053fb3b8d67c7eeda9f64085"
QUESTION_HASH = "a" * 64
PASSWORD = "correct horse battery staple"
USER = "editor"
SITE_ORIGIN = "https://timedrapery.github.io"


def settings(**overrides) -> Settings:
    values = dict(
        db_path=Path(":memory:"),
        site_dir=None,
        allowed_origins=(SITE_ORIGIN,),
        trust_proxy=False,
        max_body_bytes=8192,
        rate_limit_per_hour=50,
        contact_enabled=False,
        maintainer_user=USER,
        maintainer_password_hash=auth.hash_password(PASSWORD, iterations=1000),
        secret_key="test-secret",
        secret_is_ephemeral=False,
        retention_days=None,
    )
    values.update(overrides)
    return Settings(**values)


def make_app(**overrides) -> FeedbackApp:
    return FeedbackApp(settings(**overrides), Storage(":memory:"))


def call(app, method, path, body=None, headers=None, content_type="application/json", remote="10.0.0.1"):
    raw = b""
    if body is not None:
        raw = body if isinstance(body, bytes) else json.dumps(body).encode("utf-8")
    environ = {
        "REQUEST_METHOD": method,
        "PATH_INFO": path.split("?", 1)[0],
        "QUERY_STRING": path.split("?", 1)[1] if "?" in path else "",
        "SERVER_NAME": "127.0.0.1",
        "SERVER_PORT": "8765",
        "HTTP_HOST": "127.0.0.1:8765",
        "wsgi.url_scheme": "http",
        "wsgi.input": io.BytesIO(raw),
        "CONTENT_LENGTH": str(len(raw)),
        "REMOTE_ADDR": remote,
    }
    if body is not None:
        environ["CONTENT_TYPE"] = content_type
    for key, value in (headers or {}).items():
        environ["HTTP_" + key.upper().replace("-", "_")] = value
    captured = {}

    def start_response(status, response_headers):
        captured["status"] = status
        captured["headers"] = dict(response_headers)

    chunks = app(environ, start_response)
    data = b"".join(chunks)
    return captured["status"], captured["headers"], data


def basic(user=USER, password=PASSWORD) -> dict[str, str]:
    token = base64.b64encode(f"{user}:{password}".encode("utf-8")).decode("ascii")
    return {"Authorization": f"Basic {token}"}


def translation_payload(**overrides) -> dict:
    payload = {
        "client_submission_id": "11111111-1111-4111-8111-111111111111",
        "manifest_format": 1,
        "target": "translation",
        "surface_key": "sn36_6",
        "surface_label": "SN 36.6",
        "page_path": "suttas/sn36-6-salla-sutta/",
        "body_sha256": BODY_HASH,
        "introduction_version": "abcdef123456",
        "passage_id": "p009",
        "passage_fingerprint": "0123456789abcdef",
        "passage_section": "Two Arrows",
        "passage_text": "They feel it twice: once in the body and once in the mind.",
        "terms": [{"id": "sn36-6-two-feelings-painful-feeling", "basis": "explicit"}],
        "mapping": "mapped",
        "glossary_versions": {"felt experience": "abcdefabcdef"},
        "category": "sentence",
        "comment": "Twice? I thought there was only one arrow so far.",
        "website": "",
        "session": None,
    }
    payload.update(overrides)
    return payload


def comprehension_payload(client_id: str, session=None, **overrides) -> dict:
    payload = {
        "client_submission_id": client_id,
        "manifest_format": 1,
        "target": "comprehension",
        "surface_key": "sn36_6",
        "surface_label": "SN 36.6",
        "page_path": "suttas/sn36-6-salla-sutta/",
        "body_sha256": BODY_HASH,
        "introduction_version": "abcdef123456",
        "question_version": 1,
        "question_set_sha256": QUESTION_HASH,
        "question_editorial_status": "draft",
        "answers": {
            "paraphrase": "Two people feel pain; one makes it worse by getting upset.",
            "specific": "The first arrow is the pain, the second is being upset about it.",
            "reread": "underlying tendency",
        },
        "familiarity": "new",
        "website": "",
        "session": session,
    }
    payload.update(overrides)
    return payload


class PublicApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = make_app()

    def test_health(self) -> None:
        status, headers, body = call(self.app, "GET", "/api/health")
        self.assertEqual(status, "200 OK")
        self.assertEqual(json.loads(body)["ok"], True)
        self.assertEqual(headers["Cache-Control"], "no-store")

    def test_passage_feedback_is_stored_with_its_version_evidence(self) -> None:
        status, _, body = call(self.app, "POST", "/api/submissions", translation_payload())
        self.assertEqual(status, "201 Created", body)
        public_id = json.loads(body)["id"]
        row = self.app.storage.submission(public_id)
        self.assertEqual(row["surface_key"], "sn36_6")
        self.assertEqual(row["passage_id"], "p009")
        self.assertEqual(row["body_sha256"], BODY_HASH)
        self.assertEqual(row["passage_text"], "They feel it twice: once in the body and once in the mind.")
        self.assertEqual(row["introduction_version"], "abcdef123456")
        self.assertEqual(row["category"], "sentence")
        self.assertEqual(row["channel"], "public")
        self.assertEqual(row["status"], "received")
        self.assertTrue(row["received_at"].endswith("Z"))
        terms = self.app.storage.terms_for(row["id"])
        self.assertEqual([(t["term_id"], t["basis"]) for t in terms],
                         [("sn36-6-two-feelings-painful-feeling", "explicit")])
        self.assertEqual(json.loads(row["glossary_versions_json"]), {"felt experience": "abcdefabcdef"})

    def test_retry_with_the_same_client_id_does_not_duplicate(self) -> None:
        first = call(self.app, "POST", "/api/submissions", translation_payload())
        second = call(self.app, "POST", "/api/submissions", translation_payload(comment="changed on retry"))
        self.assertEqual(first[0], "201 Created")
        self.assertEqual(second[0], "200 OK")
        self.assertEqual(json.loads(first[2])["id"], json.loads(second[2])["id"])
        self.assertTrue(json.loads(second[2])["duplicate"])
        self.assertEqual(self.app.storage.counts()["submissions"], 1)

    def test_glossary_feedback_records_the_explanation_version(self) -> None:
        payload = {
            "client_submission_id": "22222222-2222-4222-8222-222222222222",
            "manifest_format": 1, "target": "glossary", "surface_key": "sn36_6",
            "surface_label": "SN 36.6", "page_path": "suttas/sn36-6-salla-sutta/",
            "body_sha256": BODY_HASH, "introduction_version": "abcdef123456",
            "glossary_term": "underlying tendency", "glossary_version": "0011223344ff",
            "terms": [{"id": "anusaya", "basis": "glossary"}], "mapping": "mapped",
            "passage_text": "A reactive pattern...", "rating": "partly",
            "comment": "Lying underneath what?", "website": "",
        }
        status, _, body = call(self.app, "POST", "/api/submissions", payload)
        self.assertEqual(status, "201 Created", body)
        row = self.app.storage.submission(json.loads(body)["id"])
        self.assertEqual(row["glossary_term"], "underlying tendency")
        self.assertEqual(row["glossary_version"], "0011223344ff")
        self.assertEqual(row["rating"], "partly")
        self.assertEqual([t["term_id"] for t in self.app.storage.terms_for(row["id"])], ["anusaya"])

    def test_invalid_submission_is_rejected_with_a_field_name(self) -> None:
        status, _, body = call(self.app, "POST", "/api/submissions", translation_payload(category="rude"))
        self.assertEqual(status, "422 Unprocessable Content")
        self.assertIn("category", json.loads(body)["error"])
        status, _, _ = call(self.app, "POST", "/api/submissions", translation_payload(body_sha256="nope"))
        self.assertEqual(status, "422 Unprocessable Content")
        self.assertEqual(self.app.storage.counts()["submissions"], 0)

    def test_payload_limits(self) -> None:
        big = translation_payload(comment="x" * 9000)
        status, _, _ = call(self.app, "POST", "/api/submissions", big)
        self.assertEqual(status, "413 Payload Too Large")
        status, _, _ = call(self.app, "POST", "/api/submissions", translation_payload(comment="x" * 2001))
        self.assertEqual(status, "422 Unprocessable Content")
        status, _, _ = call(self.app, "POST", "/api/submissions", b"not json")
        self.assertEqual(status, "400 Bad Request")
        status, _, _ = call(self.app, "POST", "/api/submissions", b"a=b", content_type="application/x-www-form-urlencoded")
        self.assertEqual(status, "415 Unsupported Media Type")

    def test_honeypot_is_accepted_but_not_stored(self) -> None:
        status, _, body = call(self.app, "POST", "/api/submissions", translation_payload(website="http://spam"))
        self.assertEqual(status, "200 OK")
        self.assertTrue(json.loads(body)["ok"])
        self.assertEqual(self.app.storage.counts()["submissions"], 0)

    def test_rate_limit_per_client(self) -> None:
        app = make_app(rate_limit_per_hour=2)
        for index in range(2):
            status, _, _ = call(app, "POST", "/api/submissions",
                                translation_payload(client_submission_id=f"rate-{index}-000000"))
            self.assertEqual(status, "201 Created")
        status, headers, _ = call(app, "POST", "/api/submissions", translation_payload(client_submission_id="rate-3-000000"))
        self.assertEqual(status, "429 Too Many Requests")
        self.assertIn("Retry-After", headers)
        # A different client is unaffected.
        status, _, _ = call(app, "POST", "/api/submissions",
                            translation_payload(client_submission_id="rate-4-000000"), remote="10.0.0.2")
        self.assertEqual(status, "201 Created")
        # Retrying an already stored submission is never rate limited.
        status, _, _ = call(app, "POST", "/api/submissions", translation_payload(client_submission_id="rate-0-000000"))
        self.assertEqual(status, "200 OK")

    def test_cors_allows_only_the_configured_site(self) -> None:
        status, headers, _ = call(self.app, "OPTIONS", "/api/submissions", headers={"Origin": SITE_ORIGIN})
        self.assertEqual(status, "204 No Content")
        self.assertEqual(headers["Access-Control-Allow-Origin"], SITE_ORIGIN)
        status, headers, _ = call(self.app, "POST", "/api/submissions", translation_payload(), headers={"Origin": SITE_ORIGIN})
        self.assertEqual(status, "201 Created")
        self.assertEqual(headers["Access-Control-Allow-Origin"], SITE_ORIGIN)
        status, _, _ = call(self.app, "POST", "/api/submissions",
                            translation_payload(client_submission_id="other-origin-0001"),
                            headers={"Origin": "https://evil.example"})
        self.assertEqual(status, "403 Forbidden")
        status, headers, _ = call(self.app, "GET", "/api/health", headers={"Origin": "http://127.0.0.1:8765"})
        self.assertEqual(status, "200 OK")
        self.assertNotIn("Access-Control-Allow-Origin", headers)

    def test_contact_is_refused_unless_enabled_and_consented(self) -> None:
        payload = translation_payload(contact={"email": "reader@example.org", "consent": True})
        status, _, _ = call(self.app, "POST", "/api/submissions", payload)
        self.assertEqual(status, "422 Unprocessable Content")
        app = make_app(contact_enabled=True)
        status, _, _ = call(app, "POST", "/api/submissions",
                            translation_payload(contact={"email": "reader@example.org", "consent": False}))
        self.assertEqual(status, "422 Unprocessable Content")
        status, _, body = call(app, "POST", "/api/submissions", payload)
        self.assertEqual(status, "201 Created")
        self.assertEqual(app.storage.counts()["contacts"], 1)
        public_id = json.loads(body)["id"]
        document = export.submission_document(app.storage, app.storage.submission(public_id))
        self.assertNotIn("reader@example.org", json.dumps(document))
        queue = export.queue_export(app.storage, {})
        self.assertNotIn("reader@example.org", json.dumps(queue))
        self.assertTrue(app.storage.delete_contact(public_id))
        self.assertEqual(app.storage.counts()["contacts"], 0)
        self.assertEqual(app.storage.counts()["submissions"], 1)

    def test_unknown_session_code_is_refused(self) -> None:
        payload = translation_payload(session={"code": "nosuch01", "participant": "R1"})
        status, _, body = call(self.app, "POST", "/api/submissions", payload)
        self.assertEqual(status, "422 Unprocessable Content")
        self.assertIn("session", json.loads(body)["error"])


class ValidationTests(unittest.TestCase):
    def test_control_characters_are_stripped_and_markup_kept_verbatim(self) -> None:
        result = validate_submission(translation_payload(comment="<b>bold</b>\x00\x07 and\r\nnew"))
        self.assertEqual(result["record"]["comment"], "<b>bold</b> and\nnew")

    def test_manifest_format_is_required(self) -> None:
        with self.assertRaises(ValidationError):
            validate_submission(translation_payload(manifest_format=2))

    def test_comprehension_requires_an_answer(self) -> None:
        with self.assertRaises(ValidationError):
            validate_submission(comprehension_payload("c-1", answers={"paraphrase": "  "}))
        with self.assertRaises(ValidationError):
            validate_submission(comprehension_payload("c-1", question_version=0))


class AdminTests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = make_app()
        status, _, body = call(self.app, "POST", "/api/submissions",
                               translation_payload(comment='<script>alert("x")</script> & "quotes"'))
        self.assertEqual(status, "201 Created")
        self.public_id = json.loads(body)["id"]

    def test_queue_and_export_require_authentication(self) -> None:
        for path in ("/admin/", "/admin/export.json", f"/admin/submissions/{self.public_id}", "/admin/terms", "/admin/sessions"):
            status, headers, body = call(self.app, "GET", path)
            self.assertEqual(status, "401 Unauthorized", path)
            self.assertIn("WWW-Authenticate", headers)
            self.assertNotIn(b"alert", body)
            status, _, body = call(self.app, "GET", path, headers=basic(password="wrong password!"))
            self.assertEqual(status, "401 Unauthorized", path)
            self.assertNotIn(b"alert", body)

    def test_admin_is_disabled_without_configured_credentials(self) -> None:
        app = make_app(maintainer_user=None, maintainer_password_hash=None)
        status, _, _ = call(app, "GET", "/admin/", headers=basic())
        self.assertEqual(status, "503 Service Unavailable")

    def test_submitted_markup_is_escaped_and_scripts_are_forbidden(self) -> None:
        status, headers, body = call(self.app, "GET", f"/admin/submissions/{self.public_id}", headers=basic())
        self.assertEqual(status, "200 OK")
        text = body.decode("utf-8")
        self.assertNotIn("<script>alert", text)
        self.assertIn("&lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt;", text)
        self.assertNotIn("<script", text)
        self.assertIn("default-src 'none'", headers["Content-Security-Policy"])
        status, _, body = call(self.app, "GET", "/admin/", headers=basic())
        self.assertNotIn("<script>alert", body.decode("utf-8"))

    def test_queue_filters(self) -> None:
        call(self.app, "POST", "/api/submissions", translation_payload(
            client_submission_id="second-0000001", surface_key="an2_9", passage_id="p002", category="word",
            body_sha256="b" * 64, terms=[{"id": "hiri", "basis": "explicit"}]))
        headers = basic()
        for query, expected in (
            ("surface=an2_9", 1), ("surface=sn36_6", 1), ("passage=p009", 1), ("term=hiri", 1),
            ("term=sn36-6-two-feelings-painful-feeling", 1), ("category=word", 1), ("status=received", 2),
            ("status=examined", 0), ("version=0199c3d1", 1), ("channel=formal", 0), ("target=translation", 2),
        ):
            status, _, body = call(self.app, "GET", f"/admin/export.json?{query}", headers=headers)
            self.assertEqual(status, "200 OK")
            self.assertEqual(json.loads(body)["count"], expected, query)
        status, _, body = call(self.app, "GET", "/admin/?term=hiri", headers=headers)
        self.assertIn(b"an2_9", body)
        self.assertNotIn(b"p009", body)
        status, _, body = call(self.app, "GET", "/admin/terms", headers=headers)
        self.assertIn(b"hiri", body)

    def test_disposition_requires_a_form_token_and_records_history(self) -> None:
        path = f"/admin/submissions/{self.public_id}/disposition"
        form = "status=examined&problem=Reader+lost+the+arrow+image"
        status, _, _ = call(self.app, "POST", path, form.encode(), headers=basic(),
                            content_type="application/x-www-form-urlencoded")
        self.assertEqual(status, "403 Forbidden")
        token = auth.csrf_token("test-secret", USER)
        form = (
            f"csrf={token}&status=proposed&problem=Reader+lost+the+arrow+image&fix_layer=translation"
            "&rationale=Second+arrow+needs+its+antecedent&change_reference=notes%2Fsn36-6&confirmed_terms=salla"
        )
        status, headers, _ = call(self.app, "POST", path, form.encode(), headers=basic(),
                                  content_type="application/x-www-form-urlencoded")
        self.assertEqual(status, "303 See Other")
        row = self.app.storage.submission(self.public_id)
        self.assertEqual(row["status"], "proposed")
        history = self.app.storage.dispositions(row["id"])
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["fix_layer"], "translation")
        self.assertEqual(history[0]["recorded_by"], USER)
        self.assertEqual(history[0]["confirmed_terms"], "salla")
        status, _, _ = call(self.app, "POST", path, f"csrf={token}&status=validated".encode(), headers=basic(),
                            content_type="application/x-www-form-urlencoded")
        self.assertEqual(status, "400 Bad Request")
        status, _, _ = call(self.app, "POST", path, f"csrf={token}&status=examined".encode(),
                            headers=dict(basic(), Origin="https://evil.example"),
                            content_type="application/x-www-form-urlencoded")
        self.assertEqual(status, "403 Forbidden")


class FormalSessionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = make_app()
        storage = self.app.storage
        self.session = storage.create_session("sn36_6", "Pilot 1", code="pilot001")
        storage.add_participant(self.session["id"], "R1", "fresh", independent=True)
        storage.add_participant(self.session["id"], "R2", "fresh")

    def submit(self, client_id, participant="R1", **overrides):
        payload = comprehension_payload(client_id, session={"code": "pilot001", "participant": participant}, **overrides)
        return call(self.app, "POST", "/api/submissions", payload)

    def test_formal_responses_are_tagged_and_counted_once_per_version(self) -> None:
        status, _, body = self.submit("formal-000001")
        self.assertEqual(status, "201 Created", body)
        first = self.app.storage.submission(json.loads(body)["id"])
        self.assertEqual(first["channel"], "formal")
        self.assertEqual(first["counts_for_session"], 1)
        status, _, body = self.submit("formal-000002")
        second = self.app.storage.submission(json.loads(body)["id"])
        self.assertEqual(second["counts_for_session"], 0)
        status, _, body = self.submit("formal-000003", body_sha256="b" * 64)
        revised = self.app.storage.submission(json.loads(body)["id"])
        self.assertEqual(revised["counts_for_session"], 1)

    def test_session_must_match_text_and_be_open(self) -> None:
        status, _, body = self.submit("formal-000004", surface_key="an2_9")
        self.assertEqual(status, "422 Unprocessable Content")
        status, _, body = self.submit("formal-000005", participant="R9")
        self.assertEqual(status, "422 Unprocessable Content")
        self.app.storage.close_session("pilot001")
        status, _, body = self.submit("formal-000006")
        self.assertEqual(status, "422 Unprocessable Content")

    def test_public_comprehension_never_counts(self) -> None:
        status, _, body = call(self.app, "POST", "/api/submissions", comprehension_payload("public-000001"))
        row = self.app.storage.submission(json.loads(body)["id"])
        self.assertEqual(row["channel"], "public")
        self.assertEqual(row["counts_for_session"], 0)
        data = export.session_export(self.app.storage, "pilot001")
        self.assertEqual(data["records"], [])

    def test_reviewed_export_contains_only_assessed_counted_independent_records(self) -> None:
        storage = self.app.storage
        _, _, body = self.submit("formal-000010")
        r1 = storage.submission(json.loads(body)["id"])
        _, _, body = self.submit("formal-000011", participant="R2")
        r2 = storage.submission(json.loads(body)["id"])
        _, _, body = self.submit("formal-000012")  # R1 again, same version: not counted
        data = export.session_export(storage, "pilot001")
        self.assertEqual(data["records"], [])
        self.assertEqual({e["reason"] for e in data["excluded"]},
                         {"not yet assessed by a maintainer",
                          "a counted response for this participant and body version already exists"})
        storage.record_assessment(r1["id"], "pass", "Both arrows identified.")
        storage.record_assessment(r2["id"], "fail", "Took the second arrow literally.")
        data = export.session_export(storage, "pilot001")
        self.assertEqual([r["participant"] for r in data["records"]], ["R1"])
        self.assertTrue(any("independent" in e["reason"] for e in data["excluded"]))
        storage.set_participant_independent(storage.participant(self.session["id"], "R2")["id"], True)
        data = export.session_export(storage, "pilot001")
        self.assertEqual([(r["participant"], r["pass"]) for r in data["records"]], [("R1", True), ("R2", False)])
        record = data["records"][0]
        self.assertEqual(record["what_happened"], "Two people feel pain; one makes it worse by getting upset.")
        self.assertEqual(record["practical_point"], "The first arrow is the pain, the second is being upset about it.")
        self.assertEqual(record["confusing_words"], ["underlying tendency"])
        self.assertEqual(record["body_sha256"], BODY_HASH)
        self.assertEqual(record["question_version"], 1)
        self.assertEqual(record["question_editorial_status"], "draft")
        self.assertEqual(record["participant_kind"], "fresh")
        self.assertTrue(record["independent"])
        self.assertNotIn("answers", record)

    def test_returning_participants_are_distinguished(self) -> None:
        storage = self.app.storage
        later = storage.create_session("sn36_6", "Pilot 2", code="pilot002")
        earlier = storage.participant(self.session["id"], "R1")
        storage.add_participant(later["id"], "R1", "returning", returning_from=earlier["id"], independent=True)
        storage.add_participant(later["id"], "R3", "fresh", independent=True)
        payload = comprehension_payload("formal-000020", session={"code": "pilot002", "participant": "R1"},
                                        body_sha256="c" * 64)
        _, _, body = call(self.app, "POST", "/api/submissions", payload)
        storage.record_assessment(storage.submission(json.loads(body)["id"])["id"], "pass")
        data = export.session_export(storage, "pilot002")
        self.assertEqual(data["records"][0]["participant_kind"], "returning")
        self.assertEqual(data["records"][0]["returning_from"], {"session": "pilot001", "participant": "R1"})
        self.assertEqual([p["kind"] for p in data["participants"]], ["returning", "fresh"])
        # A returning reader is a follow-up and is never independent, whatever
        # the facilitator tried to record.
        self.assertTrue(data["records"][0]["follow_up"])
        self.assertFalse(data["records"][0]["independent"])
        returning = storage.participant(later["id"], "R1")
        self.assertEqual(returning["independent"], 0)
        storage.set_participant_independent(returning["id"], True)
        self.assertEqual(storage.participant(later["id"], "R1")["independent"], 0)


class OperationsTests(unittest.TestCase):
    def test_migrations_apply_once_and_backup_purge_delete_work(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "feedback.sqlite"
            storage = Storage(db)
            self.assertEqual(storage.migrate(), [])
            app = FeedbackApp(settings(db_path=db), storage)
            status, _, body = call(app, "POST", "/api/submissions", translation_payload())
            self.assertEqual(status, "201 Created")
            public_id = json.loads(body)["id"]
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(cli_main(["--db", str(db), "backup", "--out", str(Path(tmp) / "backups")]), 0)
            backups = list((Path(tmp) / "backups").glob("feedback-*.sqlite"))
            self.assertEqual(len(backups), 1)
            self.assertEqual(Storage(backups[0]).counts()["submissions"], 1)
            self.assertEqual(storage.purge_older_than(1, dry_run=True), 0)
            storage.connection.execute(
                "UPDATE submissions SET received_at = '2020-01-01T00:00:00Z' WHERE public_id = ?", (public_id,)
            )
            self.assertEqual(storage.purge_older_than(365, dry_run=True), 1)
            self.assertEqual(storage.purge_older_than(365), 1)
            self.assertIsNone(storage.submission(public_id))
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(cli_main(["--db", str(db), "delete", "--id", public_id]), 1)
                self.assertEqual(cli_main(["--db", str(db), "stats"]), 0)

    def test_cli_sessions_and_session_export(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db = str(Path(tmp) / "feedback.sqlite")
            out = Path(tmp) / "session.json"
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(cli_main(["--db", db, "create-session", "--surface", "sn36_6", "--code", "cli00001"]), 0)
                self.assertEqual(cli_main(["--db", db, "add-participant", "--session", "cli00001", "--label", "R1", "--independent", "yes"]), 0)
                self.assertEqual(cli_main(["--db", db, "export-session", "--code", "cli00001", "--out", str(out)]), 0)
                data = json.loads(out.read_text(encoding="utf-8"))
                self.assertEqual(cli_main(["--db", db, "export-session", "--code", "missing", "--out", str(out)]), 1)
            self.assertEqual(data["export_kind"], "formal-session-review")
            self.assertEqual(data["session"]["surface_key"], "sn36_6")

    def test_password_hashing_round_trip(self) -> None:
        encoded = auth.hash_password("a long enough password", iterations=1000)
        self.assertTrue(auth.verify_password("a long enough password", encoded))
        self.assertFalse(auth.verify_password("a long enough passwor", encoded))
        self.assertFalse(auth.verify_password("x", "garbage"))


class StaticSiteTests(unittest.TestCase):
    def test_static_files_are_served_without_path_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp) / "site"
            (site / "suttas" / "x").mkdir(parents=True)
            (site / "suttas" / "x" / "index.html").write_text("<p>page</p>", encoding="utf-8")
            (Path(tmp) / "secret.txt").write_text("no", encoding="utf-8")
            app = FeedbackApp(settings(site_dir=site), Storage(":memory:"))
            status, headers, body = call(app, "GET", "/suttas/x/")
            self.assertEqual(status, "200 OK")
            self.assertEqual(body, b"<p>page</p>")
            self.assertTrue(headers["Content-Type"].startswith("text/html"))
            status, _, _ = call(app, "GET", "/suttas/x")
            self.assertEqual(status, "303 See Other")
            status, _, _ = call(app, "GET", "/../secret.txt")
            self.assertEqual(status, "404 Not Found")
            status, _, _ = call(app, "GET", "/suttas/../../secret.txt")
            self.assertEqual(status, "404 Not Found")


if __name__ == "__main__":
    unittest.main()
