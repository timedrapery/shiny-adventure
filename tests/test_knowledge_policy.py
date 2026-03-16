from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def load_term(path: str) -> dict[str, object]:
    with (REPO_ROOT / path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


class KnowledgePolicyTests(unittest.TestCase):
    def test_nana_and_panna_are_distinct(self) -> None:
        nana = load_term("terms/major/nana.json")
        panna = load_term("terms/major/panna.json")

        self.assertEqual(nana["preferred_translation"], "knowledge")
        self.assertEqual(panna["preferred_translation"], "discernment")
        self.assertIn("insight", nana["discouraged_translations"])
        self.assertIn("insight", panna["discouraged_translations"])

    def test_vijja_is_not_generic_knowledge_or_information(self) -> None:
        vijja = load_term("terms/major/vijja.json")
        avijja = load_term("terms/major/avijja.json")

        self.assertEqual(vijja["preferred_translation"], "clear knowledge")
        self.assertIn("science", vijja["discouraged_translations"])
        self.assertIn("information", vijja["discouraged_translations"])
        self.assertIn("vijja", avijja["related_terms"])

    def test_panna_stays_distinct_from_view(self) -> None:
        panna = load_term("terms/major/panna.json")
        ditthi = load_term("terms/major/ditthi.json")

        self.assertEqual(ditthi["preferred_translation"], "view")
        self.assertIn("ditthi", panna["related_terms"])
        self.assertNotEqual(panna["preferred_translation"], ditthi["preferred_translation"])

    def test_dassana_is_not_mystical_vision(self) -> None:
        dassana = load_term("terms/major/dassana.json")

        self.assertEqual(dassana["preferred_translation"], "seeing")
        self.assertIn("mystical vision", dassana["discouraged_translations"])

    def test_abhinna_and_parinna_do_not_flatten(self) -> None:
        abhinna = load_term("terms/major/abhinna.json")
        parinna = load_term("terms/major/parinna.json")

        self.assertEqual(abhinna["preferred_translation"], "higher knowing")
        self.assertIn("occult power", abhinna["discouraged_translations"])
        self.assertEqual(parinna["preferred_translation"], "full understanding")
        self.assertIn("understanding", parinna["discouraged_translations"])

    def test_sampajanna_stays_distinct_from_sati(self) -> None:
        sampajanna = load_term("terms/major/sampajanna.json")
        sati = load_term("terms/major/sati.json")

        self.assertEqual(sampajanna["preferred_translation"], "clear knowing")
        self.assertEqual(sati["preferred_translation"], "remembering")
        self.assertIn("mindfulness", sampajanna["discouraged_translations"])

    def test_compounds_preserve_knowing_and_seeing_distinction(self) -> None:
        nanadassana = load_term("terms/minor/nanadassana.json")
        vimutti_nanadassana = load_term("terms/minor/vimutti-nanadassana.json")

        self.assertEqual(nanadassana["preferred_translation"], "knowing and seeing")
        self.assertEqual(vimutti_nanadassana["preferred_translation"], "knowing and seeing of release")
        self.assertIn("mystical experience", vimutti_nanadassana["discouraged_translations"])

    def test_cluster_integrates_hillside_checkpoint_without_changing_defaults(self) -> None:
        nana = load_term("terms/major/nana.json")
        sampajanna = load_term("terms/major/sampajanna.json")

        nana_sources = {item["source"] for item in nana["authority_basis"]}
        sampajanna_sources = {item["source"] for item in sampajanna["authority_basis"]}

        self.assertEqual(nana["preferred_translation"], "knowledge")
        self.assertEqual(sampajanna["preferred_translation"], "clear knowing")
        self.assertIn("Hillside / Ñāṇamoli usage profile", nana_sources)
        self.assertIn("Hillside / Ñāṇamoli usage profile", sampajanna_sources)


if __name__ == "__main__":
    unittest.main()
