from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tests.helpers import load_module


structure = load_module(
    "check_markdown_structure", "scripts/check_markdown_structure.py"
)


class DamageDetectionTests(unittest.TestCase):
    def test_flattened_bullet_after_a_sentence_is_caught(self) -> None:
        # The exact shape of the MN 1 damage.
        line = "say. - The same pattern holds for water, fire, air, beings"
        self.assertTrue(structure.scan_text(line, "x.md"))

    def test_flattened_bullet_after_a_closing_quote_is_caught(self) -> None:
        # The exact shape of the MN 118 damage.
        line = "'I breathe out long.' - Breathing in short, they know"
        self.assertTrue(structure.scan_text(line, "x.md"))

    def test_a_proper_bullet_at_line_start_is_clean(self) -> None:
        self.assertEqual(structure.scan_text("- The same pattern holds", "x.md"), [])

    def test_a_hyphen_used_as_punctuation_is_clean(self) -> None:
        # This shape occurs legitimately in DN 15 and must not be flagged.
        line = "does not regard self in this way - 'My self does not feel.'"
        self.assertEqual(structure.scan_text(line, "x.md"), [])

    def test_fenced_code_is_ignored(self) -> None:
        text = "```\nsay. - The same pattern\n```\n"
        self.assertEqual(structure.scan_text(text, "x.md"), [])

    def test_line_numbers_are_reported(self) -> None:
        text = "clean line\n\nsay. - The same pattern holds here\n"
        found = structure.scan_text(text, "x.md")
        self.assertEqual(len(found), 1)
        self.assertTrue(found[0].startswith("x.md:3:"))


class LiveCorpusTests(unittest.TestCase):
    def test_the_live_corpus_has_no_flattened_lists(self) -> None:
        self.assertEqual(structure.collect(), [])


class ScanScopeTests(unittest.TestCase):
    def test_only_markdown_is_scanned(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "docs" / "a.md").write_text("clean\n", encoding="utf-8")
            (root / "docs" / "b.txt").write_text(
                "say. - The same pattern holds", encoding="utf-8"
            )
            found = structure.collect(roots=("docs",), repo_root=root)
        self.assertEqual(found, [])


if __name__ == "__main__":
    unittest.main()
