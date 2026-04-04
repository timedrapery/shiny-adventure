from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.helpers import load_module


audit = load_module("voice_consistency_audit", "scripts/voice_consistency_audit.py")


class VoiceConsistencyAuditTests(unittest.TestCase):
    def test_scan_text_flags_stock_templates_and_filler(self) -> None:
        findings = audit.scan_text(
            '"notes": "Default project rendering."\nIt should be understood that this is a rule.\n',
            "terms/major/example.json",
        )

        self.assertEqual(len(findings), 2)
        self.assertEqual(findings[0]["label"], "default project rendering")
        self.assertEqual(findings[1]["label"], "it should be understood that")

    def test_build_report_skips_policy_docs_and_generated_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            (repo_root / "docs" / "generated").mkdir(parents=True)
            (repo_root / "terms").mkdir()
            (repo_root / "README.md").write_text('"notes": "Useful compact analytical usage."\n', encoding="utf-8")
            (repo_root / "docs" / "VOICE_STANDARD.md").write_text("Project preference is\n", encoding="utf-8")
            (repo_root / "docs" / "generated" / "sample.md").write_text('"notes": "Simple practical usage."\n', encoding="utf-8")
            (repo_root / "terms" / "sample.json").write_text('{"notes": "Default rendering."}\n', encoding="utf-8")

            report = audit.build_report(repo_root)

        self.assertEqual(report["summary"]["files_scanned"], 2)
        self.assertEqual(report["summary"]["matches"], 2)
        self.assertEqual([entry["path"] for entry in report["top_files"]], ["README.md", "terms/sample.json"])

    def test_main_supports_json_output(self) -> None:
        payload = {
            "summary": {"files_scanned": 1, "matches": 0, "include_generated": False},
            "category_counts": {},
            "label_counts": {},
            "top_files": [],
            "findings": [],
        }
        output = io.StringIO()

        with mock.patch.object(audit, "build_report", return_value=payload):
            with mock.patch("sys.argv", ["voice_consistency_audit.py", "--format", "json"]):
                with mock.patch("sys.stdout", output):
                    result = audit.main()

        self.assertEqual(result, 0)
        rendered = json.loads(output.getvalue())
        self.assertEqual(rendered["summary"]["files_scanned"], 1)


if __name__ == "__main__":
    unittest.main()
