from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.helpers import load_module


cluster_report = load_module(
    "sense_fields_cluster_report",
    "scripts/sense_fields_cluster_report.py",
)


def make_record(stem: str, **overrides: object) -> dict[str, object]:
    if stem in cluster_report.FIELD_TERMS or stem in cluster_report.CONTACT_TERMS or stem in cluster_report.FORMULA_TERMS:
        notes_map = {
            "namarupapaccaya-salayatanam": "note with six fields of experience",
            "salayatanapaccaya-phasso": "note with six fields of experience and contact",
            "phassapaccaya-vedana": "note with contact and felt experience",
        }
        data: dict[str, object] = {
            "term": stem,
            "normalized_term": stem,
            "entry_type": "minor",
            "part_of_speech": "phrase" if stem in cluster_report.FORMULA_TERMS else "compound",
            "preferred_translation": f"{stem} translation",
            "alternative_translations": [f"{stem} alt"],
            "discouraged_translations": [f"{stem} discouraged"],
            "definition": f"{stem} definition",
            "notes": notes_map.get(stem, f"{stem} note"),
            "related_terms": ["related-a", "related-b"],
            "example_phrases": [{"pali": stem, "translation": f"{stem} translation", "source": "MN 148"}],
            "sutta_references": ["MN 148"],
            "tags": ["sense-fields"],
            "status": "reviewed",
        }
        data.update(overrides)
        return data

    notes_map = {
        "ayatana": "field note with sense field",
        "salayatana": "note with contact",
        "phassa": "note with sense field and earliest practical pivot",
    }
    data = {
        "term": stem,
        "normalized_term": stem,
        "entry_type": "major",
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
        "example_phrases": [{"pali": stem, "translation": f"{stem} translation", "source": "MN 148"}],
        "sutta_references": ["MN 148"],
        "tags": ["sense-fields"],
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


class SenseFieldsClusterReportTests(unittest.TestCase):
    def test_build_report_flags_missing_field_terms(self) -> None:
        stems = cluster_report.HEADWORD_TERMS + cluster_report.CONTACT_TERMS + cluster_report.FORMULA_TERMS
        terms = {stem: make_record(stem) for stem in stems}
        for stem, expected in cluster_report.EXPECTED_PREFERRED_TRANSLATIONS.items():
            if stem in terms:
                terms[stem]["preferred_translation"] = expected

        report = cluster_report.build_report(terms)

        self.assertIn("cakkhayatana", report["errors"]["missing_field_terms"])

    def test_build_report_warns_on_preferred_rendering_drift(self) -> None:
        stems = (
            cluster_report.HEADWORD_TERMS
            + cluster_report.FIELD_TERMS
            + cluster_report.CONTACT_TERMS
            + cluster_report.FORMULA_TERMS
        )
        terms = {stem: make_record(stem) for stem in stems}
        for stem, expected in cluster_report.EXPECTED_PREFERRED_TRANSLATIONS.items():
            terms[stem]["preferred_translation"] = expected
        terms["cakkhayatana"]["preferred_translation"] = "eye base"

        report = cluster_report.build_report(terms)

        self.assertTrue(
            any(item.startswith("cakkhayatana:") for item in report["warnings"]["preferred_rendering_mismatches"])
        )

    def test_build_report_warns_when_contact_chain_identity_missing(self) -> None:
        stems = (
            cluster_report.HEADWORD_TERMS
            + cluster_report.FIELD_TERMS
            + cluster_report.CONTACT_TERMS
            + cluster_report.FORMULA_TERMS
        )
        terms = {stem: make_record(stem) for stem in stems}
        for stem, expected in cluster_report.EXPECTED_PREFERRED_TRANSLATIONS.items():
            terms[stem]["preferred_translation"] = expected
        terms["phassa"]["notes"] = "generic phassa note"

        report = cluster_report.build_report(terms)

        self.assertEqual(report["warnings"]["contact_chain_identity_missing"], ["phassa"])

    def test_write_outputs_creates_expected_files(self) -> None:
        stems = (
            cluster_report.HEADWORD_TERMS
            + cluster_report.FIELD_TERMS
            + cluster_report.CONTACT_TERMS
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
        self.assertTrue(any(path.name == "sense-fields-twelve-field-map.md" for path in written))

    def test_live_cluster_has_no_warnings(self) -> None:
        report = cluster_report.build_report(cluster_report.load_terms())

        self.assertEqual(report["errors"]["missing_headwords"], [])
        self.assertEqual(report["errors"]["missing_field_terms"], [])
        self.assertEqual(report["errors"]["missing_contact_terms"], [])
        self.assertEqual(report["errors"]["missing_formula_terms"], [])
        self.assertEqual(report["errors"]["cluster_example_source_gaps"], [])
        self.assertEqual(report["warnings"]["headwords_with_thin_authority_basis"], [])
        self.assertEqual(report["warnings"]["field_terms_still_thin"], [])
        self.assertEqual(report["warnings"]["contact_terms_still_thin"], [])
        self.assertEqual(report["warnings"]["preferred_rendering_mismatches"], [])
        self.assertEqual(report["warnings"]["contact_chain_identity_missing"], [])

    def test_main_emits_json(self) -> None:
        output = io.StringIO()
        fake_report = {
            "summary": {
                "headwords_present": 1,
                "headwords_expected": 1,
                "field_terms_present": 1,
                "field_terms_expected": 1,
                "contact_terms_present": 1,
                "contact_terms_expected": 1,
                "formula_terms_present": 1,
                "formula_terms_expected": 1,
            },
            "errors": {
                "missing_headwords": [],
                "missing_field_terms": [],
                "missing_contact_terms": [],
                "missing_formula_terms": [],
                "cluster_example_source_gaps": [],
            },
            "warnings": {
                "headwords_with_thin_authority_basis": [],
                "field_terms_still_thin": [],
                "contact_terms_still_thin": [],
                "preferred_rendering_mismatches": [],
                "contact_chain_identity_missing": [],
            },
        }

        with mock.patch.object(cluster_report, "load_terms", return_value={}):
            with mock.patch.object(cluster_report, "build_report", return_value=fake_report):
                with mock.patch("sys.argv", ["sense_fields_cluster_report.py", "--format", "json"]):
                    with mock.patch("sys.stdout", output):
                        result = cluster_report.main()

        self.assertEqual(result, 0)
        parsed = json.loads(output.getvalue())
        self.assertEqual(parsed["summary"]["formula_terms_present"], 1)


if __name__ == "__main__":
    unittest.main()
