from __future__ import annotations

import unittest
from dataclasses import replace
from pathlib import Path

from tests.helpers import load_module


readability_reviews = load_module(
    "check_readability_reviews",
    "scripts/check_readability_reviews.py",
)

REPO_ROOT = Path(__file__).resolve().parent.parent


def sn36_surface():
    return next(
        surface
        for surface in readability_reviews.TRANSLATION_SURFACES
        if surface.key == "sn36_6"
    )


class CurrentReadabilityReviewTests(unittest.TestCase):
    def test_current_reviews_validate(self) -> None:
        self.assertEqual(readability_reviews.collect_failures(), [])

    def test_every_surface_has_current_provisional_metadata(self) -> None:
        self.assertTrue(readability_reviews.TRANSLATION_SURFACES)

        for surface in readability_reviews.TRANSLATION_SURFACES:
            with self.subTest(surface=surface.key):
                review = surface.readability_review
                self.assertIsNotNone(review)
                assert review is not None

                self.assertEqual(review.standard, readability_reviews.STANDARD)
                self.assertEqual(review.status, "provisional")
                self.assertTrue(readability_reviews.is_iso_date(review.reviewed_on))
                self.assertEqual(
                    review.body_sha256,
                    readability_reviews.translation_body_sha256(surface.main_path),
                )


class ReviewValidationTests(unittest.TestCase):
    def test_missing_readability_review_is_rejected(self) -> None:
        changed = replace(sn36_surface(), readability_review=None)

        failures = readability_reviews.review_failures((changed,), REPO_ROOT)

        self.assertTrue(
            any("missing readability_review" in failure for failure in failures),
            failures,
        )

    def test_wrong_standard_is_rejected(self) -> None:
        surface = sn36_surface()
        review = surface.readability_review
        assert review is not None
        changed = replace(
            surface,
            readability_review=replace(review, standard="wrong-standard-v9"),
        )

        failures = readability_reviews.review_failures((changed,), REPO_ROOT)

        self.assertTrue(
            any("readability standard must be" in failure for failure in failures),
            failures,
        )

    def test_unknown_status_and_bad_date_are_rejected(self) -> None:
        surface = sn36_surface()
        review = surface.readability_review
        assert review is not None
        changed = replace(
            surface,
            readability_review=replace(
                review,
                status="approved-by-automation",
                reviewed_on="not-a-date",
            ),
        )

        failures = readability_reviews.review_failures((changed,), REPO_ROOT)

        self.assertTrue(any("unknown readability review status" in item for item in failures))
        self.assertTrue(any("reviewed_on must be an ISO date" in item for item in failures))

    def test_reviewed_body_hash_drift_is_rejected(self) -> None:
        surface = sn36_surface()
        review = surface.readability_review
        assert review is not None
        changed = replace(
            surface,
            readability_review=replace(review, body_sha256="0" * 64),
        )

        failures = readability_reviews.review_failures((changed,), REPO_ROOT)

        self.assertTrue(
            any("reviewed body hash is stale" in failure for failure in failures),
            failures,
        )

    def test_validated_status_requires_all_human_review_gates(self) -> None:
        surface = sn36_surface()
        review = surface.readability_review
        assert review is not None
        changed = replace(
            surface,
            readability_review=replace(review, status="validated"),
        )

        failures = readability_reviews.review_failures((changed,), REPO_ROOT)

        self.assertTrue(
            any("human read-aloud usability review: complete" in item for item in failures),
            failures,
        )
        self.assertTrue(
            any("newcomer comprehension review: complete" in item for item in failures),
            failures,
        )


if __name__ == "__main__":
    unittest.main()
