from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def load_term(path: str) -> dict[str, object]:
    with (REPO_ROOT / path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


class CravingAppropriationPolicyTests(unittest.TestCase):
    def test_target_headwords_have_expected_defaults(self) -> None:
        upadana = load_term("terms/major/upadana.json")
        tanha = load_term("terms/major/tanha.json")
        chanda = load_term("terms/major/chanda.json")
        raga = load_term("terms/major/raga.json")
        nandi = load_term("terms/major/nandi.json")

        self.assertEqual(upadana["preferred_translation"], "taking personally")
        self.assertEqual(tanha["preferred_translation"], "ignorant wanting")
        self.assertEqual(chanda["preferred_translation"], "desire")
        self.assertEqual(raga["preferred_translation"], "passion")
        self.assertEqual(nandi["preferred_translation"], "relishing")

    def test_chanda_is_not_collapsed_into_tanha(self) -> None:
        chanda = load_term("terms/major/chanda.json")
        tanha = load_term("terms/major/tanha.json")

        self.assertIn("craving", chanda["discouraged_translations"])
        self.assertIn("desire", tanha["discouraged_translations"])
        self.assertIn("broader than taṇhā", chanda["notes"])

    def test_upadana_is_not_left_as_vague_attachment(self) -> None:
        upadana = load_term("terms/major/upadana.json")
        formula = load_term("terms/minor/tanhapaccaya-upadana.json")

        self.assertIn("attachment", upadana["discouraged_translations"])
        self.assertEqual(formula["preferred_translation"], "with ignorant wanting as condition, taking personally")
        self.assertIn("generic attachment language", formula["translation_policy"]["when_not_to_apply"])

    def test_raga_and_nandi_do_not_collapse_into_generic_pleasure_or_desire(self) -> None:
        raga = load_term("terms/major/raga.json")
        nandi = load_term("terms/major/nandi.json")
        phrase = load_term("terms/minor/nandiraga-sahagata.json")

        self.assertIn("desire", raga["discouraged_translations"])
        self.assertIn("pleasure", nandi["discouraged_translations"])
        self.assertEqual(phrase["preferred_translation"], "accompanied by relishing and passion")

    def test_upadana_heap_override_stays_stable(self) -> None:
        upadanakkhandha = load_term("terms/minor/upadanakkhandha.json")
        pancupadanakkhandha = load_term("terms/minor/pancupadanakkhandha.json")

        self.assertEqual(upadanakkhandha["preferred_translation"], "clung-to heap")
        self.assertEqual(pancupadanakkhandha["preferred_translation"], "five clung-to heaps")


if __name__ == "__main__":
    unittest.main()
