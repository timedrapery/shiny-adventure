from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from tests.helpers import load_module


hooks = load_module("mkdocs_hooks", "scripts/mkdocs_hooks.py")


class FoldTests(unittest.TestCase):
    def test_fold_strips_diacritics_and_keeps_case(self) -> None:
        self.assertEqual(hooks.fold("Nibbāna"), "Nibbana")
        self.assertEqual(hooks.fold("saḷāyatana"), "salayatana")
        self.assertEqual(hooks.fold("plain"), "plain")


class AddAliasesTests(unittest.TestCase):
    def test_alias_follows_the_first_occurrence_only(self) -> None:
        text, added = hooks.add_aliases("nibbāna is peace; nibbāna again")
        self.assertEqual(text, "nibbāna nibbana is peace; nibbāna again")
        self.assertEqual(added, 1)

    def test_text_without_diacritics_is_unchanged(self) -> None:
        self.assertEqual(hooks.add_aliases("no accents here"), ("no accents here", 0))

    def test_empty_text_is_safe(self) -> None:
        self.assertEqual(hooks.add_aliases(""), ("", 0))


class PostBuildTests(unittest.TestCase):
    def build(self, docs: object) -> dict:
        with tempfile.TemporaryDirectory() as tmp:
            search = Path(tmp) / "search"
            search.mkdir()
            index = search / "search_index.json"
            index.write_text(json.dumps({"docs": docs}), encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                hooks.on_post_build({"site_dir": tmp})
            return json.loads(index.read_text(encoding="utf-8"))

    def test_index_text_gains_ascii_aliases(self) -> None:
        result = self.build([{"title": "Glossary", "text": "anattā means not-self"}])
        self.assertEqual(result["docs"][0]["text"], "anattā anatta means not-self")

    def test_accented_title_word_is_made_searchable_without_changing_the_title(self) -> None:
        result = self.build([{"title": "Dukkha and Nibbāna", "text": "a page"}])
        doc = result["docs"][0]
        self.assertEqual(doc["title"], "Dukkha and Nibbāna")
        self.assertTrue(doc["text"].endswith("Nibbana"))

    def test_missing_index_is_not_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            hooks.on_post_build({"site_dir": tmp})
            self.assertFalse((Path(tmp) / "search").exists())


if __name__ == "__main__":
    unittest.main()
