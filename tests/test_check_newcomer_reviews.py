from __future__ import annotations

import copy
import unittest

from scripts import check_newcomer_reviews as reviews


class NewcomerReviewLedgerTests(unittest.TestCase):
    def test_repository_ledger_is_well_formed(self) -> None:
        self.assertEqual(reviews.collect_failures(reviews.load_ledger()), [])

    def test_false_ready_status_is_rejected(self) -> None:
        data = copy.deepcopy(reviews.load_ledger())
        key = data["cohort"][0]
        data["surfaces"][key]["status"] = "ready"
        failures = reviews.collect_failures(data)
        self.assertTrue(any("requires all three evidence gates" in item for item in failures))

    def test_duplicate_participant_is_rejected(self) -> None:
        data = copy.deepcopy(reviews.load_ledger())
        key = data["cohort"][0]
        sample = {
            "participant": "R1",
            "reviewed_on": "2026-08-24",
            "independent": True,
            "what_happened": "A clear account.",
            "practical_point": "A clear practical point.",
            "confusing_words": [],
            "pass": True,
        }
        data["surfaces"][key]["newcomer_reviews"] = [sample, copy.deepcopy(sample)]
        failures = reviews.collect_failures(data)
        self.assertTrue(any("duplicate participant" in item for item in failures))


if __name__ == "__main__":
    unittest.main()
