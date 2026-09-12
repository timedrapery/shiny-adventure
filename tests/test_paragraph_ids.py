from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tests.helpers import load_module


paragraph_ids = load_module("paragraph_ids", "scripts/paragraph_ids.py")
registry = load_module("surface_registry", "scripts/surface_registry.py")


BODY = "### A\n\nOne two three.\n\nRepeat me.\n\nFour five six.\n\nRepeat me.\n\nSeven eight."


def ids(mapping: dict) -> list[str]:
    return [entry["id"] for entry in mapping["passages"]]


class PassageSplittingTests(unittest.TestCase):
    def test_headings_are_not_passages_but_name_their_section(self) -> None:
        passages = paragraph_ids.passages_from_body(BODY)
        self.assertEqual(len(passages), 5)
        self.assertEqual({p.section for p in passages}, {"A"})

    def test_normalization_tracks_visible_text(self) -> None:
        self.assertEqual(
            paragraph_ids.normalize_passage("Some *emphasis*, a `code` word,\nand a [link](x.md)."),
            "Some emphasis, a code word, and a link.",
        )

    def test_identical_passages_get_distinct_ids(self) -> None:
        mapping = paragraph_ids.align(
            paragraph_ids.empty_map("x"), paragraph_ids.passages_from_body(BODY), "h0"
        )
        self.assertEqual(ids(mapping), ["p001", "p002", "p003", "p004", "p005"])
        prints = [entry["fingerprint"] for entry in mapping["passages"]]
        self.assertEqual(prints[1], prints[3])


class AlignmentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.base = paragraph_ids.align(
            paragraph_ids.empty_map("x"), paragraph_ids.passages_from_body(BODY), "h0"
        )

    def realign(self, previous: dict, body: str, version: str) -> dict:
        return paragraph_ids.align(previous, paragraph_ids.passages_from_body(body), version)

    def test_unrelated_edit_keeps_every_other_id(self) -> None:
        edited = self.realign(self.base, BODY.replace("Four five six.", "Four, five, six."), "h1")
        self.assertEqual(ids(edited), ["p001", "p002", "p003", "p004", "p005"])
        self.assertEqual(len(edited["passages"][2]["previous_fingerprints"]), 1)
        self.assertEqual(edited["passages"][0]["previous_fingerprints"], [])

    def test_split_keeps_first_id_and_records_origin(self) -> None:
        split = self.realign(self.base, BODY.replace("One two three.", "One two.\n\nThree."), "h1")
        self.assertEqual(ids(split), ["p001", "p006", "p002", "p003", "p004", "p005"])
        self.assertEqual(split["passages"][1]["split_from"], "p001")

    def test_merge_keeps_first_id_and_retires_the_rest(self) -> None:
        merged = self.realign(self.base, BODY.replace("One two three.\n\nRepeat me.", "One two three, repeat me."), "h1")
        self.assertEqual(ids(merged), ["p001", "p003", "p004", "p005"])
        self.assertEqual(
            merged["retired"],
            [{"id": "p002", "fingerprint": self.base["passages"][1]["fingerprint"],
              "retired_in": "h1", "reason": "merged", "merged_into": "p001"}],
        )

    def test_added_and_removed_passages(self) -> None:
        changed = self.realign(self.base, "### A\n\nNew opening.\n\nOne two three.\n\nRepeat me.\n\nFour five six.\n\nRepeat me.", "h1")
        self.assertEqual(ids(changed), ["p006", "p001", "p002", "p003", "p004"])
        self.assertEqual([r["id"] for r in changed["retired"]], ["p005"])
        self.assertEqual(changed["next_id"], 7)

    def test_ids_are_never_reused(self) -> None:
        removed = self.realign(self.base, BODY.replace("\n\nSeven eight.", ""), "h1")
        readded = self.realign(removed, BODY + "\n\nNine ten.", "h2")
        self.assertNotIn("p005", ids(readded))
        self.assertEqual(ids(readded)[-2:], ["p006", "p007"])

    def test_reverting_an_edit_recognizes_the_earlier_wording(self) -> None:
        edited = self.realign(self.base, BODY.replace("Four five six.", "Four."), "h1")
        reverted = self.realign(edited, BODY, "h2")
        self.assertEqual(ids(reverted), ids(self.base))


class RepositoryMapTests(unittest.TestCase):
    def test_committed_maps_are_current(self) -> None:
        self.assertEqual(paragraph_ids.check(), [])

    def test_enabled_surfaces_have_maps(self) -> None:
        for key in paragraph_ids.enabled_surface_keys():
            self.assertTrue(paragraph_ids.map_path(key).is_file(), key)

    def test_stale_map_is_reported_with_a_repair_hint(self) -> None:
        surface = next(s for s in registry.TRANSLATION_SURFACES if s.key == "sn36_6")
        data = paragraph_ids.load_map(paragraph_ids.map_path("sn36_6"))
        data["passages"] = data["passages"][1:]
        problems = paragraph_ids.map_problems(surface, data)
        self.assertTrue(any("--write" in problem for problem in problems))

    def test_write_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            map_dir = Path(tmp) / "paragraph-ids"
            config = Path(tmp) / "config.json"
            config.write_text(json.dumps({"enabled_surfaces": ["an2_9"]}), encoding="utf-8")
            first = paragraph_ids.write(None, map_dir=map_dir, config_path=config)
            second = paragraph_ids.write(None, map_dir=map_dir, config_path=config)
            self.assertEqual(len(first), 1)
            self.assertEqual(second, [])
            self.assertEqual(paragraph_ids.check(map_dir=map_dir, config_path=config), [])


if __name__ == "__main__":
    unittest.main()
