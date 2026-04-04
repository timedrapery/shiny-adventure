from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def load_term(path: str) -> dict[str, object]:
    with (REPO_ROOT / path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


class FourNobleTruthsPracticePolicyTests(unittest.TestCase):
    def test_ariyasacca_notes_allow_correct_noble_practice_cycle(self) -> None:
        ariyasacca = load_term("terms/major/ariyasacca.json")

        self.assertEqual(ariyasacca["preferred_translation"], "noble truth")
        self.assertIn("truth of the buddha", ariyasacca["alternative_translations"])
        self.assertIn("correct noble practice", ariyasacca["notes"])
        self.assertTrue(any("wake up" in rule["notes"] for rule in ariyasacca["context_rules"]))

    def test_dukkha_and_nirodha_encode_practical_cycle_without_changing_defaults(self) -> None:
        dukkha = load_term("terms/major/dukkha.json")
        nirodha = load_term("terms/major/nirodha.json")

        self.assertEqual(dukkha["preferred_translation"], "dissatisfaction")
        self.assertIn("waking up and looking directly", dukkha["notes"])
        self.assertEqual(nirodha["preferred_translation"], "quenching")
        self.assertIn("congratulating oneself", nirodha["notes"])

    def test_magga_kusala_and_sati_keep_house_defaults_while_allowing_osf_cycle_language(self) -> None:
        magga = load_term("terms/major/magga.json")
        kusala = load_term("terms/major/kusala.json")
        sati = load_term("terms/major/sati.json")

        self.assertEqual(magga["preferred_translation"], "path")
        self.assertIn("making a wholesome change", magga["notes"])
        self.assertEqual(kusala["preferred_translation"], "wholesome")
        self.assertIn("make a wholesome change", kusala["notes"])
        self.assertEqual(sati["preferred_translation"], "remembering")
        self.assertIn("again as often as one can remember", sati["notes"])


if __name__ == "__main__":
    unittest.main()
