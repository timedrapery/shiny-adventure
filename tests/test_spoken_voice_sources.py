from __future__ import annotations

import copy
import unittest
from dataclasses import replace
from pathlib import Path

from tests.helpers import load_module


spoken_sources = load_module(
    "check_spoken_voice_sources",
    "scripts/check_spoken_voice_sources.py",
)

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / spoken_sources.MANIFEST_RELPATH


def current_manifest() -> dict[str, object]:
    return spoken_sources.load_manifest(MANIFEST_PATH)


def current_sources() -> dict[str, dict[str, object]]:
    failures, sources = spoken_sources.manifest_failures(
        current_manifest(), REPO_ROOT
    )
    if failures:
        raise AssertionError(f"current source manifest is invalid: {failures}")
    return sources


def sn36_surface():
    return next(
        surface
        for surface in spoken_sources.TRANSLATION_SURFACES
        if surface.key == "sn36_6"
    )


class CurrentPilotTests(unittest.TestCase):
    def test_current_manifest_and_reviews_validate(self) -> None:
        self.assertEqual(spoken_sources.collect_failures(), [])

    def test_every_surface_has_current_pilot_metadata(self) -> None:
        sources = current_sources()
        self.assertTrue(spoken_sources.TRANSLATION_SURFACES)

        for surface in spoken_sources.TRANSLATION_SURFACES:
            with self.subTest(surface=surface.key):
                review = surface.spoken_voice_review
                self.assertIsNotNone(review)
                assert review is not None

                self.assertEqual(review.profile, spoken_sources.PROFILE)
                self.assertEqual(review.status, "pilot")
                self.assertTrue(spoken_sources.is_iso_date(review.recorded_on))
                self.assertEqual(
                    review.body_sha256,
                    spoken_sources.translation_body_sha256(surface.main_path),
                )
                self.assertTrue(review.source_ids)
                self.assertTrue(set(review.source_ids).issubset(sources))
                roles = {
                    str(sources[source_id]["role"])
                    for source_id in review.source_ids
                }
                self.assertIn("governance", roles)
                self.assertTrue(
                    roles.intersection(spoken_sources.CALIBRATION_ROLES)
                )


class ManifestValidationTests(unittest.TestCase):
    def test_duplicate_source_ids_are_rejected(self) -> None:
        manifest = copy.deepcopy(current_manifest())
        sources = manifest["sources"]
        assert isinstance(sources, list)
        sources.append(copy.deepcopy(sources[0]))

        failures, _ = spoken_sources.manifest_failures(manifest, REPO_ROOT)

        self.assertTrue(any("duplicate source id" in failure for failure in failures))

    def test_manifest_rejects_committed_transcript_text(self) -> None:
        manifest = copy.deepcopy(current_manifest())
        sources = manifest["sources"]
        assert isinstance(sources, list)
        source = sources[0]
        assert isinstance(source, dict)
        source["transcript"] = "Verbatim source text does not belong here."

        failures, _ = spoken_sources.manifest_failures(manifest, REPO_ROOT)

        self.assertTrue(
            any("`transcript` is forbidden" in failure for failure in failures)
        )

    def test_repo_source_cannot_escape_the_repository(self) -> None:
        manifest = copy.deepcopy(current_manifest())
        sources = manifest["sources"]
        assert isinstance(sources, list)
        source = sources[0]
        assert isinstance(source, dict)
        source["repo_relpath"] = "../outside.md"

        failures, _ = spoken_sources.manifest_failures(manifest, REPO_ROOT)

        self.assertTrue(
            any("repo_relpath escapes the repository" in failure for failure in failures)
        )


class ReviewValidationTests(unittest.TestCase):
    def test_missing_spoken_voice_review_is_rejected(self) -> None:
        changed = replace(sn36_surface(), spoken_voice_review=None)

        failures = spoken_sources.review_failures(
            (changed,), current_sources(), REPO_ROOT
        )

        self.assertTrue(
            any("missing spoken_voice_review" in failure for failure in failures),
            failures,
        )

    def test_unknown_review_source_is_rejected(self) -> None:
        surface = sn36_surface()
        review = surface.spoken_voice_review
        assert review is not None
        changed = replace(
            surface,
            spoken_voice_review=replace(review, source_ids=("MISSING-SOURCE-1",)),
        )

        failures = spoken_sources.review_failures(
            (changed,), current_sources(), REPO_ROOT
        )

        self.assertTrue(
            any("unknown spoken source id `MISSING-SOURCE-1`" in failure for failure in failures)
        )

    def test_review_requires_governance_and_calibration_sources(self) -> None:
        surface = sn36_surface()
        review = surface.spoken_voice_review
        assert review is not None
        cases = (
            (("DH-ARROW-1",), "needs a governance source"),
            (("GOV-PLAIN-1",), "needs a calibration source"),
        )

        for source_ids, expected in cases:
            with self.subTest(source_ids=source_ids):
                changed = replace(
                    surface,
                    spoken_voice_review=replace(review, source_ids=source_ids),
                )
                failures = spoken_sources.review_failures(
                    (changed,), current_sources(), REPO_ROOT
                )
                self.assertTrue(
                    any(expected in failure for failure in failures), failures
                )

    def test_reviewed_body_hash_drift_is_rejected(self) -> None:
        surface = sn36_surface()
        review = surface.spoken_voice_review
        assert review is not None
        changed = replace(
            surface,
            spoken_voice_review=replace(review, body_sha256="0" * 64),
        )

        failures = spoken_sources.review_failures(
            (changed,), current_sources(), REPO_ROOT
        )

        self.assertTrue(
            any("reviewed body hash is stale" in failure for failure in failures)
        )


if __name__ == "__main__":
    unittest.main()
