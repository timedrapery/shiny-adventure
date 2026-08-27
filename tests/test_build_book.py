from __future__ import annotations

import re
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

<nav class="first-twelve-nav" aria-label="First 12 reading route" markdown="1">

**Your First 12: 4 of 12**

[Previous](earlier.md) · [Your First 12](../start-here.md#your-first-12) · [Next](later.md)

</nav>

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
            "first-twelve-nav",
            "earlier.md",
            "start-here.md",
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
        self.assertNotIn("](glossary.md)", manuscript)
        self.assertIn("](#glossary)", manuscript)
        self.assertNotRegex(manuscript, r"^\*\[[^\]]+\]:", msg=manuscript[:500])

    def test_live_manuscript_keeps_no_relative_markdown_page_links(self) -> None:
        """A relative Markdown link cannot resolve inside the EPUB archive.

        Absolute links to the governed sources on GitHub are fine and stay.
        The per-page nav blocks are the usual source of relative ones; this
        is deliberately broader than any single block, so a newly added one
        fails here rather than in the EPUB validator after a deploy.
        """
        leftover = re.findall(
            r"\]\((?![a-z][a-z0-9+.-]*:|//)[^)\s]*\.md(?:#[^)\s]*)?\)",
            book.manuscript(),
        )
        self.assertEqual(leftover, [], msg=f"unresolvable EPUB links: {leftover}")

    def test_glossary_page_link_becomes_an_epub_heading_link(self) -> None:
        cleaned = book.strip_web_furniture("See the [glossary](glossary.md).")
        self.assertEqual(cleaned, "See the [glossary](#glossary).")


if __name__ == "__main__":
    unittest.main()
