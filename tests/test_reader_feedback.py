from __future__ import annotations

import copy
import json
import unittest

from tests.helpers import load_module


paragraph_ids = load_module("paragraph_ids", "scripts/paragraph_ids.py")
reader_feedback = load_module("reader_feedback", "scripts/reader_feedback.py")
registry = load_module("surface_registry", "scripts/surface_registry.py")


def surface(key: str):
    return next(s for s in registry.TRANSLATION_SURFACES if s.key == key)


class ConfigTests(unittest.TestCase):
    def test_committed_config_is_valid(self) -> None:
        config = reader_feedback.load_config()
        self.assertEqual(reader_feedback.config_problems(config), [])

    def test_endpoint_must_be_an_origin(self) -> None:
        config = reader_feedback.load_config()
        config["transport"] = None
        config["endpoint"] = "feedback.example.org"
        self.assertTrue(any("endpoint" in p for p in reader_feedback.config_problems(config)))
        config["endpoint"] = "https://feedback.example.org/"
        self.assertTrue(any("slash" in p for p in reader_feedback.config_problems(config)))
        config["endpoint"] = "https://feedback.example.org"
        self.assertEqual(reader_feedback.config_problems(config), [])

    def test_transport_is_validated(self) -> None:
        config = reader_feedback.load_config()
        config["endpoint"] = None
        config["transport"] = {"kind": "google-form", "form_action": "https://evil.example/formResponse",
                               "payload_field": "entry.1"}
        problems = reader_feedback.config_problems(config)
        self.assertTrue(any("form_action" in p for p in problems))
        self.assertTrue(any("payload_field" in p for p in problems))
        config["transport"] = {
            "kind": "google-form",
            "form_action": "https://docs.google.com/forms/d/e/1FAIpQLSf7i3UIU3R7GcY9ihUz0C40cv_M0KwieYH2hZ6GGwKaXKaFJQ/formResponse",
            "payload_field": "entry.1359254143",
        }
        self.assertEqual(reader_feedback.config_problems(config), [])
        config["endpoint"] = "https://feedback.example.org"
        self.assertTrue(any("not both" in p for p in reader_feedback.config_problems(config)))

    def test_public_site_uses_the_google_form_transport(self) -> None:
        config = reader_feedback.load_config()
        self.assertIsNone(config["endpoint"])
        self.assertEqual(config["transport"]["kind"], "google-form")

    def test_unregistered_enabled_surface_is_rejected(self) -> None:
        config = reader_feedback.load_config()
        config["enabled_surfaces"] = ["nope"]
        self.assertTrue(any("not registered" in p for p in reader_feedback.config_problems(config)))


class TermMapTests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = reader_feedback.load_term_map("sn36_6")
        self.passage_ids = {
            e["id"] for e in paragraph_ids.load_map(paragraph_ids.map_path("sn36_6"))["passages"]
        }
        self.term_ids = reader_feedback.known_term_ids()

    def test_pilot_term_map_is_valid(self) -> None:
        self.assertEqual(
            reader_feedback.term_map_problems("sn36_6", self.data, self.passage_ids, self.term_ids),
            [],
        )

    def test_unknown_term_and_passage_are_rejected(self) -> None:
        data = copy.deepcopy(self.data)
        data["mappings"]["p999"] = ["not-a-term"]
        problems = reader_feedback.term_map_problems("sn36_6", data, self.passage_ids, self.term_ids)
        self.assertTrue(any("p999 is not a current passage" in p for p in problems))
        self.assertTrue(any("unknown term 'not-a-term'" in p for p in problems))

    def test_basis_is_required(self) -> None:
        data = copy.deepcopy(self.data)
        data["basis"] = ""
        problems = reader_feedback.term_map_problems("sn36_6", data, self.passage_ids, self.term_ids)
        self.assertTrue(any("basis" in p for p in problems))


class QuestionSetTests(unittest.TestCase):
    def test_pilot_question_sets_are_valid_drafts(self) -> None:
        for key in ("sn36_6", "an2_9", "an3_65"):
            data = reader_feedback.load_question_set(key)
            self.assertIsNotNone(data, key)
            self.assertEqual(reader_feedback.question_set_problems(key, data), [], key)
            self.assertEqual(data["editorial_status"], "draft", key)
            self.assertIsNone(data["approved_on"], key)

    def test_approval_needs_evidence_in_the_repository(self) -> None:
        data = copy.deepcopy(reader_feedback.load_question_set("sn36_6"))
        data["editorial_status"] = "approved"
        problems = reader_feedback.question_set_problems("sn36_6", data)
        self.assertTrue(any("approved_on" in p for p in problems))
        self.assertTrue(any("approval_evidence" in p for p in problems))
        data["approved_on"] = "2026-09-12"
        data["approval_evidence"] = "docs/does-not-exist.md"
        problems = reader_feedback.question_set_problems("sn36_6", data)
        self.assertTrue(any("repository file" in p for p in problems))

    def test_draft_must_not_carry_approval_fields(self) -> None:
        data = copy.deepcopy(reader_feedback.load_question_set("sn36_6"))
        data["approved_on"] = "2026-09-12"
        problems = reader_feedback.question_set_problems("sn36_6", data)
        self.assertTrue(any("must not carry approval" in p for p in problems))

    def test_each_role_appears_exactly_once(self) -> None:
        data = copy.deepcopy(reader_feedback.load_question_set("sn36_6"))
        data["questions"] = data["questions"][:2]
        problems = reader_feedback.question_set_problems("sn36_6", data)
        self.assertTrue(any("role 'reread'" in p for p in problems))

    def test_content_version_changes_when_a_prompt_changes(self) -> None:
        data = reader_feedback.load_question_set("sn36_6")
        before = reader_feedback.question_set_sha256(data)
        edited = copy.deepcopy(data)
        edited["questions"][1]["prompt"] += " Really?"
        self.assertNotEqual(before, reader_feedback.question_set_sha256(edited))
        # Guidance is for assessors, not readers, so it is not part of what
        # readers saw.
        guidance_only = copy.deepcopy(data)
        guidance_only["assessment_guidance"]["paraphrase"] += " More."
        self.assertEqual(before, reader_feedback.question_set_sha256(guidance_only))

    def test_assessment_guidance_must_say_house_terms_are_not_required(self) -> None:
        data = copy.deepcopy(reader_feedback.load_question_set("sn36_6"))
        del data["assessment_guidance"]["specific"]["not_required"]
        problems = reader_feedback.question_set_problems("sn36_6", data)
        self.assertTrue(any("not_required" in p for p in problems))


class RepositoryInputTests(unittest.TestCase):
    def test_all_feedback_inputs_pass(self) -> None:
        self.assertEqual(reader_feedback.check(), [])

    def test_only_the_pilot_text_is_enabled(self) -> None:
        self.assertEqual(reader_feedback.enabled_surfaces(), ["sn36_6"])


class ManifestScriptTests(unittest.TestCase):
    def test_manifest_script_cannot_be_closed_early(self) -> None:
        text = reader_feedback.manifest_script({"format": 1, "x": "</script><b>"})
        self.assertEqual(text.count("</script>"), 1)
        self.assertIn('id="reader-feedback-manifest"', text)
        body = text.split(">", 1)[1].rsplit("<", 1)[0]
        self.assertEqual(json.loads(body)["x"], "</script><b>")


generate_reader = load_module("generate_reader", "scripts/generate_reader.py")
build_book = load_module("build_book", "scripts/build_book.py")


def manifest_from_page(text: str) -> dict | None:
    marker = 'id="reader-feedback-manifest">'
    if marker not in text:
        return None
    body = text.split(marker, 1)[1].split("</script>", 1)[0]
    return json.loads(body)


class GeneratedPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.planned = generate_reader.planned_files()
        cls.pages = {
            path.name: content for path, content in cls.planned.items()
            if path.parent.name == "suttas"
        }

    def test_manifest_and_section_appear_only_on_enabled_pages(self) -> None:
        enabled = {surface(k).main_name for k in reader_feedback.enabled_surfaces()}
        for name, content in self.pages.items():
            has_manifest = manifest_from_page(content) is not None
            self.assertEqual(has_manifest, name in enabled, name)
            self.assertEqual('class="reader-feedback"' in content, name in enabled, name)

    def test_manifest_carries_the_version_evidence(self) -> None:
        manifest = manifest_from_page(self.pages["sn36-6-salla-sutta.md"])
        sn = surface("sn36_6")
        self.assertEqual(manifest["surface_key"], "sn36_6")
        self.assertEqual(manifest["body_sha256"], sn.readability_review.body_sha256)
        self.assertEqual(manifest["page_path"], "suttas/sn36-6-salla-sutta/")
        self.assertIsNone(manifest["endpoint"])
        self.assertEqual(manifest["transport"]["payload_field"], "entry.1359254143")
        self.assertEqual(manifest["introduction"]["kind"], "guide")
        self.assertEqual(len(manifest["introduction"]["version"]), 12)
        self.assertEqual(manifest["comprehension"]["version"], 1)
        self.assertEqual(manifest["comprehension"]["editorial_status"], "draft")
        self.assertEqual([q["role"] for q in manifest["comprehension"]["questions"]],
                         ["paraphrase", "specific", "reread"])
        self.assertNotIn("assessment_guidance", json.dumps(manifest))

    def test_passages_match_the_map_and_carry_term_basis(self) -> None:
        manifest = manifest_from_page(self.pages["sn36-6-salla-sutta.md"])
        mapping = paragraph_ids.load_map(paragraph_ids.map_path("sn36_6"))
        self.assertEqual([p["id"] for p in manifest["passages"]],
                         [e["id"] for e in mapping["passages"]])
        by_id = {p["id"]: p for p in manifest["passages"]}
        # p009 is a governed SN 36.6 phrase record, mapped explicitly.
        self.assertIn({"id": "sn36-6-two-feelings-painful-feeling", "basis": "explicit"},
                      by_id["p009"]["terms"])
        # p001 names "ordinary person", which the words-used panel links to
        # puthujjana; the explicit map already lists it, so it is not repeated.
        ids = [t["id"] for t in by_id["p001"]["terms"]]
        self.assertEqual(ids.count("puthujjana"), 1)
        # A verse with no governed rendering stays honestly unmapped.
        self.assertEqual(by_id["p036"]["mapping"], "unmapped")
        self.assertEqual(by_id["p036"]["terms"], [])
        bases = {t["basis"] for p in manifest["passages"] for t in p["terms"]}
        self.assertTrue(bases <= {"explicit", "glossary"})

    def test_glossary_versions_join_to_governed_terms_where_a_record_exists(self) -> None:
        manifest = manifest_from_page(self.pages["sn36-6-salla-sutta.md"])
        self.assertEqual(manifest["glossary"]["ordinary person"]["term_id"], "puthujjana")
        self.assertEqual(len(manifest["glossary"]["ordinary person"]["version"]), 12)

    def test_feedback_section_is_hidden_until_the_service_answers(self) -> None:
        page = self.pages["sn36-6-salla-sutta.md"]
        self.assertIn('<section class="reader-feedback" id="reader-feedback" hidden', page)
        self.assertIn('<form class="reader-review" id="reader-review" novalidate>', page)
        self.assertIn('<label for="reader-review-arrows">', page)
        self.assertIn("How feedback is used", page)

    def test_governed_body_is_unchanged_by_feedback(self) -> None:
        sn = surface("sn36_6")
        body = generate_reader.surface_body(sn.main_path.read_text(encoding="utf-8"))
        self.assertIn(body, self.pages["sn36-6-salla-sutta.md"])

    def test_epub_drops_feedback_furniture(self) -> None:
        stripped = build_book.strip_web_furniture(self.pages["sn36-6-salla-sutta.md"])
        self.assertNotIn("reader-feedback", stripped)
        self.assertNotIn("<script", stripped)
        self.assertIn("### Two Arrows", stripped)

    def test_a_stale_map_stops_generation_with_a_repair_hint(self) -> None:
        sn = surface("sn36_6")
        glossary = generate_reader.load_glossary()
        body = generate_reader.surface_body(sn.main_path.read_text(encoding="utf-8"))
        entries = generate_reader.glossary_for_page(body, glossary)
        config = reader_feedback.load_config()
        with self.assertRaises(ValueError) as caught:
            generate_reader.feedback_manifest(
                sn, body.replace("Two Arrows", "Two Arrows\n\nAn added passage."),
                glossary, entries, None, None, config,
            )
        self.assertIn("paragraph_ids.py --write", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
