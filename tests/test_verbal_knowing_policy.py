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

    def test_abhijanati_stays_distinct_from_other_knowing_verbs(self) -> None:
        abhijanati = load_term("terms/major/abhijanati.json")
        janati = load_term("terms/major/janati.json")
        pajanati = load_term("terms/major/pajanati.json")
        sanjanati = load_term("terms/major/sanjanati.json")

        self.assertEqual(abhijanati["preferred_translation"], "directly knows")
        self.assertIn("recognizes", abhijanati["discouraged_translations"])
        self.assertIn("discerns", abhijanati["discouraged_translations"])
        self.assertNotEqual(abhijanati["preferred_translation"], janati["preferred_translation"])
        self.assertNotEqual(abhijanati["preferred_translation"], pajanati["preferred_translation"])
        self.assertNotEqual(abhijanati["preferred_translation"], sanjanati["preferred_translation"])

    def test_mannati_stays_distinct_from_generic_thinking_and_links_to_selfing(self) -> None:
        mannati = load_term("terms/major/mannati.json")

        self.assertEqual(mannati["preferred_translation"], "takes to be")
        self.assertIn("thinks", mannati["discouraged_translations"])
        self.assertIn("asmimana", mannati["related_terms"])
        self.assertIn("upadana", mannati["related_terms"])

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
        abhijanati = load_term("terms/major/abhijanati.json")
        pajanati = load_term("terms/major/pajanati.json")
        sanjanati = load_term("terms/major/sanjanati.json")
        mannati = load_term("terms/major/mannati.json")
        anna = load_term("terms/major/anna.json")

        self.assertIn("nana", janati["related_terms"])
        self.assertIn("abhijanati", janati["related_terms"])
        self.assertIn("abhinna", abhijanati["related_terms"])
        self.assertIn("panna", pajanati["related_terms"])
        self.assertIn("sanna", sanjanati["related_terms"])
        self.assertIn("vitakka", sanjanati["related_terms"])
        self.assertIn("mannati", sanjanati["related_terms"])
        self.assertIn("asmimana", mannati["related_terms"])
        self.assertIn("nana", anna["related_terms"])

    def test_formula_records_preserve_pajanati_policy(self) -> None:
        yathabhutam = load_term("terms/minor/yathabhutam-pajanati.json")
        naparam = load_term("terms/minor/naparam-itthattayati-pajanati.json")

        self.assertEqual(yathabhutam["preferred_translation"], "discerns it as it has come to be")
        self.assertEqual(naparam["preferred_translation"], "one discerns: there is no more of this state of being")
        self.assertIn("realizes reality", yathabhutam["discouraged_translations"])

    def test_mn1_formula_records_preserve_direct_knowing_and_selfing_pattern(self) -> None:
        recognized_selfing = load_term("terms/minor/pathavim-pathavito-sannatva-pathavim-mannati.json")
        direct_knowing_prohibitive = load_term("terms/minor/pathavim-pathavito-abhinnaya-pathavim-ma-manni.json")
        direct_knowing_nonselfing = load_term("terms/minor/pathavim-pathavito-abhinnaya-pathavim-na-mannati.json")
        delight_root = load_term("terms/minor/nandi-dukkhassa-mulan.json")
        becoming_line = load_term("terms/minor/bhava-jati-bhutassa-jaramaranam.json")

        self.assertEqual(
            recognized_selfing["preferred_translation"],
            "having recognized earth as earth, one takes oneself to be earth",
        )
        self.assertEqual(
            direct_knowing_prohibitive["preferred_translation"],
            "having directly known earth as earth, one should not take oneself to be earth",
        )
        self.assertEqual(
            direct_knowing_nonselfing["preferred_translation"],
            "having directly known earth as earth, one does not take oneself to be earth",
        )
        self.assertEqual(delight_root["preferred_translation"], "delight is the root of dissatisfaction")
        self.assertEqual(
            becoming_line["preferred_translation"],
            "with becoming there is birth, and for whatever has come to be there are aging and death",
        )

    def test_mn18_formula_records_preserve_recognition_thinking_and_proliferation_pattern(self) -> None:
        felt_recognition = load_term("terms/minor/yam-vedeti-tam-sanjanati.json")
        recognition_thinking = load_term("terms/minor/yam-sanjanati-tam-vitakketi.json")
        thinking_proliferation = load_term("terms/minor/yam-vitakketi-tam-papanceti.json")
        proliferation_overrun = load_term(
            "terms/minor/yam-papanceti-tato-nidanam-purisam-papanca-sanna-sankha-samudacaranti.json"
        )
        papanca_sanna_sankha = load_term("terms/minor/papanca-sanna-sankha.json")

        self.assertEqual(felt_recognition["preferred_translation"], "what one feels, one recognizes")
        self.assertEqual(recognition_thinking["preferred_translation"], "what one recognizes, one thinks about")
        self.assertEqual(thinking_proliferation["preferred_translation"], "what one thinks about, one proliferates about")
        self.assertEqual(
            proliferation_overrun["preferred_translation"],
            "from what one proliferates about as the source, the recognitions and notions of proliferation sweep over a person",
        )
        self.assertEqual(papanca_sanna_sankha["preferred_translation"], "recognitions and notions of proliferation")

    def test_cluster_integrates_external_checkpoints_without_changing_defaults(self) -> None:
        pajanati = load_term("terms/major/pajanati.json")
        sanjanati = load_term("terms/major/sanjanati.json")

        pajanati_sources = {item["source"] for item in pajanati["authority_basis"]}
        sanjanati_sources = {item["source"] for item in sanjanati["authority_basis"]}

        self.assertEqual(pajanati["preferred_translation"], "discerns")
        self.assertEqual(sanjanati["preferred_translation"], "recognizes")
        self.assertIn("Punnaji usage profile", pajanati_sources)
        self.assertTrue(any("Hillside" in source for source in pajanati_sources))
        self.assertTrue(any("Hillside" in source for source in sanjanati_sources))

    def test_mn1_headwords_are_stabilized_in_terms(self) -> None:
        abhijanati = load_term("terms/major/abhijanati.json")
        mannati = load_term("terms/major/mannati.json")

        abhijanati_sources = {item["source"] for item in abhijanati["authority_basis"]}
        mannati_sources = {item["source"] for item in mannati["authority_basis"]}

        self.assertEqual(abhijanati["preferred_translation"], "directly knows")
        self.assertEqual(mannati["preferred_translation"], "takes to be")
        self.assertIn("MN 1", abhijanati_sources)
        self.assertIn("MN 1", mannati_sources)


if __name__ == "__main__":
    unittest.main()
