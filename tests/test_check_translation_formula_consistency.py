from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.helpers import load_module


formula_audit = load_module(
    "check_translation_formula_consistency",
    "scripts/check_translation_formula_consistency.py",
)


class TranslationFormulaConsistencyTests(unittest.TestCase):
    def test_build_report_flags_discouraged_formula_variants(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            translations = repo_root / "docs" / "translations"
            translations.mkdir(parents=True)
            (translations / "sample.md").write_text(
                'The Buddha said:\n'
                '"Venerable sir," they replied.\n'
                "Dependent on eye and forms, eye-knowing arises.\n",
                encoding="utf-8",
            )

            report = formula_audit.build_report(repo_root, translations)

        self.assertEqual(report["summary"]["files_scanned"], 1)
        self.assertEqual(report["summary"]["matches"], 3)
        labels = {finding["label"] for finding in report["findings"]}
        self.assertIn("the buddha said colon", labels)
        self.assertIn("venerable sir", labels)
        self.assertIn("eye and forms formula", labels)

    def test_build_report_skips_notes_and_index_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            translations = repo_root / "docs" / "translations"
            translations.mkdir(parents=True)
            (translations / "sample-notes.md").write_text("The Buddha said:\n", encoding="utf-8")
            (translations / "translation-documents.md").write_text("The Buddha said:\n", encoding="utf-8")
            (translations / "surface.md").write_text("Clean line.\n", encoding="utf-8")

            report = formula_audit.build_report(repo_root, translations)

        self.assertEqual(report["summary"]["files_scanned"], 1)
        self.assertEqual(report["summary"]["matches"], 0)

    def test_main_supports_json_output(self) -> None:
        payload = {
            "summary": {"files_scanned": 1, "matches": 0},
            "label_counts": {},
            "top_files": [],
            "findings": [],
        }
        output = io.StringIO()

        with mock.patch.object(formula_audit, "build_report", return_value=payload):
            with mock.patch(
                "sys.argv",
                ["check_translation_formula_consistency.py", "--format", "json"],
            ):
                with mock.patch("sys.stdout", output):
                    result = formula_audit.main()

        self.assertEqual(result, 0)
        rendered = json.loads(output.getvalue())
        self.assertEqual(rendered["summary"]["files_scanned"], 1)

    def test_build_report_flags_cross_line_formula_variants(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            translations = repo_root / "docs" / "translations"
            translations.mkdir(parents=True)
            (translations / "sample.md").write_text(
                "The same is true when a bhikkhu remains observing feelings in relation to\n"
                "feelings.\n"
                "For, bhikkhus, I say that this is one kind of\n"
                "feeling.\n",
                encoding="utf-8",
            )

            report = formula_audit.build_report(repo_root, translations)

        self.assertEqual(report["summary"]["matches"], 2)
        labels = {finding["label"] for finding in report["findings"]}
        self.assertIn("observing feelings in relation to feelings", labels)
        self.assertIn("one kind of feeling", labels)

    def test_build_report_flags_tanha_definition_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            translations = repo_root / "docs" / "translations"
            translations.mkdir(parents=True)
            (translations / "sample.md").write_text(
                "That desire that causes rebirth, accompanied by craving, attached to this and that.\n"
                "Later the same surface says it is accompanied by pleasure and enjoying everything.\n",
                encoding="utf-8",
            )

            report = formula_audit.build_report(repo_root, translations)

        self.assertEqual(report["summary"]["matches"], 6)
        labels = {finding["label"] for finding in report["findings"]}
        self.assertIn("tanha formula desire wording", labels)
        self.assertIn("tanha formula rebirth shorthand", labels)
        self.assertIn("tanha formula craving collapse", labels)
        self.assertIn("tanha formula pleasure collapse", labels)
        self.assertIn("tanha formula this-and-that attachment", labels)
        self.assertIn("tanha formula enjoying everything", labels)


if __name__ == "__main__":
    unittest.main()
