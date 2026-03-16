from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def load_term(path: str) -> dict[str, object]:
    with (REPO_ROOT / path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


class BondageImageryPolicyTests(unittest.TestCase):
    def test_ogha_yoga_gantha_have_distinct_defaults(self) -> None:
        ogha = load_term("terms/major/ogha.json")
        yoga = load_term("terms/major/yoga.json")
        gantha = load_term("terms/major/gantha.json")

        self.assertEqual(ogha["preferred_translation"], "flood")
        self.assertEqual(yoga["preferred_translation"], "yoke")
        self.assertEqual(gantha["preferred_translation"], "knot")

    def test_ogha_and_yoga_block_generic_bondage_drift(self) -> None:
        ogha = load_term("terms/major/ogha.json")
        yoga = load_term("terms/major/yoga.json")

        self.assertIn("bondage", ogha["discouraged_translations"])
        self.assertIn("bondage", yoga["discouraged_translations"])
        self.assertIn("fetter", yoga["discouraged_translations"])

    def test_yoga_family_alignment_is_explicit(self) -> None:
        yoga = load_term("terms/major/yoga.json")
        kamayoga = load_term("terms/minor/kamayoga.json")
        yogakkhema = load_term("terms/minor/yogakkhema.json")

        self.assertEqual(yoga["preferred_translation"], "yoke")
        self.assertEqual(kamayoga["preferred_translation"], "sensual yoke")
        self.assertEqual(yogakkhema["preferred_translation"], "security from the yoke")

    def test_ogha_family_alignment_is_explicit(self) -> None:
        ogha = load_term("terms/major/ogha.json")
        kamogha = load_term("terms/minor/kamogha.json")

        self.assertEqual(ogha["preferred_translation"], "flood")
        self.assertEqual(kamogha["preferred_translation"], "sensual flood")


if __name__ == "__main__":
    unittest.main()
