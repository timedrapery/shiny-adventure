from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.helpers import load_module


cluster_report = load_module(
    "three_marks_cluster_report",
    "scripts/three_marks_cluster_report.py",
)


def make_record(stem: str, **overrides: object) -> dict[str, object]:
    if stem in cluster_report.FORMULA_TERMS:
        notes_map = {
            "anicca-sabbe-sankhara": "formula note keeping impermanent and put together linked",
            "dukkha-sabbe-sankhara": "formula note keeping unsatisfactory and put together linked",
            "sabbe-dhamma-anatta": "formula note keeping phenomena and not-self linked",
            "sabbe-sankhata-anicca": "formula note keeping conditioned things and impermanent linked",
            "yam-aniccam-tam-dukkham-yam-dukkham-tad-anatta": (
                "formula note keeping impermanent dissatisfaction and not-self linked"
            ),
        }
        data: dict[str, object] = {
            "term": stem,
            "normalized_term": stem,
            "entry_type": "minor",
            "part_of_speech": "phrase",
            "preferred_translation": f"{stem} translation",
            "alternative_translations": [f"{stem} alt"],
            "discouraged_translations": [f"{stem} discouraged"],
            "definition": f"{stem} definition",
            "notes": notes_map[stem],
            "related_terms": ["anicca", "dukkha", "anatta"],
            "example_phrases": [{"pali": stem, "translation": f"{stem} translation", "source": "Dhp 277"}],
            "sutta_references": ["Dhp 277"],
            "tags": ["three-marks", "formula"],
            "status": "reviewed",
        }
        data.update(overrides)
        return data

    notes_map = {
        "anicca": "three marks framework note linking impermanent and dissatisfaction",
        "dukkha": "dissatisfaction note linking the family without restoring suffering",
        "anatta": "note keeping not-self tied to what is impermanent is dissatisfaction",
        "sankhara": "three-marks formulae note keeping that which has been put together visible",
        "sankhata": "conditioned note linking the family to impermanent",
        "dhamma": "phenomenon note explaining analytic contexts",
        "anicca-sanna": "practice note linking impermanence and dissatisfaction",
        "dukkha-sanna": "practice note linking dissatisfaction and not-self",
        "anatta-sanna": "practice note linking not-self and de-appropriation",
        "aniccanupassana": "practice note keeping impermanence explicit",
        "dukkhanupassana": "practice note keeping dissatisfaction explicit",
        "anattanupassana": "practice note keeping not-self explicit",
    }
    data = {
        "term": stem,
        "normalized_term": stem,
        "entry_type": "major" if stem in cluster_report.HEADWORD_TERMS + cluster_report.SUPPORTING_TERMS else "minor",
        "part_of_speech": "noun",
        "preferred_translation": f"{stem} translation",
        "alternative_translations": [f"{stem} alt"],
        "discouraged_translations": [f"{stem} discouraged"],
        "definition": f"{stem} definition",
        "notes": notes_map.get(stem, f"{stem} note"),
        "context_rules": [
            {"context": "default", "rendering": f"{stem} translation", "notes": "default"},
            {"context": "alt", "rendering": f"{stem} alt", "notes": "alt"},
        ],
        "related_terms": ["related-a", "related-b"],
        "example_phrases": [{"pali": stem, "translation": f"{stem} translation", "source": "SN 22.59"}],
        "sutta_references": ["SN 22.59"],
        "tags": ["three-marks"],
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


class ThreeMarksClusterReportTests(unittest.TestCase):
    def test_build_report_flags_missing_formula_terms(self) -> None:
        stems = (
            cluster_report.HEADWORD_TERMS
            + cluster_report.SUPPORTING_TERMS
            + cluster_report.PRACTICE_TERMS
        )
        terms = {stem: make_record(stem) for stem in stems}
        for stem, expected in cluster_report.EXPECTED_PREFERRED_TRANSLATIONS.items():
            if stem in terms:
                terms[stem]["preferred_translation"] = expected

        report = cluster_report.build_report(terms)

        self.assertIn("anicca-sabbe-sankhara", report["errors"]["missing_formula_terms"])

    def test_build_report_warns_on_preferred_rendering_drift(self) -> None:
        stems = (
            cluster_report.HEADWORD_TERMS
            + cluster_report.SUPPORTING_TERMS
            + cluster_report.PRACTICE_TERMS
            + cluster_report.FORMULA_TERMS
        )
        terms = {stem: make_record(stem) for stem in stems}
        for stem, expected in cluster_report.EXPECTED_PREFERRED_TRANSLATIONS.items():
            terms[stem]["preferred_translation"] = expected
        terms["sabbe-dhamma-anatta"]["preferred_translation"] = "all dhammas are not-self"

        report = cluster_report.build_report(terms)

        self.assertTrue(
            any(item.startswith("sabbe-dhamma-anatta:") for item in report["warnings"]["preferred_rendering_mismatches"])
        )

    def test_build_report_warns_when_formula_override_identity_missing(self) -> None:
        stems = (
            cluster_report.HEADWORD_TERMS
            + cluster_report.SUPPORTING_TERMS
            + cluster_report.PRACTICE_TERMS
            + cluster_report.FORMULA_TERMS
        )
        terms = {stem: make_record(stem) for stem in stems}
        for stem, expected in cluster_report.EXPECTED_PREFERRED_TRANSLATIONS.items():
            terms[stem]["preferred_translation"] = expected
        terms["dhamma"]["notes"] = "generic dhamma note"

        report = cluster_report.build_report(terms)

        self.assertEqual(report["warnings"]["formula_override_identity_missing"], ["dhamma"])

    def test_write_outputs_creates_expected_files(self) -> None:
        stems = (
            cluster_report.HEADWORD_TERMS
            + cluster_report.SUPPORTING_TERMS
            + cluster_report.PRACTICE_TERMS
            + cluster_report.FORMULA_TERMS
        )
        terms = {stem: make_record(stem) for stem in stems}
        for stem, expected in cluster_report.EXPECTED_PREFERRED_TRANSLATIONS.items():
            terms[stem]["preferred_translation"] = expected

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            with mock.patch.object(cluster_report, "OUTPUT_DIR", output_dir):
                written = cluster_report.write_outputs(terms)

        self.assertEqual(len(written), 4)
        self.assertTrue(any(path.name == "three-marks-formula-sheet.md" for path in written))

    def test_live_cluster_has_no_warnings(self) -> None:
        report = cluster_report.build_report(cluster_report.load_terms())

        self.assertEqual(report["errors"]["missing_headwords"], [])
        self.assertEqual(report["errors"]["missing_supporting_terms"], [])
        self.assertEqual(report["errors"]["missing_practice_terms"], [])
        self.assertEqual(report["errors"]["missing_formula_terms"], [])
        self.assertEqual(report["errors"]["cluster_example_source_gaps"], [])
        self.assertEqual(report["warnings"]["headwords_with_thin_authority_basis"], [])
        self.assertEqual(report["warnings"]["practice_terms_still_thin"], [])
        self.assertEqual(report["warnings"]["formula_terms_still_thin"], [])
        self.assertEqual(report["warnings"]["preferred_rendering_mismatches"], [])
        self.assertEqual(report["warnings"]["formula_override_identity_missing"], [])

    def test_main_emits_json(self) -> None:
        output = io.StringIO()
        fake_report = {
            "summary": {
                "headwords_present": 1,
                "headwords_expected": 1,
                "supporting_terms_present": 1,
                "supporting_terms_expected": 1,
                "practice_terms_present": 1,
                "practice_terms_expected": 1,
                "formula_terms_present": 1,
                "formula_terms_expected": 1,
            },
            "errors": {
                "missing_headwords": [],
                "missing_supporting_terms": [],
                "missing_practice_terms": [],
                "missing_formula_terms": [],
                "cluster_example_source_gaps": [],
            },
            "warnings": {
                "headwords_with_thin_authority_basis": [],
                "practice_terms_still_thin": [],
                "formula_terms_still_thin": [],
                "preferred_rendering_mismatches": [],
                "formula_override_identity_missing": [],
            },
        }

        with mock.patch.object(cluster_report, "load_terms", return_value={}):
            with mock.patch.object(cluster_report, "build_report", return_value=fake_report):
                with mock.patch("sys.argv", ["three_marks_cluster_report.py", "--format", "json"]):
                    with mock.patch("sys.stdout", output):
                        result = cluster_report.main()

        self.assertEqual(result, 0)
        parsed = json.loads(output.getvalue())
        self.assertEqual(parsed["summary"]["formula_terms_present"], 1)


if __name__ == "__main__":
    unittest.main()
