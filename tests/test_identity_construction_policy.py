from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def load_term(path: str) -> dict[str, object]:
    with (REPO_ROOT / path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


class IdentityConstructionPolicyTests(unittest.TestCase):
    def test_clung_to_heaps_rendering_stays_stable(self) -> None:
        term = load_term("terms/minor/pancupadanakkhandha.json")
        self.assertEqual(term["preferred_translation"], "five clung-to heaps")

    def test_upadana_family_alignment_is_explicit(self) -> None:
        upadana = load_term("terms/major/upadana.json")
        ditthupadana = load_term("terms/major/ditthupadana.json")
        attavadupadana = load_term("terms/major/attavadupadana.json")
        upadanakkhandha = load_term("terms/minor/upadanakkhandha.json")

        self.assertEqual(upadana["preferred_translation"], "taking personally")
        self.assertEqual(ditthupadana["preferred_translation"], "taking views personally")
        self.assertEqual(attavadupadana["preferred_translation"], "taking self-doctrine personally")
        self.assertEqual(upadanakkhandha["preferred_translation"], "clung-to heap")

    def test_mana_and_asmimana_are_distinct(self) -> None:
        mana = load_term("terms/major/mana.json")
        asmimana = load_term("terms/major/asmimana.json")

        self.assertEqual(mana["preferred_translation"], "conceit")
        self.assertEqual(asmimana["preferred_translation"], "conceit 'I am'")
        self.assertIn("pride", mana["discouraged_translations"])
        self.assertIn("ego", asmimana["discouraged_translations"])

    def test_ditthi_and_ditthupadana_are_distinct(self) -> None:
        ditthi = load_term("terms/major/ditthi.json")
        ditthupadana = load_term("terms/major/ditthupadana.json")

        self.assertEqual(ditthi["preferred_translation"], "view")
        self.assertEqual(ditthupadana["preferred_translation"], "taking views personally")
        self.assertIn("wrong view", ditthi["discouraged_translations"])

    def test_sakkaya_prefers_identity_with_personal_identity_as_controlled_alternate(self) -> None:
        sakkaya = load_term("terms/major/sakkaya.json")
        self.assertEqual(sakkaya["preferred_translation"], "identity")
        self.assertIn("personal identity", sakkaya["alternative_translations"])
        self.assertIn("self", sakkaya["discouraged_translations"])


if __name__ == "__main__":
    unittest.main()
