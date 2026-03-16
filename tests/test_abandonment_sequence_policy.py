from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def load_term(path: str) -> dict[str, object]:
    with (REPO_ROOT / path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


class AbandonmentSequencePolicyTests(unittest.TestCase):
    def test_target_defaults_are_distinct(self) -> None:
        pariyutthana = load_term("terms/major/pariyutthana.json")
        pahana = load_term("terms/major/pahana.json")
        viraga = load_term("terms/major/viraga.json")
        vossagga = load_term("terms/major/vossagga.json")
        nirodha = load_term("terms/major/nirodha.json")
        khaya = load_term("terms/major/khaya.json")

        self.assertEqual(pariyutthana["preferred_translation"], "manifestation")
        self.assertEqual(pahana["preferred_translation"], "abandoning")
        self.assertEqual(viraga["preferred_translation"], "fading")
        self.assertEqual(vossagga["preferred_translation"], "relinquishment")
        self.assertEqual(nirodha["preferred_translation"], "quenching")
        self.assertEqual(khaya["preferred_translation"], "wearing away")

    def test_nirodha_stays_distinct_from_khaya(self) -> None:
        nirodha = load_term("terms/major/nirodha.json")
        khaya = load_term("terms/major/khaya.json")

        self.assertIn("wearing away", nirodha["discouraged_translations"])
        self.assertIn("cessation", khaya["discouraged_translations"])

    def test_pahana_and_vossagga_do_not_collapse(self) -> None:
        pahana = load_term("terms/major/pahana.json")
        vossagga = load_term("terms/major/vossagga.json")

        self.assertIn("release", pahana["discouraged_translations"])
        self.assertIn("abandonment", vossagga["discouraged_translations"])

    def test_formula_records_preserve_sequence_distinctions(self) -> None:
        asesa = load_term("terms/minor/asesa-viraga-nirodha.json")
        asavakkhaya = load_term("terms/minor/asavakkhaya.json")

        self.assertEqual(asesa["preferred_translation"], "complete fading and quenching")
        self.assertEqual(asavakkhaya["preferred_translation"], "the wearing away of the outflows")


if __name__ == "__main__":
    unittest.main()
