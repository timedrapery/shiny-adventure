from __future__ import annotations

import csv
import io
import json
import tempfile
import unittest
from pathlib import Path

from feedback_service import ingest
from feedback_service.storage import Storage
from tests.test_feedback_service import comprehension_payload, translation_payload


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

    def test_rows_are_validated_stored_and_deduplicated(self) -> None:
        path = sheet([
            ("9/13/2026 10:15:02", translation_payload()),
            ("9/13/2026 10:15:09", translation_payload(comment="retry duplicate")),
            ("9/13/2026 10:16:00", translation_payload(client_submission_id="second-0000002", category="rude")),
            ("9/13/2026 10:17:00", "not json at all"),
            ("9/13/2026 10:18:00", translation_payload(client_submission_id="spam-00000003", website="http://x")),
        ])
        result = ingest.ingest_csv(self.storage, path)
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
        result = ingest.ingest_csv(self.storage, path)
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
            ingest.ingest_csv(self.storage, Path(handle.name))

    def test_unknown_timestamp_falls_back_to_ingest_time(self) -> None:
        path = sheet([("yesterday-ish", translation_payload())])
        result = ingest.ingest_csv(self.storage, path)
        row = self.storage.submission(result.stored[0])
        self.assertTrue(row["received_at"].endswith("Z"))


if __name__ == "__main__":
    unittest.main()
