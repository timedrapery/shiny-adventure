from __future__ import annotations

import unittest

from tests.helpers import load_module


text_utils = load_module("text_utils", "scripts/text_utils.py")


class TextUtilsTests(unittest.TestCase):
    def test_normalize_term_removes_diacritics_and_normalizes_separators(self) -> None:
        self.assertEqual(
            text_utils.normalize_term("Paṭicca-samuppāda"),
            "paticca_samuppada",
        )

    def test_safe_text_escapes_non_ascii_for_console_output(self) -> None:
        self.assertEqual(
            text_utils.safe_text("paññā"),
            "pa\\xf1\\xf1\\u0101",
        )


if __name__ == "__main__":
    unittest.main()
