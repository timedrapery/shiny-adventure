from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def load_term(path: str) -> dict[str, object]:
    with (REPO_ROOT / path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


class ConsummationInterfacePolicyTests(unittest.TestCase):
    def test_target_defaults_are_distinct(self) -> None:
        nibbana = load_term("terms/major/nibbana.json")
        amata = load_term("terms/major/amata.json")
        asankhata = load_term("terms/major/asankhata.json")
        santi = load_term("terms/major/santi.json")
        nibbuta = load_term("terms/major/nibbuta.json")
        parinibbana = load_term("terms/major/parinibbana.json")

        self.assertEqual(nibbana["preferred_translation"], "nibbāna")
        self.assertEqual(amata["preferred_translation"], "deathless")
        self.assertEqual(asankhata["preferred_translation"], "unconditioned")
        self.assertEqual(santi["preferred_translation"], "peace")
        self.assertEqual(nibbuta["preferred_translation"], "cooled")
        self.assertEqual(parinibbana["preferred_translation"], "final nibbāna")

    def test_nibbana_and_vimutti_do_not_collapse(self) -> None:
        nibbana = load_term("terms/major/nibbana.json")
        vimutti = load_term("terms/major/vimutti.json")

        self.assertIn("mere cessation", nibbana["discouraged_translations"])
        self.assertIn("nibbana", vimutti["related_terms"])

    def test_amata_and_asankhata_stay_distinct(self) -> None:
        amata = load_term("terms/major/amata.json")
        asankhata = load_term("terms/major/asankhata.json")

        self.assertIn("nibbāna", amata["discouraged_translations"])
        self.assertIn("nibbāna", asankhata["discouraged_translations"])

    def test_santi_stays_distinct_from_passaddhi(self) -> None:
        santi = load_term("terms/major/santi.json")
        upasama = load_term("terms/minor/upasama.json")

        self.assertIn("relaxation", santi["discouraged_translations"])
        self.assertEqual(upasama["preferred_translation"], "calming")

    def test_nibbuta_stays_distinct_from_nibbana(self) -> None:
        nibbuta = load_term("terms/major/nibbuta.json")

        self.assertIn("nibbāna", nibbuta["discouraged_translations"])
        self.assertIn("cooled", nibbuta["preferred_translation"])

    def test_supporting_compounds_are_governed(self) -> None:
        amatapada = load_term("terms/minor/amatapada.json")
        asankhata_dhatu = load_term("terms/minor/asankhata-dhatu.json")
        nibbana_dhatu = load_term("terms/minor/nibbana-dhatu.json")

        self.assertEqual(amatapada["preferred_translation"], "path to the deathless")
        self.assertEqual(asankhata_dhatu["preferred_translation"], "unconditioned element")
        self.assertEqual(nibbana_dhatu["preferred_translation"], "nibbāna element")


if __name__ == "__main__":
    unittest.main()
