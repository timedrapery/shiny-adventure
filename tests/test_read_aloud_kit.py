from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tests.helpers import load_module


kit_module = load_module("read_aloud_kit", "scripts/read_aloud_kit.py")
check_readability = load_module(
    "check_readability_reviews", "scripts/check_readability_reviews.py"
)


SAMPLE = (
    "# MN 0: Sample\n"
    "\n"
    "## Editorial Note\n"
    "\n"
    "- The Blessed One dwells here, in apparatus that is not read aloud.\n"
    "\n"
    "## Translation\n"
    "\n"
    "### The First Part\n"
    "\n"
    '"Bhikkhus, this is the first sentence. This is the second."\n'
    "\n"
    "They were glad.\n"
)


class FakeSurface:
    def __init__(self, main_relpath: str) -> None:
        self.key = "mn0"
        self.label = "MN 0"
        self.main_relpath = main_relpath


class NumberedSentenceTests(unittest.TestCase):
    def test_sentences_are_numbered_from_one(self) -> None:
        sentences = kit_module.numbered_sentences(SAMPLE)
        self.assertEqual([s["number"] for s in sentences], [1, 2, 3])

    def test_apparatus_is_not_part_of_the_reading(self) -> None:
        """A reviewer reads the translation, not the editorial note."""
        joined = " ".join(s["text"] for s in kit_module.numbered_sentences(SAMPLE))
        self.assertNotIn("Blessed One", joined)
        self.assertNotIn("The First Part", joined)

    def test_each_sentence_carries_its_source_line(self) -> None:
        sentences = kit_module.numbered_sentences(SAMPLE)
        for sentence in sentences:
            self.assertGreater(sentence["line"], 0)


class BuildKitTests(unittest.TestCase):
    def _kit(self, tmpdir: str, text: str = SAMPLE) -> dict:
        repo_root = Path(tmpdir)
        translations = repo_root / "docs" / "translations"
        translations.mkdir(parents=True)
        relpath = "docs/translations/mn0-sample-sutta.md"
        (repo_root / relpath).write_text(text, encoding="utf-8")
        return kit_module.build_kit(FakeSurface(relpath), repo_root=repo_root)

    def test_hash_matches_the_gate_the_ledger_checks(self) -> None:
        """The kit's hash must be the same one check_newcomer_reviews compares.

        A kit that computed its own hash a different way would bind evidence to
        something the gate does not recognise, which is the exact failure the
        protocol warns about.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            translations = repo_root / "docs" / "translations"
            translations.mkdir(parents=True)
            relpath = "docs/translations/mn0-sample-sutta.md"
            path = repo_root / relpath
            path.write_text(SAMPLE, encoding="utf-8")
            kit = kit_module.build_kit(FakeSurface(relpath), repo_root=repo_root)
            self.assertEqual(
                kit["body_sha256"], check_readability.translation_body_sha256(path)
            )

    def test_estimate_is_at_least_one_minute(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            kit = self._kit(tmpdir, "## Translation\n\nShort.\n")
        self.assertEqual(kit["minutes"], 1)


class RenderTests(unittest.TestCase):
    def _kit(self, tmpdir: str) -> dict:
        repo_root = Path(tmpdir)
        (repo_root / "docs" / "translations").mkdir(parents=True)
        relpath = "docs/translations/mn0-sample-sutta.md"
        (repo_root / relpath).write_text(SAMPLE, encoding="utf-8")
        return kit_module.build_kit(FakeSurface(relpath), repo_root=repo_root)

    def test_watch_points_are_withheld_by_default(self) -> None:
        """A reviewer told where the awkward sentences are is not a first hearing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            kit = self._kit(tmpdir)
        self.assertNotIn("Facilitator notes", kit_module.render_kit(kit))
        self.assertIn(
            "Facilitator notes", kit_module.render_kit(kit, facilitator=True)
        )

    def test_ledger_block_carries_the_real_hash(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            kit = self._kit(tmpdir)
            rendered = kit_module.render_kit(kit)
        block = rendered.split("```json")[1].split("```")[0]
        record = json.loads(block)
        self.assertEqual(record["body_sha256"], kit["body_sha256"])
        self.assertEqual(record["status"], "complete")
        self.assertTrue(record["reviewers"])

    def test_every_sentence_appears_in_the_reading(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            kit = self._kit(tmpdir)
            rendered = kit_module.render_kit(kit)
        for sentence in kit["sentences"]:
            self.assertIn(str(sentence["text"]), rendered)


class PilotTests(unittest.TestCase):
    def test_pilot_keys_exist_in_the_registry(self) -> None:
        registry = kit_module.surfaces_by_key()
        for key in kit_module.PILOT:
            self.assertIn(key, registry)

    def test_pilot_is_ordered_shortest_first(self) -> None:
        """The first session should meet the method on a one-minute text."""
        kits = [
            kit_module.build_kit(kit_module.surfaces_by_key()[key])
            for key in kit_module.PILOT
        ]
        lengths = [int(kit["words"]) for kit in kits]
        self.assertEqual(lengths, sorted(lengths))

    def test_real_surfaces_render(self) -> None:
        for key in kit_module.PILOT:
            kit = kit_module.build_kit(kit_module.surfaces_by_key()[key])
            rendered = kit_module.render_kit(kit, facilitator=True)
            self.assertIn(str(kit["body_sha256"]), rendered)
            self.assertTrue(kit["sentences"])


if __name__ == "__main__":
    unittest.main()
