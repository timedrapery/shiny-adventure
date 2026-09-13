from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from tests.helpers import load_module


stage_evidence = load_module("stage_feedback_evidence", "scripts/stage_feedback_evidence.py")
newcomer_checks = load_module("check_newcomer_reviews", "scripts/check_newcomer_reviews.py")
readability = load_module("check_readability_reviews", "scripts/check_readability_reviews.py")
registry = load_module("surface_registry", "scripts/surface_registry.py")

REPO_ROOT = Path(__file__).resolve().parent.parent
SN36_6 = next(s for s in registry.TRANSLATION_SURFACES if s.key == "sn36_6")
CURRENT_HASH = readability.translation_body_sha256(SN36_6.main_path)


def export_fixture(**overrides) -> dict:
    # Synthetic fixture for the test suite only. Not evidence.
    record = {
        "participant": "R1",
        "participant_kind": "fresh",
        "returning_from": None,
        "reviewed_on": "2026-09-12",
        "independent": True,
        "what_happened": "Two people both feel pain; one also gets upset about it.",
        "practical_point": "The first arrow is the pain and the second is the fuss on top.",
        "confusing_words": ["underlying tendency"],
        "pass": True,
        "assessment": "pass",
        "assessment_note": "",
        "body_sha256": CURRENT_HASH,
        "familiarity": "new",
        "question_version": 1,
        "question_set_sha256": "a" * 64,
        "question_editorial_status": "draft",
        "submission_id": "fb_test000001",
    }
    record.update(overrides)
    return {
        "export_kind": "formal-session-review",
        "export_format": 1,
        "exported_at": "2026-09-12T00:00:00Z",
        "session": {"code": "pilot001", "surface_key": "sn36_6", "title": "", "created_at": "", "closed_at": None},
        "participants": [{"label": "R1", "kind": "fresh", "independent": 1}],
        "records": [record],
        "excluded": [],
    }


class StagingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ledger = newcomer_checks.load_ledger()

    def test_current_body_record_is_staged_and_counts(self) -> None:
        records, notes = stage_evidence.stage(export_fixture(), self.ledger)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["participant"], "R1")
        self.assertEqual(records[0]["evidence_source"]["session"], "pilot001")
        self.assertTrue(any("counts toward the threshold" in n for n in notes))
        self.assertTrue(any("DRAFT question set" in n for n in notes))
        updated = stage_evidence.apply(self.ledger, "sn36_6", records)
        self.assertEqual(newcomer_checks.collect_failures(updated, REPO_ROOT), [])

    def test_older_body_is_staged_as_history_only(self) -> None:
        records, notes = stage_evidence.stage(export_fixture(body_sha256="b" * 64), self.ledger)
        self.assertEqual(len(records), 1)
        self.assertTrue(any("does not count" in n for n in notes))

    def test_public_export_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "queue.json"
            path.write_text(json.dumps({"export_kind": "reader-feedback-queue", "export_format": 1}), encoding="utf-8")
            with self.assertRaises(stage_evidence.StagingError):
                stage_evidence.load_export(path)

    def test_unassessed_record_is_refused(self) -> None:
        with self.assertRaises(stage_evidence.StagingError):
            stage_evidence.stage(export_fixture(assessment=None), self.ledger)

    def test_returning_reader_gets_a_distinct_ledger_label(self) -> None:
        ledger = copy.deepcopy(self.ledger)
        ledger["surfaces"]["sn36_6"]["newcomer_reviews"].append({
            "participant": "R1", "reviewed_on": "2026-09-01", "independent": True,
            "what_happened": "x", "practical_point": "y", "confusing_words": [], "pass": True,
            "body_sha256": "c" * 64,
        })
        fixture = export_fixture(participant_kind="returning",
                                 returning_from={"session": "pilot000", "participant": "R1"})
        records, _ = stage_evidence.stage(fixture, ledger)
        self.assertEqual(records[0]["participant"], "R1@pilot001")
        self.assertEqual(records[0]["evidence_source"]["participant_kind"], "returning")
        updated = stage_evidence.apply(ledger, "sn36_6", records)
        self.assertEqual(newcomer_checks.collect_failures(updated, REPO_ROOT), [])

    def test_already_staged_submission_is_skipped(self) -> None:
        records, _ = stage_evidence.stage(export_fixture(), self.ledger)
        updated = stage_evidence.apply(self.ledger, "sn36_6", records)
        again, notes = stage_evidence.stage(export_fixture(), updated)
        self.assertEqual(again, [])
        self.assertTrue(any("already in the ledger" in n for n in notes))

    def test_staging_never_marks_a_surface_validated(self) -> None:
        fixtures = export_fixture()
        fixtures["records"] = [
            dict(fixtures["records"][0], participant=f"R{i}", submission_id=f"fb_test00000{i}")
            for i in range(1, 6)
        ]
        records, _ = stage_evidence.stage(fixtures, self.ledger)
        updated = stage_evidence.apply(self.ledger, "sn36_6", records)
        self.assertEqual(updated["surfaces"]["sn36_6"]["status"], "recruiting")
        self.assertEqual(newcomer_checks.collect_failures(updated, REPO_ROOT), [])
        # Even five passing sessions leave the read-aloud gate pending, and the
        # registry unchanged: nothing in this path can promote the text.
        self.assertEqual(SN36_6.readability_review.status, "provisional")

    def test_unregistered_surface_is_refused(self) -> None:
        fixture = export_fixture()
        fixture["session"]["surface_key"] = "zz9"
        with self.assertRaises(stage_evidence.StagingError):
            stage_evidence.stage(fixture, self.ledger)


if __name__ == "__main__":
    unittest.main()
