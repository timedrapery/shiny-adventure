from __future__ import annotations

import io
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.helpers import load_module


check_docs_integrity = load_module("check_docs_integrity", "scripts/check_docs_integrity.py")


def write_required_repo_files(repo_root: Path) -> None:
    (repo_root / ".github" / "ISSUE_TEMPLATE").mkdir(parents=True, exist_ok=True)
    (repo_root / "docs").mkdir(parents=True, exist_ok=True)
    for relative_path in check_docs_integrity.REQUIRED_PATHS:
        path = repo_root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("placeholder\n", encoding="utf-8")


class CheckDocsIntegrityTests(unittest.TestCase):
    def test_collect_markdown_failures_accepts_valid_relative_links_and_anchor(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            write_required_repo_files(repo_root)
            target = repo_root / "docs" / "guide.md"
            target.write_text("# Guide\n\n## Review Model\n", encoding="utf-8")
            source = repo_root / "README.md"
            source.write_text("See [guide](docs/guide.md#review-model).\n", encoding="utf-8")

            failures = check_docs_integrity.collect_markdown_failures(repo_root)

        self.assertEqual(failures, [])

    def test_collect_markdown_failures_reports_missing_anchor(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            write_required_repo_files(repo_root)
            target = repo_root / "docs" / "guide.md"
            target.write_text("# Guide\n", encoding="utf-8")
            source = repo_root / "README.md"
            source.write_text("See [guide](docs/guide.md#missing-anchor).\n", encoding="utf-8")

            failures = check_docs_integrity.collect_markdown_failures(repo_root)

        self.assertEqual(len(failures), 1)
        self.assertIn("missing anchor", failures[0])

    def test_collect_metadata_failures_reports_missing_required_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            write_required_repo_files(repo_root)
            (repo_root / "CITATION.cff").unlink()

            failures = check_docs_integrity.collect_metadata_failures(repo_root)

        self.assertIn("Missing required repository file: CITATION.cff", failures)

    def test_collect_docs_naming_failures_reports_non_kebab_case_docs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            write_required_repo_files(repo_root)
            (repo_root / "docs" / "BAD_NAME.md").write_text("# Bad\n", encoding="utf-8")

            failures = check_docs_integrity.collect_docs_naming_failures(repo_root)

        self.assertEqual(len(failures), 1)
        self.assertIn("lowercase-kebab-case", failures[0])

    def test_collect_docs_naming_failures_allows_registered_policy_docs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            write_required_repo_files(repo_root)
            (repo_root / "docs" / "MODERN_ENGLISH_AUDIT.md").write_text("# Audit\n", encoding="utf-8")
            (repo_root / "docs" / "MODERN_ENGLISH_POLICY.md").write_text("# Policy\n", encoding="utf-8")
            (repo_root / "docs" / "ARCHAIC_DICTION_SWEEP.md").write_text("# Sweep\n", encoding="utf-8")
            (repo_root / "docs" / "VOICE_CONSISTENCY_AUDIT.md").write_text("# Voice Audit\n", encoding="utf-8")
            (repo_root / "docs" / "VOICE_STANDARD.md").write_text("# Voice Standard\n", encoding="utf-8")

            failures = check_docs_integrity.collect_docs_naming_failures(repo_root)

        self.assertEqual(failures, [])

    def test_main_reports_success_for_clean_repo(self) -> None:
        output = io.StringIO()
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            write_required_repo_files(repo_root)
            (repo_root / "docs" / "guide.md").write_text("# Guide\n", encoding="utf-8")
            (repo_root / "README.md").write_text("See [guide](docs/guide.md).\n", encoding="utf-8")

            with mock.patch.object(check_docs_integrity, "REPO_ROOT", repo_root):
                with mock.patch("sys.argv", ["check_docs_integrity.py"]):
                    with mock.patch("sys.stdout", output):
                        result = check_docs_integrity.main()

        self.assertEqual(result, 0)
        self.assertIn("Documentation integrity check passed.", output.getvalue())


if __name__ == "__main__":
    unittest.main()
