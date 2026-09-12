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


def review_entry(participant: str, body_sha256: str, **overrides: object) -> dict[str, object]:
    entry: dict[str, object] = {
        "participant": participant,
        "reviewed_on": "2026-08-24",
        "independent": True,
        "what_happened": "A clear account.",
        "practical_point": "A clear practical point.",
        "confusing_words": [],
        "pass": True,
        "body_sha256": body_sha256,
    }
    entry.update(overrides)
    return entry


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
        sample = review_entry("R1", current_hash(key))
        data["surfaces"][key]["newcomer_reviews"] = [sample, copy.deepcopy(sample)]
        failures = reviews.collect_failures(data)
        self.assertTrue(any("duplicate participant" in item for item in failures))

    def test_a_review_with_no_body_hash_cannot_fill_a_seat(self) -> None:
        # The duplicate check keys on (participant, body), so an entry with no
        # body recorded is rejected before it can be counted at all rather
        # than silently passing through that pairing.
        data = copy.deepcopy(reviews.load_ledger())
        key = data["cohort"][0]
        sample = review_entry("R1", current_hash(key))
        del sample["body_sha256"]
        data["surfaces"][key]["newcomer_reviews"] = [sample]
        failures = reviews.collect_failures(data)
        self.assertTrue(
            any("body_sha256 of the reviewed text is required" in item for item in failures),
            failures,
        )


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


class ReviewLifecycleTests(unittest.TestCase):
    """A translation can be revised and reviewed again without losing history."""

    OLD_BODY = "a" * 64

    def ledger_with(self, key: str, entries: list[dict[str, object]]) -> dict[str, object]:
        data = copy.deepcopy(reviews.load_ledger())
        data["surfaces"][key]["newcomer_reviews"] = entries
        return data

    def test_a_returning_participant_may_review_the_revised_body(self) -> None:
        # The protocol says to keep the old record and repeat the affected
        # review. Checking the participant label across the whole history made
        # the returning reader collide with their own earlier entry, so the
        # documented workflow reported `duplicate participant R1`.
        key = "an2_9"
        data = self.ledger_with(
            key,
            [
                review_entry("R1", self.OLD_BODY, reviewed_on="2026-08-24"),
                review_entry(
                    "R1",
                    current_hash(key),
                    reviewed_on="2026-09-10",
                    follow_up=True,
                    independent=False,
                ),
            ],
        )

        self.assertEqual(reviews.collect_failures(data), [])

        # The historical record is still there to read.
        kept = data["surfaces"][key]["newcomer_reviews"][0]
        self.assertEqual(kept["body_sha256"], self.OLD_BODY)

    def test_the_same_participant_twice_on_one_body_is_still_a_duplicate(self) -> None:
        key = "an2_9"
        body = current_hash(key)
        data = self.ledger_with(
            key,
            [
                review_entry("R1", body, reviewed_on="2026-09-10"),
                review_entry("R1", body, reviewed_on="2026-09-11"),
            ],
        )

        failures = reviews.collect_failures(data)

        self.assertIn("an2_9: duplicate participant R1 for one body version", failures)

    def test_an_unmarked_follow_up_is_rejected_and_the_original_is_not(self) -> None:
        key = "an2_9"
        data = self.ledger_with(
            key,
            [
                review_entry("R1", self.OLD_BODY, reviewed_on="2026-08-24"),
                review_entry("R1", current_hash(key), reviewed_on="2026-09-10"),
            ],
        )

        failures = reviews.collect_failures(data)

        self.assertTrue(all("review 1" not in failure for failure in failures), failures)
        self.assertTrue(
            any("review 2: R1 reviewed another body of this text" in f for f in failures),
            failures,
        )
        self.assertTrue(
            any("review 2: a returning reader cannot give a first unprompted" in f for f in failures),
            failures,
        )

    def test_follow_up_without_an_earlier_review_is_rejected(self) -> None:
        key = "an2_9"
        data = self.ledger_with(
            key,
            [review_entry("R1", current_hash(key), follow_up=True, independent=False)],
        )

        failures = reviews.collect_failures(data)

        self.assertTrue(
            any("follow_up is recorded but this participant has no review" in f for f in failures),
            failures,
        )

    def test_a_follow_up_fills_a_seat_but_never_an_independent_pass(self) -> None:
        # Five readers of the current body, one of them returning: the
        # participant count is met, the independent-pass count is one short.
        key = "an2_9"
        body = current_hash(key)
        data = self.ledger_with(
            key,
            [review_entry("R1", self.OLD_BODY, reviewed_on="2026-08-24")]
            + [
                review_entry("R1", body, reviewed_on="2026-09-10", follow_up=True, independent=False),
                review_entry("R2", body, reviewed_on="2026-09-10"),
                review_entry("R3", body, reviewed_on="2026-09-10"),
                review_entry("R4", body, reviewed_on="2026-09-10"),
                review_entry("R5", body, reviewed_on="2026-09-10"),
            ],
        )
        record = data["surfaces"][key]
        record["status"] = "ready"
        record["human_read_aloud"] = {"status": "complete", "reviewers": ["A1"], "body_sha256": body}
        record["source_fidelity"]["body_sha256"] = body

        count, passes = reviews.count_newcomer_evidence(
            key, record["newcomer_reviews"], body, []
        )

        self.assertEqual((count, passes), (5, 4))
        self.assertEqual(reviews.collect_failures(data), [])


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
