from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.helpers import load_module


cluster_report = load_module(
    "craving_appropriation_cluster_report",
    "scripts/craving_appropriation_cluster_report.py",
)


def make_record(stem: str, **overrides: object) -> dict[str, object]:
    data: dict[str, object] = {
        "term": stem,
        "normalized_term": stem,
        "entry_type": "major" if stem in cluster_report.HEADWORD_TERMS else "minor",
        "part_of_speech": "phrase" if stem in cluster_report.FORMULA_TERMS else "noun",
        "preferred_translation": f"{stem} translation",
        "alternative_translations": [f"{stem} alt"],
        "discouraged_translations": [f"{stem} discouraged"],
        "definition": f"{stem} definition",
        "notes": f"{stem} note",
        "context_rules": [
            {"context": "default", "rendering": f"{stem} translation", "notes": "default"},
        ],
        "related_terms": [],
        "example_phrases": [{"pali": stem, "translation": f"{stem} translation", "source": "SN 12.2"}],
        "sutta_references": ["SN 12.2"],
        "tags": ["core-doctrine"],
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
    def test_build_report_flags_missing_formula_records(self) -> None:
        terms = {
            stem: make_record(stem)
            for stem in cluster_report.HEADWORD_TERMS + cluster_report.SUPPORTING_TERMS
        }

        report = cluster_report.build_report(terms)

        self.assertIn("nandiraga-sahagata", report["errors"]["missing_formula_records"])

    def test_build_report_warns_on_preferred_rendering_mismatch(self) -> None:
        terms = {
            stem: make_record(stem)
            for stem in cluster_report.HEADWORD_TERMS + cluster_report.SUPPORTING_TERMS + cluster_report.FORMULA_TERMS
        }
        terms["tanha"]["preferred_translation"] = "desire"

        report = cluster_report.build_report(terms)

        self.assertIn("tanha", report["warnings"]["preferred_rendering_mismatches"])

    def test_write_outputs_creates_expected_files(self) -> None:
        terms = {
            stem: make_record(stem)
            for stem in cluster_report.HEADWORD_TERMS + cluster_report.SUPPORTING_TERMS + cluster_report.FORMULA_TERMS
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            with mock.patch.object(cluster_report, "OUTPUT_DIR", output_dir):
                written = cluster_report.write_outputs(terms)

        self.assertEqual(len(written), 2)
        self.assertTrue(any(path.name == "craving-appropriation-cluster-glossary.md" for path in written))

    def test_main_emits_json(self) -> None:
        output = io.StringIO()
        fake_report = {
            "summary": {
                "headwords_present": 1,
                "headwords_expected": 1,
                "supporting_terms_present": 1,
                "supporting_terms_expected": 1,
                "formula_records_present": 1,
                "formula_records_expected": 1,
            },
            "errors": {
                "missing_headwords": [],
                "missing_supporting_terms": [],
                "missing_formula_records": [],
                "cluster_example_source_gaps": [],
            },
            "warnings": {
                "headwords_with_thin_authority_basis": [],
                "preferred_rendering_mismatches": [],
            },
        }

        with mock.patch.object(cluster_report, "load_terms", return_value={}):
            with mock.patch.object(cluster_report, "build_report", return_value=fake_report):
                with mock.patch("sys.argv", ["craving_appropriation_cluster_report.py", "--format", "json"]):
                    with mock.patch("sys.stdout", output):
                        result = cluster_report.main()

        self.assertEqual(result, 0)
        parsed = json.loads(output.getvalue())
        self.assertEqual(parsed["summary"]["formula_records_present"], 1)


if __name__ == "__main__":
    unittest.main()
