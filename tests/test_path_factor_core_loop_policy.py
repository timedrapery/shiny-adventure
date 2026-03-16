from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def load_term(path: str) -> dict[str, object]:
    with (REPO_ROOT / path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


class PathFactorCoreLoopPolicyTests(unittest.TestCase):
    def test_right_view_encodes_active_viewing_loop_without_changing_default(self) -> None:
        samma_ditthi = load_term("terms/major/samma-ditthi.json")

        self.assertEqual(samma_ditthi["preferred_translation"], "right view")
        self.assertIn("right remembering and right effort", samma_ditthi["notes"])
        self.assertTrue(any("right remembering and right effort" in rule["notes"] for rule in samma_ditthi["context_rules"]))

    def test_right_remembering_and_right_effort_are_mutually_reinforcing(self) -> None:
        samma_sati = load_term("terms/major/samma-sati.json")
        samma_vayama = load_term("terms/major/samma-vayama.json")

        self.assertEqual(samma_sati["preferred_translation"], "right remembering")
        self.assertIn("runs circles around the path", samma_sati["notes"])
        self.assertEqual(samma_vayama["preferred_translation"], "right effort")
        self.assertIn("right view and right remembering", samma_vayama["notes"])

    def test_magga_records_core_loop_as_osf_path_explanation(self) -> None:
        magga = load_term("terms/major/magga.json")

        self.assertEqual(magga["preferred_translation"], "path")
        self.assertIn("run circles around one another", magga["notes"])


if __name__ == "__main__":
    unittest.main()
