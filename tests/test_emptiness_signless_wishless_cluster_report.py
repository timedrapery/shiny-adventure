from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.helpers import load_module


cluster_report = load_module(
    "emptiness_signless_wishless_cluster_report",
    "scripts/emptiness_signless_wishless_cluster_report.py",
)


def make_record(stem: str, **overrides: object) -> dict[str, object]:
    data: dict[str, object] = {
        "term": stem,
        "normalized_term": stem,
        "entry_type": "major" if stem in cluster_report.HEADWORD_TERMS else "minor",
        "part_of_speech": "noun",
        "preferred_translation": f"{stem} translation",
        "alternative_translations": [f"{stem} alt"],
        "discouraged_translations": [f"{stem} discouraged"],
        "definition": f"{stem} definition",
        "notes": f"{stem} note",
        "context_rules": [
            {"context": "default", "rendering": f"{stem} translation", "notes": "default"},
        ],
        "related_terms": [],
        "authority_basis": [
            {"source": "source-a", "scope": "scope-a"},
            {"source": "source-b", "scope": "scope-b"},
        ],
        "translation_policy": {
            "default_scope": "default",
            "when_not_to_apply": "never",
            "compound_inheritance": "inherit",
            "drift_risk": "avoid drift",
        },
        "status": "stable" if stem in cluster_report.HEADWORD_TERMS else "reviewed",
    }
    data.update(overrides)
    return data


class EmptinessSignlessWishlessClusterReportTests(unittest.TestCase):
    def test_build_report_flags_missing_headwords(self) -> None:
        terms = {stem: make_record(stem) for stem in cluster_report.SUPPORTING_TERMS}

        report = cluster_report.build_report(terms)

        self.assertIn("sunnata", report["errors"]["missing_headwords"])

    def test_build_report_flags_non_major_or_unstable_headwords(self) -> None:
        terms = {
            stem: make_record(stem)
            for stem in cluster_report.HEADWORD_TERMS + cluster_report.SUPPORTING_TERMS
        }
        terms["animitta"]["entry_type"] = "minor"

        report = cluster_report.build_report(terms)

        self.assertIn("animitta", report["errors"]["unstable_or_non_major_headwords"])

    def test_write_outputs_creates_expected_files(self) -> None:
        terms = {
            stem: make_record(stem)
            for stem in cluster_report.HEADWORD_TERMS + cluster_report.SUPPORTING_TERMS
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            with mock.patch.object(cluster_report, "OUTPUT_DIR", output_dir):
                written = cluster_report.write_outputs(terms)

        self.assertEqual(len(written), 2)
        self.assertTrue(any(path.name == "emptiness-signless-wishless-glossary.md" for path in written))

    def test_render_contrast_sheet_mentions_anatta_and_vimutti(self) -> None:
        terms = {
            stem: make_record(stem)
            for stem in cluster_report.HEADWORD_TERMS + cluster_report.SUPPORTING_TERMS
        }

        sheet = cluster_report.render_contrast_sheet(terms)

        self.assertIn("anattā", sheet)
        self.assertIn("vimutti", sheet)

    def test_main_emits_json(self) -> None:
        output = io.StringIO()
        fake_report = {
            "summary": {
                "headwords_present": 3,
                "headwords_expected": 3,
                "supporting_terms_present": 10,
                "supporting_terms_expected": 10,
                "formula_records_present": 0,
                "formula_records_expected": 0,
            },
            "errors": {
                "missing_headwords": [],
                "missing_supporting_terms": [],
                "unstable_or_non_major_headwords": [],
            },
            "warnings": {
                "headwords_with_thin_authority_basis": [],
                "preferred_rendering_mismatches": [],
            },
        }

        with mock.patch.object(cluster_report, "load_terms", return_value={}):
            with mock.patch.object(cluster_report, "build_report", return_value=fake_report):
                with mock.patch("sys.argv", ["emptiness_signless_wishless_cluster_report.py", "--format", "json"]):
                    with mock.patch("sys.stdout", output):
                        result = cluster_report.main()

        self.assertEqual(result, 0)
        parsed = json.loads(output.getvalue())
        self.assertEqual(parsed["summary"]["supporting_terms_present"], 10)


if __name__ == "__main__":
    unittest.main()
