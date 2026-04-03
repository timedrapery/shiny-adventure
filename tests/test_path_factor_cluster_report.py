from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.helpers import load_module


cluster_report = load_module(
    "path_factor_cluster_report",
    "scripts/path_factor_cluster_report.py",
)


def make_record(stem: str, **overrides: object) -> dict[str, object]:
    if stem in cluster_report.COLLECTIVE_TERMS:
        data: dict[str, object] = {
            "term": stem,
            "normalized_term": stem,
            "entry_type": "minor",
            "part_of_speech": "compound",
            "preferred_translation": f"{stem} translation",
            "alternative_translations": [f"{stem} alt"],
            "discouraged_translations": [f"{stem} discouraged"],
            "definition": f"{stem} definition",
            "notes": "collective note linking the eight factors into one governed path record",
            "related_terms": ["magga", "samma-ditthi"],
            "example_phrases": [{"pali": stem, "translation": f"{stem} translation", "source": "SN 45.8"}],
            "sutta_references": ["SN 45.8"],
            "tags": ["core-doctrine"],
            "status": "reviewed",
        }
        data.update(overrides)
        return data

    notes_map = {
        "samma-ditthi": "note with right remembering and right effort",
        "samma-sati": "note with right view and right effort that runs circles around the path",
        "samma-vayama": "note with right view and right remembering",
        "magga": "note where right view, right remembering, and right effort run circles around one another",
        "samma-samadhi": "note with first second third fourth jhana and right knowledge plus right release",
        "samma-nana": "note with right mental composure and right release",
        "samma-vimutti": "note with right knowledge",
    }
    note = notes_map.get(stem, f"{stem} note")
    data = {
        "term": stem,
        "normalized_term": stem,
        "entry_type": "major",
        "part_of_speech": "compound" if stem.startswith("samma-") else "noun",
        "preferred_translation": f"{stem} translation",
        "alternative_translations": [f"{stem} alt"],
        "discouraged_translations": [f"{stem} discouraged"],
        "definition": f"{stem} definition",
        "notes": note,
        "context_rules": [
            {"context": "default", "rendering": f"{stem} translation", "notes": "default"},
            {"context": "alt", "rendering": f"{stem} alt", "notes": "alt"},
        ],
        "related_terms": ["related-a", "related-b"],
        "example_phrases": [{"pali": stem, "translation": f"{stem} translation", "source": "MN 117"}],
        "sutta_references": ["MN 117"],
        "tags": ["path-family"],
        "authority_basis": [
            {"source": "source-a", "scope": "scope-a"},
            {"source": "source-b", "scope": "scope-b"},
        ],
        "translation_policy": {
            "default_scope": "default",
            "when_not_to_apply": "never",
            "compound_inheritance": "case-by-case",
            "drift_risk": "avoid drift",
        },
        "status": "reviewed",
    }
    data.update(overrides)
    return data


class PathFactorClusterReportTests(unittest.TestCase):
    def test_build_report_flags_missing_collective_term(self) -> None:
        stems = cluster_report.HEADWORD_TERMS + cluster_report.SUPPORTING_TERMS + cluster_report.COMPLETION_TERMS
        terms = {stem: make_record(stem) for stem in stems}
        for stem, expected in cluster_report.EXPECTED_PREFERRED_TRANSLATIONS.items():
            if stem in terms:
                terms[stem]["preferred_translation"] = expected

        report = cluster_report.build_report(terms)

        self.assertEqual(report["errors"]["missing_collective_terms"], ["ariya-atthangika-magga"])

    def test_build_report_warns_on_preferred_rendering_drift(self) -> None:
        stems = (
            cluster_report.HEADWORD_TERMS
            + cluster_report.SUPPORTING_TERMS
            + cluster_report.COMPLETION_TERMS
            + cluster_report.COLLECTIVE_TERMS
        )
        terms = {stem: make_record(stem) for stem in stems}
        for stem, expected in cluster_report.EXPECTED_PREFERRED_TRANSLATIONS.items():
            terms[stem]["preferred_translation"] = expected
        terms["samma-sati"]["preferred_translation"] = "right mindfulness"
        terms["lokuttara"]["preferred_translation"] = "supramundane"

        report = cluster_report.build_report(terms)

        self.assertTrue(
            any(item.startswith("samma-sati:") for item in report["warnings"]["preferred_rendering_mismatches"])
        )
        self.assertTrue(
            any(item.startswith("lokuttara:") for item in report["warnings"]["preferred_rendering_mismatches"])
        )

    def test_build_report_warns_when_core_loop_identity_missing(self) -> None:
        stems = (
            cluster_report.HEADWORD_TERMS
            + cluster_report.SUPPORTING_TERMS
            + cluster_report.COMPLETION_TERMS
            + cluster_report.COLLECTIVE_TERMS
        )
        terms = {stem: make_record(stem) for stem in stems}
        for stem, expected in cluster_report.EXPECTED_PREFERRED_TRANSLATIONS.items():
            terms[stem]["preferred_translation"] = expected
        terms["magga"]["notes"] = "generic path note"

        report = cluster_report.build_report(terms)

        self.assertEqual(report["warnings"]["core_loop_identity_missing"], ["magga"])

    def test_build_report_warns_when_completion_identity_missing(self) -> None:
        stems = (
            cluster_report.HEADWORD_TERMS
            + cluster_report.SUPPORTING_TERMS
            + cluster_report.COMPLETION_TERMS
            + cluster_report.COLLECTIVE_TERMS
        )
        terms = {stem: make_record(stem) for stem in stems}
        for stem, expected in cluster_report.EXPECTED_PREFERRED_TRANSLATIONS.items():
            terms[stem]["preferred_translation"] = expected
        terms["samma-samadhi"]["notes"] = "generic composure note"

        report = cluster_report.build_report(terms)

        self.assertEqual(report["warnings"]["tenfold_completion_identity_missing"], ["samma-samadhi"])

    def test_build_report_warns_on_thin_collective_term(self) -> None:
        stems = (
            cluster_report.HEADWORD_TERMS
            + cluster_report.SUPPORTING_TERMS
            + cluster_report.COMPLETION_TERMS
            + cluster_report.COLLECTIVE_TERMS
        )
        terms = {stem: make_record(stem) for stem in stems}
        for stem, expected in cluster_report.EXPECTED_PREFERRED_TRANSLATIONS.items():
            terms[stem]["preferred_translation"] = expected
        terms["ariya-atthangika-magga"].pop("notes")

        report = cluster_report.build_report(terms)

        self.assertEqual(report["warnings"]["collective_terms_still_thin"], ["ariya-atthangika-magga"])

    def test_write_outputs_creates_expected_files(self) -> None:
        stems = (
            cluster_report.HEADWORD_TERMS
            + cluster_report.SUPPORTING_TERMS
            + cluster_report.COMPLETION_TERMS
            + cluster_report.COLLECTIVE_TERMS
        )
        terms = {stem: make_record(stem) for stem in stems}
        for stem, expected in cluster_report.EXPECTED_PREFERRED_TRANSLATIONS.items():
            terms[stem]["preferred_translation"] = expected

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            with mock.patch.object(cluster_report, "OUTPUT_DIR", output_dir):
                written = cluster_report.write_outputs(terms)

        self.assertEqual(len(written), 4)
        self.assertTrue(any(path.name == "path-factor-tenfold-sequence-sheet.md" for path in written))

    def test_live_cluster_has_no_warnings(self) -> None:
        report = cluster_report.build_report(cluster_report.load_terms())

        self.assertEqual(report["errors"]["missing_headwords"], [])
        self.assertEqual(report["errors"]["missing_supporting_terms"], [])
        self.assertEqual(report["errors"]["missing_completion_terms"], [])
        self.assertEqual(report["errors"]["missing_collective_terms"], [])
        self.assertEqual(report["errors"]["cluster_example_source_gaps"], [])
        self.assertEqual(report["warnings"]["headwords_with_thin_authority_basis"], [])
        self.assertEqual(report["warnings"]["collective_terms_still_thin"], [])
        self.assertEqual(report["warnings"]["preferred_rendering_mismatches"], [])
        self.assertEqual(report["warnings"]["core_loop_identity_missing"], [])
        self.assertEqual(report["warnings"]["tenfold_completion_identity_missing"], [])

    def test_main_emits_json(self) -> None:
        output = io.StringIO()
        fake_report = {
            "summary": {
                "headwords_present": 1,
                "headwords_expected": 1,
                "supporting_terms_present": 1,
                "supporting_terms_expected": 1,
                "completion_terms_present": 1,
                "completion_terms_expected": 1,
                "collective_terms_present": 1,
                "collective_terms_expected": 1,
            },
            "errors": {
                "missing_headwords": [],
                "missing_supporting_terms": [],
                "missing_completion_terms": [],
                "missing_collective_terms": [],
                "cluster_example_source_gaps": [],
            },
            "warnings": {
                "headwords_with_thin_authority_basis": [],
                "collective_terms_still_thin": [],
                "preferred_rendering_mismatches": [],
                "core_loop_identity_missing": [],
                "tenfold_completion_identity_missing": [],
            },
        }

        with mock.patch.object(cluster_report, "load_terms", return_value={}):
            with mock.patch.object(cluster_report, "build_report", return_value=fake_report):
                with mock.patch("sys.argv", ["path_factor_cluster_report.py", "--format", "json"]):
                    with mock.patch("sys.stdout", output):
                        result = cluster_report.main()

        self.assertEqual(result, 0)
        parsed = json.loads(output.getvalue())
        self.assertEqual(parsed["summary"]["collective_terms_present"], 1)


if __name__ == "__main__":
    unittest.main()
