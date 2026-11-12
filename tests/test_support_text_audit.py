from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from tests.helpers import load_module


audit = load_module("support_text_audit", "scripts/support_text_audit.py")


def words(n: int) -> str:
    return " ".join(["word"] * n)


class SentenceRulesTests(unittest.TestCase):
    def test_sentences_split_on_end_punctuation(self) -> None:
        self.assertEqual(
            audit.split_sentences('One idea here. "A quote." Another one?'),
            ["One idea here.", '"A quote."', "Another one?"],
        )

    def test_quoted_text_does_not_count_toward_length(self) -> None:
        sentence = f'It says "{words(30)}" plainly.'
        self.assertEqual(audit.counted_words(sentence), 3)

    def test_passive_voice_is_detected_outside_quotes(self) -> None:
        self.assertTrue(audit.is_passive("The monks are taught by the Buddha."))
        self.assertTrue(audit.is_passive("Harm is not done."))
        self.assertFalse(audit.is_passive("The Buddha teaches the monks."))
        self.assertFalse(audit.is_passive('He says "it is done" and leaves.'))

    def test_limits_differ_for_questions_and_descriptions(self) -> None:
        sentence = words(22) + "."
        self.assertEqual(audit.check_block("f", "x", sentence, audit.DESCRIPTION_LIMIT, 3), [])
        [finding] = audit.check_block("f", "x", sentence, audit.INSTRUCTION_LIMIT, 3)
        self.assertEqual(finding.rule, "long sentence")

    def test_long_paragraphs_are_reported(self) -> None:
        text = " ".join(["Short one."] * 4)
        [finding] = audit.check_block("f", "x", text, audit.DESCRIPTION_LIMIT, 3)
        self.assertEqual(finding.rule, "long paragraph")


class FileTests(unittest.TestCase):
    def test_guide_questions_use_the_shorter_limit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "x.json"
            path.write_text(json.dumps({
                "surface_key": "x",
                "question": words(22) + "?",
                "main_point": words(22) + ".",
                "key_terms": ["not prose"],
            }), encoding="utf-8")
            findings = audit.audit([path])
        self.assertEqual([(f.location, f.rule) for f in findings], [("question", "long sentence")])

    def test_intros_skip_comments_and_headings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "x.md"
            path.write_text(f"<!-- {words(40)}. -->\n\n# {words(40)}\n\nA short line.\n", encoding="utf-8")
            self.assertEqual(audit.audit([path]), [])

    def test_markdown_list_items_are_checked_and_code_is_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "README.md"
            path.write_text(
                f"```bash\n{words(40)}\n```\n\n- Short item.\n- {words(30)}.\n\n    {words(40)}\n",
                encoding="utf-8",
            )
            [finding] = audit.audit([path])
        self.assertEqual((finding.location, finding.rule), ("paragraph 1, item 2", "long sentence"))

    def test_glossary_definitions_are_checked_by_term(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "glossary.md"
            path.write_text(f"*[heart]: {words(30)}.\n*[mind]: Short.\n", encoding="utf-8")
            [finding] = audit.audit([path])
        self.assertEqual(finding.location, "glossary: heart")

    def test_strict_fails_only_when_there_are_findings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            clean = Path(tmp) / "clean.md"
            clean.write_text("A short line.\n", encoding="utf-8")
            dirty = Path(tmp) / "dirty.md"
            dirty.write_text("The text is written badly.\n", encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(audit.main(["--strict", "--path", str(clean)]), 0)
                self.assertEqual(audit.main(["--strict", "--path", str(dirty)]), 1)
                self.assertEqual(audit.main(["--path", str(dirty)]), 0)

    def test_the_repository_support_text_parses(self) -> None:
        self.assertIsInstance(audit.audit(audit.default_targets()), list)


if __name__ == "__main__":
    unittest.main()
