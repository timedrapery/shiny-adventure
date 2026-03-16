from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def load_term(path: str) -> dict[str, object]:
    with (REPO_ROOT / path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


class EmptinessSignlessWishlessPolicyTests(unittest.TestCase):
    def test_animitta_and_appanihita_are_promoted_major_headwords(self) -> None:
        animitta = load_term("terms/major/animitta.json")
        appanihita = load_term("terms/major/appanihita.json")

        self.assertEqual(animitta["entry_type"], "major")
        self.assertEqual(animitta["status"], "stable")
        self.assertEqual(appanihita["entry_type"], "major")
        self.assertEqual(appanihita["status"], "stable")

    def test_sunnata_stays_distinct_from_anatta_and_nibbana(self) -> None:
        sunnata = load_term("terms/major/sunnata.json")

        self.assertEqual(sunnata["preferred_translation"], "emptiness")
        self.assertIn("nothingness", sunnata["discouraged_translations"])
        self.assertIn("emptiness of self and what belongs to self", sunnata["alternative_translations"])
        self.assertIn("animitta", sunnata["related_terms"])
        self.assertIn("appanihita", sunnata["related_terms"])

    def test_animitta_and_appanihita_have_distinct_defaults(self) -> None:
        animitta = load_term("terms/major/animitta.json")
        appanihita = load_term("terms/major/appanihita.json")

        self.assertEqual(animitta["preferred_translation"], "signless")
        self.assertEqual(appanihita["preferred_translation"], "wishless")
        self.assertIn("formless", animitta["discouraged_translations"])
        self.assertIn("no goals", appanihita["discouraged_translations"])

    def test_appanihita_blocks_passive_no_goals_drift(self) -> None:
        appanihita = load_term("terms/major/appanihita.json")

        self.assertIn("without placing desire", appanihita["alternative_translations"])
        self.assertIn("desireless", appanihita["alternative_translations"])
        self.assertIn("apathetic", appanihita["discouraged_translations"])

    def test_support_compounds_preserve_family_defaults(self) -> None:
        animitta_vimokkha = load_term("terms/minor/animitta-vimokkha.json")
        appanihita_vimokkha = load_term("terms/minor/appanihita-vimokkha.json")
        vimokkhamukha = load_term("terms/minor/vimokkhamukha.json")

        self.assertEqual(animitta_vimokkha["preferred_translation"], "signless release")
        self.assertEqual(appanihita_vimokkha["preferred_translation"], "wishless release")
        self.assertIn("animitta", vimokkhamukha["related_terms"])
        self.assertIn("appanihita", vimokkhamukha["related_terms"])
        self.assertIn("sunnata", vimokkhamukha["related_terms"])


if __name__ == "__main__":
    unittest.main()
