from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.helpers import load_module


navigation = load_module("term_directory_navigation", "scripts/term_directory_navigation.py")


class TermDirectoryNavigationTests(unittest.TestCase):
    def test_render_index_mentions_flat_structure_decision(self) -> None:
        content = navigation.render_index(
            "major",
            [
                {
                    "stem": "anicca",
                    "path": "terms/major/anicca.json",
                    "term": "anicca",
                    "preferred_translation": "impermanence",
                    "status": "stable",
                    "tags": "core-doctrine",
                }
            ],
        )

        self.assertIn("keep the on-disk directory flat", content)
        self.assertIn("[anicca](../../terms/major/anicca.json)", content)

    def test_check_outputs_reports_missing_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            outputs = {output_dir / "major-term-index.md": "content"}

            failures = navigation.check_outputs(outputs)

        self.assertEqual(len(failures), 1)
        self.assertIn("Missing generated navigation file", failures[0])

    def test_write_and_check_outputs_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            outputs = {output_dir / "major-term-index.md": "# Major\n"}

            with mock.patch.object(navigation, "OUTPUT_DIR", output_dir):
                navigation.write_outputs(outputs)
                failures = navigation.check_outputs(outputs)

        self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()
