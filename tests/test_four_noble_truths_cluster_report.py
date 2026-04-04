from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.helpers import load_module


cluster_report = load_module(
    "four_noble_truths_cluster_report",
    "scripts/four_noble_truths_cluster_report.py",
)


def make_record(stem: str, **overrides: object) -> dict[str, object]:
    if stem in cluster_report.TRUTH_RECORDS:
        data: dict[str, object] = {
            "term": stem,
            "normalized_term": stem,
            "entry_type": "minor",
            "part_of_speech": "compound",
            "preferred_translation": f"{stem} translation",
            "alternative_translations": [f"{stem} alt"],
            "discouraged_translations": [f"{stem} discouraged"],
            "definition": f"{stem} definition",
            "notes": "truth-record note tying the formula back to the governed truth family",
            "related_terms": ["ariyasacca", "dukkha"],
            "example_phrases": [{"pali": stem, "translation": f"{stem} translation", "source": "SN 56.11"}],
            "sutta_references": ["SN 56.11"],
            "tags": ["four-noble-truths"],
            "status": "reviewed",
        }
        data.update(overrides)
        return data

    notes_map = {
        "ariyasacca": "correct noble practice wake up wholesome change quenching SN 22.86 dukkha / dukkha-nirodha scope",
        "dukkha": "SN 22.86 only dissatisfaction and the ending of dissatisfaction waking up what is here",
        "samudaya": "note about where it is heading",
        "nirodha": "SN 22.86 note about congratulating oneself",
        "magga": "note about making a wholesome change",
        "sati": "note about again as often as one can remember",
        "patipada": "path of practice note",
    }
    data = {
        "term": stem,
        "normalized_term": stem,
        "entry_type": "major",
        "part_of_speech": "compound" if stem == "ariyasacca" else "noun",
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
        "example_phrases": [{"pali": stem, "translation": f"{stem} translation", "source": "SN 56.11"}],
        "sutta_references": ["SN 56.11"],
        "tags": ["four-noble-truths"],
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


class FourNobleTruthsClusterReportTests(unittest.TestCase):
    def test_build_report_flags_missing_truth_records(self) -> None:
        stems = cluster_report.HEADWORD_TERMS + cluster_report.SUPPORTING_TERMS
        terms = {stem: make_record(stem) for stem in stems}
        for stem, expected in cluster_report.EXPECTED_PREFERRED_TRANSLATIONS.items():
            if stem in terms:
                terms[stem]["preferred_translation"] = expected

        report = cluster_report.build_report(terms)

        self.assertIn("dukkha-ariyasacca", report["errors"]["missing_truth_records"])

    def test_build_report_warns_on_preferred_rendering_drift(self) -> None:
        stems = (
            cluster_report.HEADWORD_TERMS
            + cluster_report.SUPPORTING_TERMS
            + cluster_report.TRUTH_RECORDS
        )
        terms = {stem: make_record(stem) for stem in stems}
        for stem, expected in cluster_report.EXPECTED_PREFERRED_TRANSLATIONS.items():
            terms[stem]["preferred_translation"] = expected
        terms["samudaya-ariyasacca"]["preferred_translation"] = "noble truth of arising"

        report = cluster_report.build_report(terms)

        self.assertTrue(
            any(item.startswith("samudaya-ariyasacca:") for item in report["warnings"]["preferred_rendering_mismatches"])
        )

    def test_build_report_warns_when_practical_cycle_mapping_missing(self) -> None:
        stems = (
            cluster_report.HEADWORD_TERMS
            + cluster_report.SUPPORTING_TERMS
            + cluster_report.TRUTH_RECORDS
        )
        terms = {stem: make_record(stem) for stem in stems}
        for stem, expected in cluster_report.EXPECTED_PREFERRED_TRANSLATIONS.items():
            terms[stem]["preferred_translation"] = expected
        terms["samudaya"]["notes"] = "generic origin note"

        report = cluster_report.build_report(terms)

        self.assertEqual(report["warnings"]["practical_cycle_mapping_missing"], ["samudaya"])

    def test_build_report_warns_when_scope_rule_missing(self) -> None:
        stems = (
            cluster_report.HEADWORD_TERMS
            + cluster_report.SUPPORTING_TERMS
            + cluster_report.TRUTH_RECORDS
        )
        terms = {stem: make_record(stem) for stem in stems}
        for stem, expected in cluster_report.EXPECTED_PREFERRED_TRANSLATIONS.items():
            terms[stem]["preferred_translation"] = expected
        terms["ariyasacca"]["notes"] = "generic truths note"

        report = cluster_report.build_report(terms)

        self.assertEqual(report["warnings"]["dukkha_nirodha_scope_missing"], ["ariyasacca"])

    def test_write_outputs_creates_expected_files(self) -> None:
        stems = (
            cluster_report.HEADWORD_TERMS
            + cluster_report.SUPPORTING_TERMS
            + cluster_report.TRUTH_RECORDS
        )
        terms = {stem: make_record(stem) for stem in stems}
        for stem, expected in cluster_report.EXPECTED_PREFERRED_TRANSLATIONS.items():
            terms[stem]["preferred_translation"] = expected

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            with mock.patch.object(cluster_report, "OUTPUT_DIR", output_dir):
                written = cluster_report.write_outputs(terms)

        self.assertEqual(len(written), 4)
        self.assertTrue(any(path.name == "four-noble-truths-truth-task-sheet.md" for path in written))

    def test_live_cluster_has_no_warnings(self) -> None:
        report = cluster_report.build_report(cluster_report.load_terms())

        self.assertEqual(report["errors"]["missing_headwords"], [])
        self.assertEqual(report["errors"]["missing_supporting_terms"], [])
        self.assertEqual(report["errors"]["missing_truth_records"], [])
        self.assertEqual(report["errors"]["cluster_example_source_gaps"], [])
        self.assertEqual(report["warnings"]["headwords_with_thin_authority_basis"], [])
        self.assertEqual(report["warnings"]["truth_records_still_thin"], [])
        self.assertEqual(report["warnings"]["preferred_rendering_mismatches"], [])
        self.assertEqual(report["warnings"]["practical_cycle_mapping_missing"], [])
        self.assertEqual(report["warnings"]["dukkha_nirodha_scope_missing"], [])

    def test_main_emits_json(self) -> None:
        output = io.StringIO()
        fake_report = {
            "summary": {
                "headwords_present": 1,
                "headwords_expected": 1,
                "supporting_terms_present": 1,
                "supporting_terms_expected": 1,
                "truth_records_present": 1,
                "truth_records_expected": 1,
            },
            "errors": {
                "missing_headwords": [],
                "missing_supporting_terms": [],
                "missing_truth_records": [],
                "cluster_example_source_gaps": [],
            },
            "warnings": {
                "headwords_with_thin_authority_basis": [],
                "truth_records_still_thin": [],
                "preferred_rendering_mismatches": [],
                "practical_cycle_mapping_missing": [],
                "dukkha_nirodha_scope_missing": [],
            },
        }

        with mock.patch.object(cluster_report, "load_terms", return_value={}):
            with mock.patch.object(cluster_report, "build_report", return_value=fake_report):
                with mock.patch("sys.argv", ["four_noble_truths_cluster_report.py", "--format", "json"]):
                    with mock.patch("sys.stdout", output):
                        result = cluster_report.main()

        self.assertEqual(result, 0)
        parsed = json.loads(output.getvalue())
        self.assertEqual(parsed["summary"]["truth_records_present"], 1)


if __name__ == "__main__":
    unittest.main()
