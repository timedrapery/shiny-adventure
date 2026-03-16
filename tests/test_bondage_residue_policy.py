from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def load_term(path: str) -> dict[str, object]:
    with (REPO_ROOT / path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


class BondageResiduePolicyTests(unittest.TestCase):
    def test_asava_and_anusaya_are_distinct(self) -> None:
        asava = load_term("terms/major/asava.json")
        anusaya = load_term("terms/major/anusaya.json")

        self.assertEqual(asava["preferred_translation"], "outflow")
        self.assertEqual(anusaya["preferred_translation"], "underlying tendency")
        self.assertIn("defilement", asava["discouraged_translations"])
        self.assertIn("habit", anusaya["discouraged_translations"])

    def test_anusaya_and_samyojana_are_distinct(self) -> None:
        anusaya = load_term("terms/major/anusaya.json")
        samyojana = load_term("terms/major/samyojana.json")

        self.assertEqual(anusaya["preferred_translation"], "underlying tendency")
        self.assertEqual(samyojana["preferred_translation"], "fetter")
        self.assertIn("attachment", samyojana["discouraged_translations"])

    def test_samyojana_and_nivarana_are_distinct(self) -> None:
        samyojana = load_term("terms/major/samyojana.json")
        nivarana = load_term("terms/major/nivarana.json")
        panca_nivarana = load_term("terms/minor/panca-nivarana.json")

        self.assertEqual(samyojana["preferred_translation"], "fetter")
        self.assertEqual(nivarana["preferred_translation"], "distraction")
        self.assertEqual(panca_nivarana["preferred_translation"], "five distractions")

    def test_kilesa_stays_broader_than_specific_bondage_families(self) -> None:
        kilesa = load_term("terms/major/kilesa.json")
        self.assertEqual(kilesa["preferred_translation"], "defilement")
        self.assertIn("hindrance", kilesa["discouraged_translations"])
        self.assertIn("fetter", kilesa["discouraged_translations"])

    def test_anapanasati_practice_clarification_stays_guarded(self) -> None:
        anapanasati = load_term("terms/major/anapanasati.json")
        notes = anapanasati["notes"]

        self.assertIn("mano can be explained as the thinking mind", notes)
        self.assertIn("citta is the feeling mind", notes)
        self.assertIn("counter or displace active distractions", notes)
        self.assertIn("not treat that as identical to the final wearing away of outflows", notes)


if __name__ == "__main__":
    unittest.main()
