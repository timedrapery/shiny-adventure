from __future__ import annotations

import re
import unittest
from pathlib import Path

from tests.helpers import load_module


reader = load_module("generate_reader", "scripts/generate_reader.py")
registry = load_module("surface_registry", "scripts/surface_registry.py")

REPO_ROOT = Path(__file__).resolve().parent.parent
READER_DIR = REPO_ROOT / "reader-src"
SUTTA_DIR = READER_DIR / "suttas"


class MetadataCoverageTests(unittest.TestCase):
    def test_every_surface_has_reader_metadata(self) -> None:
        keys = {s.key for s in registry.TRANSLATION_SURFACES}
        self.assertEqual(keys - set(registry.READER_METADATA), set())

    def test_no_orphan_reader_metadata(self) -> None:
        keys = {s.key for s in registry.TRANSLATION_SURFACES}
        self.assertEqual(set(registry.READER_METADATA) - keys, set())

    def test_every_surface_has_a_known_stage(self) -> None:
        stages = {number for number, _, _ in registry.STAGES}
        for key, meta in registry.READER_METADATA.items():
            self.assertIn(meta.stage, stages, key)

    def test_every_surface_has_a_nonempty_reader_title(self) -> None:
        for key, meta in registry.READER_METADATA.items():
            self.assertIsInstance(meta.reader_title, str, key)
            self.assertTrue(meta.reader_title.strip(), key)

    def test_reading_order_covers_the_corpus_exactly_once(self) -> None:
        ordered = registry.surfaces_in_reading_order()
        self.assertEqual(len(ordered), len(registry.TRANSLATION_SURFACES))
        self.assertEqual(len({s.key for s in ordered}), len(ordered))

    def test_stage_positions_are_unique(self) -> None:
        seen: set[tuple[int, int]] = set()
        for key, meta in registry.READER_METADATA.items():
            position = (meta.stage, meta.order)
            self.assertNotIn(position, seen, f"duplicate position at {key}")
            seen.add(position)

    def test_essential_five_are_registered_surfaces(self) -> None:
        keys = {s.key for s in registry.TRANSLATION_SURFACES}
        for key in registry.ESSENTIAL_FIVE:
            self.assertIn(key, keys)


class GeneratedStateTests(unittest.TestCase):
    def test_reader_is_current(self) -> None:
        self.assertEqual(reader.check(), [])

    def test_generation_is_deterministic(self) -> None:
        first = reader.planned_files()
        second = reader.planned_files()
        self.assertEqual(
            {p: c for p, c in first.items()},
            {p: c for p, c in second.items()},
        )

    def test_every_surface_has_a_reader_page(self) -> None:
        for surface in registry.TRANSLATION_SURFACES:
            page = SUTTA_DIR / surface.main_name
            self.assertTrue(page.exists(), surface.label)

    def test_no_orphan_reader_pages(self) -> None:
        self.assertEqual(reader.orphan_pages(), [])

    def test_reader_body_matches_the_governed_surface(self) -> None:
        for surface in registry.TRANSLATION_SURFACES:
            want = reader.surface_body(
                surface.main_path.read_text(encoding="utf-8")
            )
            page = (SUTTA_DIR / surface.main_name).read_text(encoding="utf-8")
            self.assertIn(want.strip(), page, surface.label)

    def test_hand_written_intros_survive_regeneration(self) -> None:
        page = SUTTA_DIR / "mn26-pasarasi-sutta.md"
        intro = reader.existing_intro(page)
        self.assertIsNotNone(intro)
        self.assertIn("Most of these texts are the Buddha teaching", intro)
        regenerated = reader.planned_files()[page]
        self.assertIn("Most of these texts are the Buddha teaching", regenerated)

    def test_every_page_has_a_sound_reader_hierarchy(self) -> None:
        planned = reader.planned_files()
        for surface in registry.TRANSLATION_SURFACES:
            page = planned[SUTTA_DIR / surface.main_name]
            self.assertEqual(page.count("\n# "), 1, surface.label)
            self.assertIn("\n## Before you read\n", page, surface.label)
            self.assertIn("\n## Translation\n", page, surface.label)
            self.assertRegex(page, r"\n### .+", surface.label)
            self.assertLess(
                page.index("## Before you read"),
                page.index("## Translation"),
                surface.label,
            )

    def test_every_page_has_reading_time_visible_terms_and_named_navigation(self) -> None:
        planned = reader.planned_files()
        for surface in registry.TRANSLATION_SURFACES:
            page = planned[SUTTA_DIR / surface.main_name]
            self.assertRegex(
                page,
                r"Reading time:</strong> about \d+ min · [\d,]+ words",
            )
            self.assertIn('<details class="reader-terms">', page, surface.label)
            self.assertIn('aria-label="Reading order"', page, surface.label)

    def test_the_default_intro_never_displaces_a_written_one(self) -> None:
        planned = reader.planned_files()
        pages = [
            p for p in planned
            if p.parent == SUTTA_DIR and p.name != "index.md"
        ]
        self.assertEqual(len(pages), len(registry.TRANSLATION_SURFACES))
        for path in pages:
            intro = reader.existing_intro(path)
            uses_default = reader.DEFAULT_INTRO in planned[path]
            if intro and intro != reader.DEFAULT_INTRO:
                self.assertFalse(
                    uses_default,
                    f"{path.name} has a written intro but regenerates to the default",
                )

    def test_the_hand_written_intros_are_present_and_counted(self) -> None:
        written = [
            p for p in SUTTA_DIR.glob("*.md")
            if p.name != "index.md"
            and (reader.existing_intro(p) or "") != reader.DEFAULT_INTRO
            and reader.existing_intro(p)
        ]
        # Five prototype pages plus the five added in the reader phase.
        self.assertGreaterEqual(len(written), 10)


class CorpusCountTests(unittest.TestCase):
    def _read(self, name: str) -> str:
        return (READER_DIR / name).read_text(encoding="utf-8")

    def test_home_page_states_the_real_corpus_size(self) -> None:
        total = len(registry.TRANSLATION_SURFACES)
        self.assertIn(f"All {total} translations", self._read("index.md"))

    def test_essential_five_reading_claim_is_computed_from_the_corpus(self) -> None:
        by_key = {surface.key: surface for surface in registry.TRANSLATION_SURFACES}
        words = sum(
            reader.translation_word_count(reader.surface_body(
                by_key[key].main_path.read_text(encoding="utf-8")
            ))
            for key in registry.ESSENTIAL_FIVE
        )
        minutes = (words + reader.WORDS_PER_MINUTE - 1) // reader.WORDS_PER_MINUTE
        home = reader.render_home()
        self.assertIn(f"about {minutes} minutes", home)
        self.assertIn(f"({words:,} words)", home)
        self.assertNotIn("under a thousand words", home)

    def test_no_stale_hardcoded_counts_in_reader_prose(self) -> None:
        total = len(registry.TRANSLATION_SURFACES)
        for name in ("index.md", "start-here.md", "about.md"):
            text = self._read(name)
            for stale in ("36 translations", "36 suttas", "five readings",
                          "Five readings"):
                self.assertNotIn(stale, text, f"{name} has stale count {stale!r}")
            for match in re.findall(r"\b(\d{2})\s+(?:translations|texts)\b", text):
                self.assertEqual(int(match), total, name)

    def test_all_suttas_index_lists_every_surface(self) -> None:
        text = (SUTTA_DIR / "index.md").read_text(encoding="utf-8")
        for surface in registry.TRANSLATION_SURFACES:
            self.assertIn(surface.main_name, text, surface.label)


class LinkTests(unittest.TestCase):
    def _internal_links(self, text: str) -> list[str]:
        return [
            target for target in re.findall(r"\]\(([^)]+)\)", text)
            if not target.startswith(("http://", "https://", "#"))
        ]

    def test_start_here_links_all_resolve_internally(self) -> None:
        text = (READER_DIR / "start-here.md").read_text(encoding="utf-8")
        targets = self._internal_links(text)
        self.assertTrue(targets)
        for target in targets:
            self.assertTrue(
                (READER_DIR / target.split("#")[0]).exists(), target
            )

    def test_start_here_covers_every_surface(self) -> None:
        text = (READER_DIR / "start-here.md").read_text(encoding="utf-8")
        for surface in registry.TRANSLATION_SURFACES:
            self.assertIn(f"suttas/{surface.main_name}", text, surface.label)

    def test_start_here_has_no_raw_github_translation_links(self) -> None:
        text = (READER_DIR / "start-here.md").read_text(encoding="utf-8")
        self.assertNotIn("blob/main/docs/translations", text)

    def test_all_suttas_links_resolve(self) -> None:
        text = (SUTTA_DIR / "index.md").read_text(encoding="utf-8")
        for target in self._internal_links(text):
            self.assertTrue((SUTTA_DIR / target.split("#")[0]).exists()
                            or (READER_DIR / target.split("#")[0]).exists(), target)

    def test_reading_path_navigation_is_linked_end_to_end(self) -> None:
        ordered = registry.surfaces_in_reading_order()
        first = (SUTTA_DIR / ordered[0].main_name).read_text(encoding="utf-8")
        last = (SUTTA_DIR / ordered[-1].main_name).read_text(encoding="utf-8")
        self.assertIn(ordered[1].main_name, first)
        self.assertIn(ordered[-2].main_name, last)


class NavigationTests(unittest.TestCase):
    def test_generated_nav_includes_every_surface(self) -> None:
        nav = reader.render_nav()
        for surface in registry.TRANSLATION_SURFACES:
            self.assertIn(f"suttas/{surface.main_name}", nav, surface.label)

    def test_mkdocs_nav_block_is_current(self) -> None:
        self.assertEqual(
            reader.MKDOCS.read_text(encoding="utf-8"), reader.planned_mkdocs()
        )


class GlossaryTests(unittest.TestCase):
    def test_glossary_source_parses(self) -> None:
        entries = reader.load_glossary()
        self.assertGreater(len(entries), 20)

    def test_glossary_page_generates_and_lists_terms(self) -> None:
        page = reader.render_glossary()
        entries = reader.load_glossary()
        sample = sorted(entries)[0]
        self.assertIn(sample.casefold(), page.casefold())

    def test_per_page_glossary_only_includes_terms_on_that_page(self) -> None:
        entries = {"arrow": "a definition", "zebra": "not present here"}
        body = "There was an arrow in the story."
        found = dict(reader.glossary_for_page(body, entries))
        self.assertIn("arrow", found)
        self.assertNotIn("zebra", found)

    def test_per_page_glossary_is_case_insensitive_and_deduplicated(self) -> None:
        entries = {
            "Bhante": "a respectful form of address",
            "bhante": "a respectful form of address",
        }
        found = reader.glossary_for_page("BHANTE, please listen.", entries)
        self.assertEqual(len(found), 1)

    def test_inline_abbreviations_preserve_exact_case(self) -> None:
        entries = {
            "Bhante": "upper-case definition",
            "bhante": "lower-case definition",
        }
        found = reader.glossary_abbreviations_for_page(
            "Bhante, please listen.", entries
        )
        self.assertEqual(found, [("Bhante", "upper-case definition")])

    def test_case_variants_with_different_meanings_remain_distinct(self) -> None:
        entries = {
            "Dhamma": "the Buddha's teaching",
            "dhamma": "a thing or quality",
        }
        found = reader.glossary_for_page("The Dhamma explains each dhamma.", entries)
        self.assertEqual(dict(found), entries)

    def test_standalone_glossary_only_collapses_identical_case_variants(self) -> None:
        page = reader.render_glossary().casefold()
        self.assertEqual(page.count("<dfn>bhante</dfn>"), 1)
        self.assertEqual(page.count("<dfn>dhamma</dfn>"), 2)


class NewcomerGuideTests(unittest.TestCase):
    def test_guides_cover_the_essential_five_exactly(self) -> None:
        guides = reader.load_newcomer_guides()
        self.assertEqual(set(guides), set(registry.ESSENTIAL_FIVE))

    def test_essential_pages_render_the_structured_orientation(self) -> None:
        planned = reader.planned_files()
        by_key = {surface.key: surface for surface in registry.TRANSLATION_SURFACES}
        for key in registry.ESSENTIAL_FIVE:
            page = planned[SUTTA_DIR / by_key[key].main_name]
            for heading in (
                "### What happens",
                "### Central question",
                "### Main point",
                "### Reading tip",
                "### This text is not saying",
                "### Key words",
            ):
                self.assertIn(heading, page, key)

    def test_guide_validation_checks_terms_and_governed_headings(self) -> None:
        # Loading is the validation boundary; malformed terms or evidence
        # headings raise instead of becoming untraceable reader prose.
        self.assertTrue(reader.load_newcomer_guides())


if __name__ == "__main__":
    unittest.main()
