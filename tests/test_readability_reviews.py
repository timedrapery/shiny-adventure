from __future__ import annotations

import tempfile
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

    def test_every_surface_has_current_review_metadata(self) -> None:
        # Deliberately not `assertEqual(status, "provisional")`. That pinned
        # the repository at the state it happened to be in, so the first
        # genuinely validated surface would have failed CI -- the evidence
        # work had nowhere to land. The status must be a legal one; whether
        # it is earned is the ledger's question, not this test's.
        self.assertTrue(readability_reviews.TRANSLATION_SURFACES)

        for surface in readability_reviews.TRANSLATION_SURFACES:
            with self.subTest(surface=surface.key):
                review = surface.readability_review
                self.assertIsNotNone(review)
                assert review is not None

                self.assertEqual(review.standard, readability_reviews.STANDARD)
                self.assertIn(review.status, readability_reviews.REVIEW_STATUSES)
                self.assertTrue(readability_reviews.is_iso_date(review.revised_on))
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
                revised_on="not-a-date",
            ),
        )

        failures = readability_reviews.review_failures((changed,), REPO_ROOT)

        self.assertTrue(any("unknown readability review status" in item for item in failures))
        self.assertTrue(any("revised_on must be an ISO date" in item for item in failures))

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
            any("recorded body hash is stale" in failure for failure in failures),
            failures,
        )

    def test_validated_status_requires_all_human_review_gates(self) -> None:
        # Built in a scratch repository so the test does not depend on what
        # any real surface's notes happen to say about its review gates.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "t.md").write_text("# T\n\n## Translation\n\nBody.\n", encoding="utf-8")
            (root / "t-notes.md").write_text(
                "# Notes\n\n## Readability Review\n\n"
                "- Standard: `plain-english-v1`\n- Status: `validated`\n"
                "- Source-fidelity review: complete.\n"
                "- Human read-aloud usability review: pending.\n"
                "- Newcomer comprehension review: pending.\n",
                encoding="utf-8",
            )
            surface = readability_reviews.TranslationSurface(
                key="t1",
                label="T 1",
                main_relpath="t.md",
                notes_relpath="t-notes.md",
                readability_review=replace(
                    sn36_surface().readability_review,
                    status="validated",
                    body_sha256=readability_reviews.translation_body_sha256(root / "t.md"),
                ),
            )

            failures = readability_reviews.review_failures((surface,), root)

        self.assertFalse(
            any("source-fidelity review: complete" in item for item in failures), failures
        )
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
