from __future__ import annotations

import csv
import io
import json
import tempfile
import unittest
from pathlib import Path

from feedback_service import export, ingest
from feedback_service.storage import Storage
from tests.test_feedback_service import comprehension_payload, translation_payload


# The sheet locale used by most tests: month first, in UTC.
SHEET = {"date_order": "mdy", "timezone_name": "UTC"}


def sheet(rows: list[tuple[str, object]]) -> Path:
    handle = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8", newline="")
    writer = csv.writer(handle)
    writer.writerow(["Timestamp", "Feedback payload"])
    for stamp, payload in rows:
        writer.writerow([stamp, payload if isinstance(payload, str) else json.dumps(payload)])
    handle.close()
    return Path(handle.name)


class IngestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.storage = Storage(":memory:")
        self.addCleanup(self.storage.close)

    def test_rows_are_validated_stored_and_deduplicated(self) -> None:
        path = sheet([
            ("9/13/2026 10:15:02", translation_payload()),
            ("9/13/2026 10:15:09", translation_payload(comment="retry duplicate")),
            ("9/13/2026 10:16:00", translation_payload(client_submission_id="second-0000002", category="rude")),
            ("9/13/2026 10:17:00", "not json at all"),
            ("9/13/2026 10:18:00", translation_payload(client_submission_id="spam-00000003", website="http://x")),
        ])
        result = ingest.ingest_csv(self.storage, path, **SHEET)
        self.assertEqual(len(result.stored), 1)
        self.assertEqual(len(result.duplicates), 1)
        self.assertEqual([line for line, _ in result.rejected], [4, 5])
        self.assertEqual(result.dropped, [6])
        self.assertEqual(self.storage.counts()["submissions"], 1)
        row = self.storage.submission(result.stored[0])
        self.assertEqual(row["received_at"], "2026-09-13T10:15:02Z")
        self.assertEqual(row["comment"], "Twice? I thought there was only one arrow so far.")
        self.assertEqual([t["term_id"] for t in self.storage.terms_for(row["id"])],
                         ["sn36-6-two-feelings-painful-feeling"])

    def test_formal_session_rows_resolve_against_local_sessions(self) -> None:
        session = self.storage.create_session("sn36_6", code="pilot001")
        self.storage.add_participant(session["id"], "R1", "fresh", independent=True)
        path = sheet([
            ("2026-09-13 11:00:00", comprehension_payload("form-0000001", session={"code": "pilot001", "participant": "R1"})),
            ("2026-09-13 11:05:00", comprehension_payload("form-0000002", session={"code": "pilot001", "participant": "R1"})),
            ("2026-09-13 11:06:00", comprehension_payload("form-0000003", session={"code": "nope0001", "participant": "R1"})),
        ])
        result = ingest.ingest_csv(self.storage, path, **SHEET)
        self.assertEqual(len(result.stored), 2)
        self.assertEqual(len(result.rejected), 1)
        first = self.storage.submission(result.stored[0])
        second = self.storage.submission(result.stored[1])
        self.assertEqual(first["channel"], "formal")
        self.assertEqual(first["counts_for_session"], 1)
        self.assertEqual(second["counts_for_session"], 0)

    def test_sheet_shape_is_checked(self) -> None:
        handle = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8", newline="")
        csv.writer(handle).writerow(["Timestamp", "One", "Two"])
        handle.close()
        with self.assertRaises(ValueError):
            ingest.ingest_csv(self.storage, Path(handle.name), **SHEET)

    def test_unknown_timestamp_falls_back_to_ingest_time_with_a_note(self) -> None:
        path = sheet([("yesterday-ish", translation_payload())])
        result = ingest.ingest_csv(self.storage, path, **SHEET)
        row = self.storage.submission(result.stored[0])
        self.assertTrue(row["received_at"].endswith("Z"))
        self.assertIn("'yesterday-ish' could not be read as mdy in UTC", row["received_at_note"])
        self.assertEqual(result.unread_timestamps, [(2, "yesterday-ish")])
        self.assertIn("unreadable timestamp 1", result.summary())

    def test_a_readable_timestamp_carries_no_note(self) -> None:
        result = ingest.ingest_csv(self.storage, sheet([("9/13/2026 10:15:02", translation_payload())]), **SHEET)
        self.assertEqual(self.storage.submission(result.stored[0])["received_at_note"], "")

    def test_day_first_sheets_are_read_day_first(self) -> None:
        path = sheet([("03/04/2026 10:00:00", translation_payload())])
        result = ingest.ingest_csv(self.storage, path, date_order="dmy", timezone_name="UTC")
        self.assertEqual(self.storage.submission(result.stored[0])["received_at"], "2026-04-03T10:00:00Z")

    def test_month_first_sheets_are_read_month_first(self) -> None:
        path = sheet([("03/04/2026 10:00:00", translation_payload())])
        result = ingest.ingest_csv(self.storage, path, **SHEET)
        self.assertEqual(self.storage.submission(result.stored[0])["received_at"], "2026-03-04T10:00:00Z")

    def test_sheet_local_time_is_converted_to_utc(self) -> None:
        path = sheet([("9/13/2026 10:15:02", translation_payload())])
        result = ingest.ingest_csv(self.storage, path, date_order="mdy", timezone_name="America/Los_Angeles")
        # Pacific daylight time is seven hours behind UTC in September.
        self.assertEqual(self.storage.submission(result.stored[0])["received_at"], "2026-09-13T17:15:02Z")

    def test_an_explicit_utc_stamp_ignores_the_sheet_zone(self) -> None:
        path = sheet([("2026-09-13T10:15:02Z", translation_payload())])
        result = ingest.ingest_csv(self.storage, path, date_order="dmy", timezone_name="Asia/Tokyo")
        self.assertEqual(self.storage.submission(result.stored[0])["received_at"], "2026-09-13T10:15:02Z")

    def test_an_unknown_zone_or_date_order_stops_before_anything_is_stored(self) -> None:
        path = sheet([("9/13/2026 10:15:02", translation_payload())])
        with self.assertRaises(ValueError):
            ingest.ingest_csv(self.storage, path, date_order="mdy", timezone_name="Mars/Olympus")
        with self.assertRaises(ValueError):
            ingest.ingest_csv(self.storage, path, date_order="ymd", timezone_name="UTC")
        self.assertEqual(self.storage.counts()["submissions"], 0)

    def test_a_closed_session_is_refused_as_the_live_endpoint_refuses_it(self) -> None:
        session = self.storage.create_session("sn36_6", code="pilot002")
        self.storage.add_participant(session["id"], "R1", "fresh", independent=True)
        self.storage.connection.execute(
            "UPDATE sessions SET closed_at = '2026-09-13T12:00:00Z' WHERE id = ?", (session["id"],)
        )
        formal = {"code": "pilot002", "participant": "R1"}
        path = sheet([
            ("9/13/2026 11:00:00", comprehension_payload("form-0000010", session=formal)),
            ("9/13/2026 13:00:00", comprehension_payload("form-0000011", session=formal)),
            ("whenever", comprehension_payload("form-0000012", session=formal)),
        ])
        result = ingest.ingest_csv(self.storage, path, **SHEET)
        # Received before the session closed: still valid evidence.
        self.assertEqual(len(result.stored), 1)
        self.assertEqual(result.rejected, [(3, "session: closed"), (4, "session: closed")])

    def test_a_response_with_an_unknown_time_is_kept_out_of_the_evidence_export(self) -> None:
        session = self.storage.create_session("sn36_6", code="pilot003")
        participant = self.storage.add_participant(session["id"], "R1", "fresh", independent=True)
        formal = {"code": "pilot003", "participant": "R1"}
        result = ingest.ingest_csv(
            self.storage, sheet([("whenever", comprehension_payload("form-0000020", session=formal))]), **SHEET
        )
        row = self.storage.submission(result.stored[0])
        self.storage.record_assessment(row["id"], "pass", "")
        data = export.session_export(self.storage, "pilot003")
        self.assertEqual(data["records"], [])
        self.assertIn("could not be read", data["excluded"][0]["reason"])
        self.assertIsNotNone(participant)

    def test_one_unreadable_row_does_not_stop_the_rows_after_it(self) -> None:
        # Anyone can post to the public form. Each of these rows used to raise
        # out of the import, so every valid response after it was never stored.
        path = sheet([
            ("9/13/2026 10:15:02", translation_payload()),
            ("9/13/2026 10:16:00", translation_payload(client_submission_id="surrogate-00001", comment="\ud800")),
            ("9/13/2026 10:17:00", comprehension_payload("hugeint-0000001", question_version=10**30)),
            ("9/13/2026 10:18:00", "x" * 200_000),
            ("9/13/2026 10:19:00", "1" * 5000),
            ("9/13/2026 10:20:00", translation_payload(client_submission_id="after-00000002")),
        ])
        result = ingest.ingest_csv(self.storage, path, **SHEET)
        # The surrogate is kept as a visible replacement mark and stored; the
        # other three cannot be read and are reported by line.
        self.assertEqual(len(result.stored), 3, result.rejected)
        self.assertEqual([line for line, _ in result.rejected], [4, 5, 6])
        self.assertEqual(self.storage.submission(result.stored[1])["comment"], "\ufffd")
        self.assertEqual(self.storage.counts()["submissions"], 3)


if __name__ == "__main__":
    unittest.main()
