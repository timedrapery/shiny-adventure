from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.helpers import load_module


cluster_report = load_module("verbal_knowing_cluster_report", "scripts/verbal_knowing_cluster_report.py")


def make_record(stem: str, **overrides: object) -> dict[str, object]:
    data: dict[str, object] = {
        "term": stem,
        "normalized_term": stem,
        "entry_type": "major" if stem in cluster_report.HEADWORD_TERMS else "minor",
        "part_of_speech": "verb",
        "preferred_translation": f"{stem} translation",
        "alternative_translations": [f"{stem} alt"],
        "discouraged_translations": [f"{stem} discouraged"],
        "definition": f"{stem} definition",
        "notes": f"{stem} note",
        "context_rules": [
            {"context": "default", "rendering": f"{stem} translation", "notes": "default"},
        ],
        "related_terms": [],
        "example_phrases": [{"pali": stem, "translation": f"{stem} translation", "source": "MN 1"}],
        "sutta_references": ["MN 1"],
        "tags": ["verbal-knowing-cluster"],
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


class VerbalKnowingClusterReportTests(unittest.TestCase):
    def test_build_report_flags_missing_headwords(self) -> None:
        terms = {stem: make_record(stem) for stem in cluster_report.SUPPORTING_TERMS + cluster_report.FORMULA_TERMS}

        report = cluster_report.build_report(terms)

        self.assertIn("janati", report["errors"]["missing_headwords"])

    def test_build_report_warns_on_preferred_rendering_mismatch(self) -> None:
        terms = {
            stem: make_record(stem)
            for stem in cluster_report.HEADWORD_TERMS + cluster_report.SUPPORTING_TERMS + cluster_report.FORMULA_TERMS
        }
        terms["janati"]["preferred_translation"] = "understands"

        report = cluster_report.build_report(terms)

        self.assertIn("janati", report["warnings"]["preferred_rendering_mismatches"])

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
        self.assertTrue(any(path.name == "verbal-knowing-cluster-glossary.md" for path in written))

    def test_render_contrast_sheet_mentions_recognition_selfing_and_sanna(self) -> None:
        terms = {
            stem: make_record(stem)
            for stem in cluster_report.HEADWORD_TERMS + cluster_report.SUPPORTING_TERMS + cluster_report.FORMULA_TERMS
        }

        sheet = cluster_report.render_contrast_sheet(terms)

        self.assertIn("recognition", sheet)
        self.assertIn("proliferation", sheet)
        self.assertIn("selfing", sheet)
        self.assertIn("sanna", sheet)

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
                with mock.patch("sys.argv", ["verbal_knowing_cluster_report.py", "--format", "json"]):
                    with mock.patch("sys.stdout", output):
                        result = cluster_report.main()

        self.assertEqual(result, 0)
        parsed = json.loads(output.getvalue())
        self.assertEqual(parsed["summary"]["formula_records_present"], 1)


if __name__ == "__main__":
    unittest.main()
