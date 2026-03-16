from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def load_term(path: str) -> dict[str, object]:
    with (REPO_ROOT / path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


class CrossingReleaseInterfacePolicyTests(unittest.TestCase):
    def test_target_defaults_are_distinct(self) -> None:
        nissarana = load_term("terms/major/nissarana.json")
        vimutti = load_term("terms/major/vimutti.json")
        mutti = load_term("terms/major/mutti.json")
        tarati = load_term("terms/major/tarati.json")
        tinna = load_term("terms/major/tinna.json")

        self.assertEqual(nissarana["preferred_translation"], "escape")
        self.assertEqual(vimutti["preferred_translation"], "release")
        self.assertEqual(mutti["preferred_translation"], "freedom")
        self.assertEqual(tarati["preferred_translation"], "crosses over")
        self.assertEqual(tinna["preferred_translation"], "crossed over")

    def test_nissarana_and_vimutti_do_not_collapse(self) -> None:
        nissarana = load_term("terms/major/nissarana.json")
        vimutti = load_term("terms/major/vimutti.json")

        self.assertIn("release", nissarana["discouraged_translations"])
        self.assertIn("escape", vimutti["discouraged_translations"])

    def test_vimutti_and_mutti_do_not_drift_into_uncontrolled_synonymy(self) -> None:
        vimutti = load_term("terms/major/vimutti.json")
        mutti = load_term("terms/major/mutti.json")

        self.assertIn("freedom", vimutti["discouraged_translations"])
        self.assertIn("release", mutti["alternative_translations"])

    def test_tarati_and_tinna_preserve_process_result_distinction(self) -> None:
        tarati = load_term("terms/major/tarati.json")
        tinna = load_term("terms/major/tinna.json")

        self.assertIn("is liberated", tarati["discouraged_translations"])
        self.assertIn("liberated", tinna["discouraged_translations"])

    def test_yogakkhema_stays_linked_to_yoga(self) -> None:
        yogakkhema = load_term("terms/minor/yogakkhema.json")

        self.assertEqual(yogakkhema["preferred_translation"], "security from the yoke")
        self.assertIn("yoga", yogakkhema["related_terms"])
        self.assertIn("freedom", yogakkhema["discouraged_translations"])

    def test_crossing_formulas_keep_imagery_explicit(self) -> None:
        ogham_atari = load_term("terms/minor/ogham-atari.json")
        tinno_parangato = load_term("terms/minor/tinno-parangato.json")

        self.assertEqual(ogham_atari["preferred_translation"], "crossed over the flood")
        self.assertEqual(tinno_parangato["preferred_translation"], "crossed over, gone to the far shore")


if __name__ == "__main__":
    unittest.main()
