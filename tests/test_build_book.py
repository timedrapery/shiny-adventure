from __future__ import annotations

import unittest

from tests.helpers import load_module


book = load_module("build_book", "scripts/build_book.py")


class WebFurnitureTests(unittest.TestCase):
    def test_current_reader_furniture_is_removed(self) -> None:
        page = """\
<!-- generated -->
# A Sutta

<p class="reading-meta">Reading time: about 5 min · 784 words</p>

[Skip to the translation](#translation){ .reader-skip-link }

## Before you read

<div class="reader-guide" markdown="1">

### What happens

The useful orientation stays.

</div>

## Translation

### Setting

The governed body stays.

<details class="reader-terms">
<summary>Words used in this translation (1)</summary>
<dl><dt>term</dt><dd>definition</dd></dl>
</details>

---

<nav class="reading-order" aria-label="Reading order" markdown="1">

- [Previous](previous.md)
- [All suttas](index.md)
- [Next](next.md)

</nav>

*[term]: definition
"""
        cleaned = book.strip_web_furniture(page)
        self.assertIn("The useful orientation stays.", cleaned)
        self.assertIn("The governed body stays.", cleaned)
        self.assertIn("reading-meta", cleaned)
        for web_only in (
            "generated",
            "Skip to the translation",
            "reader-terms",
            "reading-order",
            "previous.md",
            "*[term]",
        ):
            self.assertNotIn(web_only, cleaned)

    def test_live_manuscript_has_no_per_page_web_furniture(self) -> None:
        manuscript = book.manuscript()
        self.assertIn("What happens", manuscript)
        self.assertIn("# Glossary", manuscript)
        self.assertNotIn('class="reader-terms"', manuscript)
        self.assertNotIn('class="reading-order"', manuscript)
        self.assertNotIn("Skip to the translation", manuscript)
        self.assertNotRegex(manuscript, r"^\*\[[^\]]+\]:", msg=manuscript[:500])


if __name__ == "__main__":
    unittest.main()
