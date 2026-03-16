from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def load_term(path: str) -> dict[str, object]:
    with (REPO_ROOT / path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


class VerbalKnowingPolicyTests(unittest.TestCase):
    def test_janati_and_pajanati_are_distinct(self) -> None:
        janati = load_term("terms/major/janati.json")
        pajanati = load_term("terms/major/pajanati.json")

        self.assertEqual(janati["preferred_translation"], "knows")
        self.assertEqual(pajanati["preferred_translation"], "discerns")
        self.assertIn("realizes", janati["discouraged_translations"])
        self.assertIn("comprehends fully", pajanati["discouraged_translations"])

    def test_pajanati_and_parinna_do_not_flatten(self) -> None:
        pajanati = load_term("terms/major/pajanati.json")
        parinna = load_term("terms/major/parinna.json")

        self.assertEqual(pajanati["preferred_translation"], "discerns")
        self.assertEqual(parinna["preferred_translation"], "full understanding")
        self.assertNotEqual(pajanati["preferred_translation"], parinna["preferred_translation"])

    def test_sanjanati_stays_distinct_from_generic_knowing(self) -> None:
        sanjanati = load_term("terms/major/sanjanati.json")
        janati = load_term("terms/major/janati.json")

        self.assertEqual(sanjanati["preferred_translation"], "recognizes")
        self.assertIn("knows", sanjanati["discouraged_translations"])
        self.assertNotEqual(sanjanati["preferred_translation"], janati["preferred_translation"])

    def test_anna_stays_distinct_from_nana_and_vijja(self) -> None:
        anna = load_term("terms/major/anna.json")
        nana = load_term("terms/major/nana.json")
        vijja = load_term("terms/major/vijja.json")

        self.assertEqual(anna["preferred_translation"], "final knowledge")
        self.assertEqual(nana["preferred_translation"], "knowledge")
        self.assertEqual(vijja["preferred_translation"], "clear knowledge")
        self.assertIn("realization", anna["discouraged_translations"])

    def test_noun_and_verb_families_are_cross_linked(self) -> None:
        janati = load_term("terms/major/janati.json")
        pajanati = load_term("terms/major/pajanati.json")
        sanjanati = load_term("terms/major/sanjanati.json")
        anna = load_term("terms/major/anna.json")

        self.assertIn("nana", janati["related_terms"])
        self.assertIn("panna", pajanati["related_terms"])
        self.assertIn("sanna", sanjanati["related_terms"])
        self.assertIn("nana", anna["related_terms"])

    def test_formula_records_preserve_pajanati_policy(self) -> None:
        yathabhutam = load_term("terms/minor/yathabhutam-pajanati.json")
        naparam = load_term("terms/minor/naparam-itthattayati-pajanati.json")

        self.assertEqual(yathabhutam["preferred_translation"], "discerns it as it has come to be")
        self.assertEqual(naparam["preferred_translation"], "one discerns: there is no more of this state of being")
        self.assertIn("realizes reality", yathabhutam["discouraged_translations"])

    def test_cluster_integrates_external_checkpoints_without_changing_defaults(self) -> None:
        pajanati = load_term("terms/major/pajanati.json")
        sanjanati = load_term("terms/major/sanjanati.json")

        pajanati_sources = {item["source"] for item in pajanati["authority_basis"]}
        sanjanati_sources = {item["source"] for item in sanjanati["authority_basis"]}

        self.assertEqual(pajanati["preferred_translation"], "discerns")
        self.assertEqual(sanjanati["preferred_translation"], "recognizes")
        self.assertIn("Punnaji usage profile", pajanati_sources)
        self.assertIn("Hillside / Ñāṇamoli usage profile", pajanati_sources)
        self.assertIn("Hillside / Ñāṇamoli usage profile", sanjanati_sources)


if __name__ == "__main__":
    unittest.main()
