from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tests.helpers import load_module


term_store = load_module("term_store", "scripts/term_store.py")


class TermStoreTests(unittest.TestCase):
    def test_iter_term_files_is_sorted_recursive_and_json_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "major").mkdir()
            (root / "minor").mkdir()
            (root / "minor" / "b.json").write_text("{}", encoding="utf-8")
            (root / "major" / "a.json").write_text("{}", encoding="utf-8")
            (root / "README.md").write_text("not a term", encoding="utf-8")
            (root / "dir.json").mkdir()

            found = [path.relative_to(root).as_posix() for path in term_store.iter_term_files(root)]

        self.assertEqual(found, ["major/a.json", "minor/b.json"])

    def test_destination_uses_entry_type_folder(self) -> None:
        root = Path("terms")
        self.assertEqual(
            term_store.destination_for_record(root, {"entry_type": "major"}, "sati"),
            root / "major" / "sati.json",
        )
        self.assertEqual(
            term_store.destination_for_record(root, {"entry_type": "minor"}, "pamojja"),
            root / "minor" / "pamojja.json",
        )

    def test_unknown_entry_type_goes_to_the_root(self) -> None:
        root = Path("terms")
        self.assertEqual(
            term_store.destination_for_record(root, {}, "loose"),
            root / "loose.json",
        )


if __name__ == "__main__":
    unittest.main()
