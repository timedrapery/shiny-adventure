from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.helpers import load_module


cluster_report = load_module(
    "jhana_cluster_report",
    "scripts/jhana_cluster_report.py",
)


def make_record(stem: str, **overrides: object) -> dict[str, object]:
    data: dict[str, object] = {
        "term": stem,
        "normalized_term": stem,
        "entry_type": "major" if stem in cluster_report.HEADWORD_TERMS else "minor",
        "part_of_speech": "verb" if stem == "jhayati" else "noun",
        "preferred_translation": f"{stem} translation",
        "alternative_translations": [f"{stem} alt"],
        "discouraged_translations": [f"{stem} discouraged"],
        "definition": f"{stem} definition",
        "notes": f"{stem} note mentioning source-a and source-b plus first second third fourth jhana where needed",
        "context_rules": [
            {"context": "default", "rendering": f"{stem} translation", "notes": "default"},
            {"context": "alt", "rendering": f"{stem} alt", "notes": "alt"},
        ],
        "related_terms": [],
        "example_phrases": [{"pali": stem, "translation": f"{stem} translation", "source": "DN 2"}],
        "sutta_references": ["DN 2"],
        "tags": ["jhana-factors"],
        "authority_basis": [
            {"source": "source-a", "scope": "scope-a"},
            {"source": "source-b", "scope": "scope-b"},
        ],
        "translation_policy": {
            "default_scope": "default",
            "when_not_to_apply": "never",
            "compound_inheritance": "blocked",
            "drift_risk": "avoid drift",
        },
        "status": "reviewed",
    }
    data.update(overrides)
    return data


class ClusterReportTests(unittest.TestCase):
    def test_build_report_flags_missing_sequence_terms(self) -> None:
        terms = {
            stem: make_record(stem)
            for stem in cluster_report.HEADWORD_TERMS + cluster_report.FORMULA_TERMS
        }

        report = cluster_report.build_report(terms)

        self.assertIn(
            "pathama-jhana",
            report["errors"]["missing_sequence_terms"],
        )

    def test_build_report_warns_on_preferred_rendering_drift(self) -> None:
        terms = {
            stem: make_record(stem)
            for stem in cluster_report.HEADWORD_TERMS + cluster_report.SEQUENCE_TERMS + cluster_report.FORMULA_TERMS
        }
        terms["jhana"]["preferred_translation"] = "theme"
        terms["jhayati"]["preferred_translation"] = "meditate"

        report = cluster_report.build_report(terms)

        self.assertTrue(
            any(item.startswith("jhana:") for item in report["warnings"]["preferred_rendering_mismatches"])
        )
        self.assertTrue(
            any(item.startswith("jhayati:") for item in report["warnings"]["preferred_rendering_mismatches"])
        )

    def test_build_report_warns_when_samma_samadhi_identity_missing(self) -> None:
        terms = {
            stem: make_record(stem)
            for stem in cluster_report.HEADWORD_TERMS + cluster_report.SEQUENCE_TERMS + cluster_report.FORMULA_TERMS
        }
        terms["samma-samadhi"] = make_record(
            "samma-samadhi",
            preferred_translation="right mental composure",
            notes="generic path-factor note",
            definition="generic path-factor definition",
        )

        report = cluster_report.build_report(terms)

        self.assertEqual(
            report["warnings"]["samma_samadhi_identity_missing"],
            ["samma-samadhi"],
        )

    def test_write_outputs_creates_expected_files(self) -> None:
        terms = {
            stem: make_record(stem)
            for stem in cluster_report.HEADWORD_TERMS + cluster_report.SEQUENCE_TERMS + cluster_report.FORMULA_TERMS
        }
        for stem, expected in cluster_report.EXPECTED_PREFERRED_TRANSLATIONS.items():
            terms[stem]["preferred_translation"] = expected
        terms["samma-samadhi"]["notes"] = "first second third fourth jhana"

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            with mock.patch.object(cluster_report, "OUTPUT_DIR", output_dir):
                written = cluster_report.write_outputs(terms)

        self.assertEqual(len(written), 4)
        self.assertTrue(any(path.name == "jhana-formula-sheet.md" for path in written))

    def test_live_cluster_has_no_warnings(self) -> None:
        report = cluster_report.build_report(cluster_report.load_terms())

        self.assertEqual(report["warnings"]["headwords_with_thin_authority_basis"], [])
        self.assertEqual(report["warnings"]["sequence_terms_still_thin"], [])
        self.assertEqual(report["warnings"]["formula_terms_still_thin"], [])
        self.assertEqual(report["warnings"]["preferred_rendering_mismatches"], [])
        self.assertEqual(report["warnings"]["samma_samadhi_identity_missing"], [])

    def test_main_emits_json(self) -> None:
        output = io.StringIO()
        fake_report = {
            "summary": {
                "headwords_present": 1,
                "headwords_expected": 1,
                "sequence_terms_present": 1,
                "sequence_terms_expected": 1,
                "formula_terms_present": 1,
                "formula_terms_expected": 1,
            },
            "errors": {
                "missing_headwords": [],
                "missing_sequence_terms": [],
                "missing_formula_terms": [],
                "cluster_example_source_gaps": [],
            },
            "warnings": {
                "headwords_with_thin_authority_basis": [],
                "sequence_terms_still_thin": [],
                "formula_terms_still_thin": [],
                "preferred_rendering_mismatches": [],
                "samma_samadhi_identity_missing": [],
            },
        }

        with mock.patch.object(cluster_report, "load_terms", return_value={}):
            with mock.patch.object(cluster_report, "build_report", return_value=fake_report):
                with mock.patch("sys.argv", ["jhana_cluster_report.py", "--format", "json"]):
                    with mock.patch("sys.stdout", output):
                        result = cluster_report.main()

        self.assertEqual(result, 0)
        parsed = json.loads(output.getvalue())
        self.assertEqual(parsed["summary"]["formula_terms_present"], 1)


if __name__ == "__main__":
    unittest.main()
