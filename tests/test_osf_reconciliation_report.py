from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.helpers import load_module


report_module = load_module("osf_reconciliation_report", "scripts/osf_reconciliation_report.py")


def make_record(stem: str, preferred: str, **overrides: object) -> dict[str, object]:
    data: dict[str, object] = {
        "term": stem,
        "normalized_term": stem,
        "entry_type": "major",
        "part_of_speech": "noun",
        "preferred_translation": preferred,
        "alternative_translations": [f"{preferred} alt"],
        "discouraged_translations": [f"{preferred} discouraged"],
        "definition": f"{stem} definition",
        "notes": f"{stem} note",
        "context_rules": [
            {"context": "default", "rendering": preferred, "notes": "default"},
        ],
        "related_terms": [],
        "example_phrases": [{"pali": stem, "translation": preferred, "source": "SN 1.1"}],
        "sutta_references": ["SN 1.1"],
        "tags": ["osf-reconciliation"],
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
        "status": "stable",
    }
    data.update(overrides)
    return data


class OsfReconciliationReportTests(unittest.TestCase):
    def test_build_report_flags_missing_reviewed_terms(self) -> None:
        terms = {
            "sunnata": make_record("sunnata", "emptiness"),
            "nibbana": make_record("nibbana", "nibbāna"),
        }

        report = report_module.build_report(terms)

        self.assertIn("nirodha", report["errors"]["missing_reviewed_terms"])
        self.assertIn("sati", report["errors"]["missing_reviewed_terms"])

    def test_build_report_warns_on_preferred_rendering_mismatch(self) -> None:
        terms = {
            stem: make_record(stem, meta["expected_default"])
            for stem, meta in report_module.REVIEWED_TERMS.items()
        }
        terms["vimutti"]["preferred_translation"] = "liberation"

        report = report_module.build_report(terms)

        self.assertIn("vimutti", report["warnings"]["preferred_rendering_mismatches"])

    def test_write_outputs_creates_expected_file(self) -> None:
        terms = {
            stem: make_record(stem, meta["expected_default"])
            for stem, meta in report_module.REVIEWED_TERMS.items()
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            with mock.patch.object(report_module, "OUTPUT_DIR", output_dir):
                written = report_module.write_outputs(terms)

        self.assertEqual(len(written), 1)
        self.assertEqual(written[0].name, "osf-reconciliation-sheet.md")

    def test_render_sheet_mentions_classifications(self) -> None:
        terms = {
            stem: make_record(stem, meta["expected_default"])
            for stem, meta in report_module.REVIEWED_TERMS.items()
        }

        sheet = report_module.render_sheet(terms)

        self.assertIn("ALIGN", sheet)
        self.assertIn("TOLERATE ALTERNATE", sheet)
        self.assertIn("REFUSE DRIFT", sheet)

    def test_main_emits_json(self) -> None:
        output = io.StringIO()
        fake_report = {
            "summary": {"reviewed_terms_present": 1, "reviewed_terms_expected": 1},
            "errors": {"missing_reviewed_terms": []},
            "warnings": {"preferred_rendering_mismatches": []},
        }

        with mock.patch.object(report_module, "load_terms", return_value={}):
            with mock.patch.object(report_module, "build_report", return_value=fake_report):
                with mock.patch("sys.argv", ["osf_reconciliation_report.py", "--format", "json"]):
                    with mock.patch("sys.stdout", output):
                        result = report_module.main()

        self.assertEqual(result, 0)
        parsed = json.loads(output.getvalue())
        self.assertEqual(parsed["summary"]["reviewed_terms_present"], 1)


if __name__ == "__main__":
    unittest.main()
