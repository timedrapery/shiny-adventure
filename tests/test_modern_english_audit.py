from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.helpers import load_module


audit = load_module("modern_english_audit", "scripts/modern_english_audit.py")


class ModernEnglishAuditTests(unittest.TestCase):
    def test_scan_text_flags_multiple_pattern_categories(self) -> None:
        findings = audit.scan_text(
            "one dwells contemplating the body\nthis is meritorious action\n",
            "terms/major/example.json",
        )

        self.assertEqual(len(findings), 2)
        self.assertEqual(findings[0]["label"], "one dwells")
        self.assertEqual(findings[1]["label"], "meritorious")

    def test_build_report_skips_policy_docs_and_generated_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            (repo_root / "docs" / "generated").mkdir(parents=True)
            (repo_root / "terms").mkdir()
            (repo_root / "README.md").write_text("thus there arises\n", encoding="utf-8")
            (repo_root / "docs" / "MODERN_ENGLISH_AUDIT.md").write_text("thus\n", encoding="utf-8")
            (repo_root / "docs" / "generated" / "sample.md").write_text("one dwells\n", encoding="utf-8")
            (repo_root / "terms" / "sample.json").write_text('{"notes": "meritorious"}\n', encoding="utf-8")

            report = audit.build_report(repo_root)

        self.assertEqual(report["summary"]["files_scanned"], 2)
        self.assertEqual(report["summary"]["matches"], 3)
        self.assertEqual([entry["path"] for entry in report["top_files"]], ["README.md", "terms/sample.json"])

    def test_main_supports_json_output(self) -> None:
        payload = {"summary": {"files_scanned": 1, "matches": 0, "include_generated": False}, "category_counts": {}, "label_counts": {}, "top_files": [], "findings": []}
        output = io.StringIO()

        with mock.patch.object(audit, "build_report", return_value=payload):
            with mock.patch("sys.argv", ["modern_english_audit.py", "--format", "json"]):
                with mock.patch("sys.stdout", output):
                    result = audit.main()

        self.assertEqual(result, 0)
        rendered = json.loads(output.getvalue())
        self.assertEqual(rendered["summary"]["files_scanned"], 1)


if __name__ == "__main__":
    unittest.main()
