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

    def approved(self, **overrides) -> dict:
        return export_fixture(question_editorial_status="approved", **overrides)

    def test_current_body_record_is_staged_and_counts(self) -> None:
        records, notes = stage_evidence.stage(self.approved(), self.ledger)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["participant"], "R1")
        self.assertFalse(records[0]["follow_up"])
        self.assertEqual(records[0]["evidence_source"]["session"], "pilot001")
        self.assertEqual(records[0]["evidence_source"]["question_set_sha256"], "a" * 64)
        self.assertFalse(records[0]["evidence_source"]["draft_questions_accepted_by_editor"])
        self.assertTrue(any("current body" in n for n in notes))
        updated = stage_evidence.apply(self.ledger, "sn36_6", records)
        self.assertEqual(newcomer_checks.collect_failures(updated, REPO_ROOT), [])

    def test_draft_question_responses_are_exploratory_unless_an_editor_accepts_them(self) -> None:
        records, notes = stage_evidence.stage(export_fixture(), self.ledger)
        self.assertEqual(records, [])
        self.assertTrue(any("not staged" in n and "draft" in n for n in notes))
        records, notes = stage_evidence.stage(export_fixture(), self.ledger, accept_draft_questions=True)
        self.assertEqual(len(records), 1)
        self.assertTrue(records[0]["evidence_source"]["draft_questions_accepted_by_editor"])
        self.assertEqual(records[0]["evidence_source"]["question_editorial_status"], "draft")

    def test_older_body_is_staged_as_history_only(self) -> None:
        records, notes = stage_evidence.stage(self.approved(body_sha256="b" * 64), self.ledger)
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
            stage_evidence.stage(self.approved(assessment=None), self.ledger)

    def test_returning_reader_keeps_identity_and_never_counts_as_independent(self) -> None:
        ledger = copy.deepcopy(self.ledger)
        ledger["surfaces"]["sn36_6"]["newcomer_reviews"].append({
            "participant": "R1", "reviewed_on": "2026-09-01", "independent": True,
            "what_happened": "x", "practical_point": "y", "confusing_words": [], "pass": True,
            "body_sha256": "c" * 64,
        })
        # The service labels them R7 in the later session and, wrongly, independent.
        fixture = self.approved(participant="R7", participant_kind="returning", independent=True,
                                returning_from={"session": "pilot000", "participant": "R1"})
        records, notes = stage_evidence.stage(fixture, ledger)
        record = records[0]
        self.assertEqual(record["participant"], "R1")
        self.assertTrue(record["follow_up"])
        self.assertFalse(record["independent"])
        self.assertEqual(record["evidence_source"]["session_label"], "R7")
        self.assertTrue(any("staged as independent: false" in n for n in notes))
        updated = stage_evidence.apply(ledger, "sn36_6", records)
        self.assertEqual(newcomer_checks.collect_failures(updated, REPO_ROOT), [])
        # One participant for the current body, zero independent passes.
        failures: list[str] = []
        count, passes = newcomer_checks.count_newcomer_evidence(
            "sn36_6", updated["surfaces"]["sn36_6"]["newcomer_reviews"], CURRENT_HASH, failures
        )
        self.assertEqual((count, passes, failures), (1, 0, []))

    def test_returning_reader_without_an_earlier_record_is_refused(self) -> None:
        fixture = self.approved(participant_kind="returning",
                                returning_from={"session": "pilot000", "participant": "R1"})
        with self.assertRaises(stage_evidence.StagingError):
            stage_evidence.stage(fixture, self.ledger)

    def test_fresh_reader_cannot_reuse_a_ledger_label(self) -> None:
        ledger = copy.deepcopy(self.ledger)
        ledger["surfaces"]["sn36_6"]["newcomer_reviews"].append({
            "participant": "R1", "reviewed_on": "2026-09-01", "independent": True,
            "what_happened": "x", "practical_point": "y", "confusing_words": [], "pass": True,
            "body_sha256": "c" * 64,
        })
        with self.assertRaises(stage_evidence.StagingError):
            stage_evidence.stage(self.approved(), ledger)

    def test_already_staged_submission_is_skipped(self) -> None:
        records, _ = stage_evidence.stage(self.approved(), self.ledger)
        updated = stage_evidence.apply(self.ledger, "sn36_6", records)
        again, notes = stage_evidence.stage(self.approved(), updated)
        self.assertEqual(again, [])
        self.assertTrue(any("already in the ledger" in n for n in notes))

    def test_staging_never_marks_a_surface_validated(self) -> None:
        fixtures = self.approved()
        fixtures["records"] = [
            dict(fixtures["records"][0], participant=f"R{i}", submission_id=f"fb_test00000{i}")
            for i in range(1, 6)
        ]
        records, _ = stage_evidence.stage(fixtures, self.ledger)
        updated = stage_evidence.apply(self.ledger, "sn36_6", records)
        self.assertEqual(updated["surfaces"]["sn36_6"]["status"], "recruiting")
        self.assertEqual(newcomer_checks.collect_failures(updated, REPO_ROOT), [])
        self.assertEqual(SN36_6.readability_review.status, "provisional")

    def test_unregistered_surface_is_refused(self) -> None:
        fixture = self.approved()
        fixture["session"]["surface_key"] = "zz9"
        with self.assertRaises(stage_evidence.StagingError):
            stage_evidence.stage(fixture, self.ledger)


if __name__ == "__main__":
    unittest.main()
