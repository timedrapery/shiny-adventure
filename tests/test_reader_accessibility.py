from __future__ import annotations

import unittest

from tests.helpers import load_module


accessibility = load_module(
    "check_reader_accessibility", "scripts/check_reader_accessibility.py"
)


GOOD_PAGE = """\
# A readable title

*About 5 min · 784 words*

## Before you read

[Skip to the translation](#translation)

### What happens

A teacher explains pain.

### Central question

Why add suffering?

### Main point

Pain need not become resistance.

### Reading tip

Compare the two responses.

Key terms: pain; resistance.

## Translation

### Setting

The translation begins.

<details class="reader-terms">
<summary>Words used in this translation (2)</summary>
Definitions go here.
</details>

<nav class="reading-order" aria-label="Reading order">
Previous, all suttas, next.
</nav>
"""


class PageContractTests(unittest.TestCase):
    def test_complete_page_passes(self) -> None:
        self.assertEqual(
            accessibility.sutta_page_failures(GOOD_PAGE, "reader-src/suttas/x.md"),
            [],
        )

    def test_reading_metadata_needs_words_and_minutes_on_one_line(self) -> None:
        broken = GOOD_PAGE.replace(
            "*About 5 min · 784 words*", "*784 words*\n\n*About 5 min*"
        )
        failures = accessibility.sutta_page_failures(broken, "x.md")
        self.assertTrue(any("same line" in failure for failure in failures), failures)

    def test_translation_needs_a_real_subheading(self) -> None:
        broken = GOOD_PAGE.replace("### Setting\n\n", "")
        failures = accessibility.sutta_page_failures(broken, "x.md")
        self.assertTrue(any("at least one H3" in failure for failure in failures))

    def test_navigation_needs_both_class_and_accessible_label(self) -> None:
        broken = GOOD_PAGE.replace('aria-label="Reading order"', "")
        failures = accessibility.sutta_page_failures(broken, "x.md")
        self.assertTrue(any("nav.reading-order" in failure for failure in failures))

    def test_visible_terms_panel_needs_a_summary(self) -> None:
        broken = GOOD_PAGE.replace("<summary>", "<p>").replace(
            "</summary>", "</p>"
        )
        failures = accessibility.sutta_page_failures(broken, "x.md")
        self.assertTrue(any("non-empty summary" in failure for failure in failures))

    def test_raw_html_markdown_links_are_rejected(self) -> None:
        broken = GOOD_PAGE.replace(
            "Previous, all suttas, next.",
            '<a href="previous.md">Previous</a>',
        )
        failures = accessibility.sutta_page_failures(broken, "x.md")
        self.assertTrue(any("raw HTML links" in failure for failure in failures))


class NewcomerGuideTests(unittest.TestCase):
    def test_current_essential_five_guides_load(self) -> None:
        guides, failures = accessibility.load_guides()
        self.assertEqual(failures, [])
        self.assertEqual(set(guides), set(accessibility.ESSENTIAL_FIVE))

    def test_guide_content_and_key_terms_must_be_visible_before_translation(self) -> None:
        guide = {
            "scene": "A teacher explains pain.",
            "question": "Why add suffering?",
            "main_point": "Pain need not become resistance.",
            "reading_cue": "Compare the two responses.",
            "key_terms": ["pain", "missing term"],
        }
        failures = accessibility.sutta_page_failures(GOOD_PAGE, "x.md", guide)
        self.assertTrue(
            any("missing term" in failure for failure in failures), failures
        )

    def test_guide_headings_are_checked_inside_before_you_read(self) -> None:
        guide = {
            "scene": "A teacher explains pain.",
            "question": "Why add suffering?",
            "main_point": "Pain need not become resistance.",
            "reading_cue": "Compare the two responses.",
            "key_terms": ["pain", "resistance"],
        }
        broken = GOOD_PAGE.replace("### Main point", "### The answer")
        failures = accessibility.sutta_page_failures(broken, "x.md", guide)
        self.assertTrue(any("Main point" in failure for failure in failures))


class FlowingIndexTests(unittest.TestCase):
    def test_markdown_table_is_rejected(self) -> None:
        table = "| Term | Meaning |\n| --- | --- |\n| pain | feeling |\n"
        failures = accessibility.markdown_table_failures(table, "glossary.md")
        self.assertTrue(failures)

    def test_flowing_list_is_accepted(self) -> None:
        text = "- **pain** — an unpleasant feeling\n"
        self.assertEqual(
            accessibility.markdown_table_failures(text, "glossary.md"), []
        )


class SiteAssetTests(unittest.TestCase):
    def test_accessible_site_assets_pass(self) -> None:
        mkdocs = "theme:\n  font: false\nextra_css:\n  - stylesheets/reader.css\n"
        css = (
            ":focus-visible { outline: solid; }\n"
            "a { min-height: 44px; max-width: 70ch; }\n"
            ".reader-terms summary { display: block; }\n"
            ".reader-terms summary::before { content: 'open'; "
            "position: absolute; mask: none; -webkit-mask: none; }\n"
            "@media (prefers-reduced-motion: reduce) {}\n"
        )
        self.assertEqual(
            accessibility.accessibility_asset_failures(mkdocs, css), []
        )

    def test_theme_colliding_summary_grid_is_reported(self) -> None:
        mkdocs = "theme:\n  font: false\nextra_css:\n  - stylesheets/reader.css\n"
        css = (
            ":focus-visible { outline: solid; }\n"
            "a { min-height: 44px; max-width: 70ch; }\n"
            ".reader-terms summary { display: grid; }\n"
            ".reader-terms summary::before { content: 'open'; "
            "position: absolute; mask: none; -webkit-mask: none; }\n"
            "@media (prefers-reduced-motion: reduce) {}\n"
        )
        failures = accessibility.accessibility_asset_failures(mkdocs, css)
        self.assertTrue(any("full-width block layout" in item for item in failures))

    def test_missing_accessibility_features_are_reported(self) -> None:
        failures = accessibility.accessibility_asset_failures(
            "theme:\n  font: true\n  features:\n    - navigation.instant\n",
            "",
            False,
        )
        self.assertGreaterEqual(len(failures), 7)


class LiveReaderContractTests(unittest.TestCase):
    def test_planned_reader_output_meets_the_contract(self) -> None:
        self.assertEqual(accessibility.collect_failures(), [])


if __name__ == "__main__":
    unittest.main()
