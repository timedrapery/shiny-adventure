from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def load_term(path: str) -> dict[str, object]:
    with (REPO_ROOT / path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


class OsfReconciliationPolicyTests(unittest.TestCase):
    def test_sati_aligns_with_osf_remembering_and_blocks_bare_attention_drift(self) -> None:
        sati = load_term("terms/major/sati.json")

        self.assertEqual(sati["preferred_translation"], "remembering")
        self.assertIn("mindfulness", sati["discouraged_translations"])
        self.assertIn("bare attention", sati["discouraged_translations"])
        self.assertIn("ALIGN case", sati["notes"])

    def test_nibbana_keeps_house_default_and_tolerates_cooling_language(self) -> None:
        nibbana = load_term("terms/major/nibbana.json")

        self.assertEqual(nibbana["preferred_translation"], "nibbāna")
        self.assertTrue(nibbana["untranslated_preferred"])
        self.assertIn("coolness", nibbana["alternative_translations"])
        self.assertIn("ultimate reality", nibbana["discouraged_translations"])

    def test_nirodha_stays_quenching_while_allowing_osf_stopping_language(self) -> None:
        nirodha = load_term("terms/major/nirodha.json")

        self.assertEqual(nirodha["preferred_translation"], "quenching")
        self.assertIn("ending", nirodha["alternative_translations"])
        self.assertIn("cessation", nirodha["alternative_translations"])
        self.assertIn("annihilation", nirodha["discouraged_translations"])

    def test_vimutti_keeps_release_and_controls_liberation(self) -> None:
        vimutti = load_term("terms/major/vimutti.json")

        self.assertEqual(vimutti["preferred_translation"], "release")
        self.assertIn("liberation", vimutti["alternative_translations"])
        self.assertIn("salvation", vimutti["discouraged_translations"])
        self.assertIn("TOLERATE-ALTERNATE case", vimutti["notes"])

    def test_sunnata_aligns_with_emptiness_and_blocks_nihilism(self) -> None:
        sunnata = load_term("terms/major/sunnata.json")

        self.assertEqual(sunnata["preferred_translation"], "emptiness")
        self.assertIn("voidness", sunnata["alternative_translations"])
        self.assertIn("nothingness", sunnata["discouraged_translations"])
        self.assertIn("mystical oneness", sunnata["discouraged_translations"])


if __name__ == "__main__":
    unittest.main()
