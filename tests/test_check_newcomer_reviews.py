from __future__ import annotations

import copy
import unittest
from dataclasses import replace
from unittest import mock

from scripts import check_newcomer_reviews as reviews


def current_hash(key: str) -> str:
    surface = next(s for s in reviews.TRANSLATION_SURFACES if s.key == key)
    hash_value = reviews.current_body_hash(surface, reviews.REPO_ROOT)
    assert hash_value is not None
    return hash_value


def review_entry(participant: str, body_sha256: str) -> dict[str, object]:
    return {
        "participant": participant,
        "reviewed_on": "2026-08-24",
        "independent": True,
        "what_happened": "A clear account.",
        "practical_point": "A clear practical point.",
        "confusing_words": [],
        "pass": True,
        "body_sha256": body_sha256,
    }


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


class EvidenceIsBoundToABodyTests(unittest.TestCase):
    """Human evidence is evidence about a particular text, not a filename."""

    def fully_evidenced(self, key: str, body_sha256: str) -> dict[str, object]:
        data = copy.deepcopy(reviews.load_ledger())
        record = data["surfaces"][key]
        record["status"] = "ready"
        record["human_read_aloud"] = {
            "status": "complete",
            "reviewers": ["R1"],
            "body_sha256": body_sha256,
        }
        required = data["threshold"]["participants_required"]
        record["newcomer_reviews"] = [
            review_entry(f"R{index}", body_sha256) for index in range(1, required + 1)
        ]
        return data

    def test_a_review_without_the_body_it_read_is_rejected(self) -> None:
        key = "an2_9"
        data = self.fully_evidenced(key, current_hash(key))
        del data["surfaces"][key]["newcomer_reviews"][0]["body_sha256"]

        failures = reviews.collect_failures(data)

        self.assertTrue(
            any("body_sha256 of the reviewed text is required" in item for item in failures),
            failures,
        )

    def test_reviews_of_the_current_body_satisfy_the_threshold(self) -> None:
        key = "an2_9"
        data = self.fully_evidenced(key, current_hash(key))

        self.assertEqual(reviews.collect_failures(data), [])

    def test_reviews_of_an_older_body_stop_counting(self) -> None:
        # The whole point: editing the translation must not inherit approval
        # from readers who never saw the edit. The records stay as history.
        key = "an2_9"
        data = self.fully_evidenced(key, "0" * 64)

        failures = reviews.collect_failures(data)

        self.assertTrue(any("requires all three evidence gates" in item for item in failures), failures)
        self.assertTrue(
            any("read-aloud evidence is for an older body" in item for item in failures),
            failures,
        )


class RegistryDrivesEnforcementTests(unittest.TestCase):
    def test_a_validated_surface_missing_from_the_ledger_is_rejected(self) -> None:
        # Enforcement once iterated the cohort alone, so promoting a surface
        # in the registry without adding it to the ledger skipped every gate.
        data = copy.deepcopy(reviews.load_ledger())
        outside = next(
            surface
            for surface in reviews.TRANSLATION_SURFACES
            if surface.key not in data["surfaces"]
        )
        review = outside.readability_review
        assert review is not None
        promoted = replace(outside, readability_review=replace(review, status="validated"))
        surfaces = tuple(
            promoted if surface.key == outside.key else surface
            for surface in reviews.TRANSLATION_SURFACES
        )

        with mock.patch.object(reviews, "TRANSLATION_SURFACES", surfaces):
            failures = reviews.collect_failures(data)

        self.assertEqual(
            failures,
            [f"{outside.key}: registry says validated but the ledger has no record for it"],
        )


if __name__ == "__main__":
    unittest.main()
