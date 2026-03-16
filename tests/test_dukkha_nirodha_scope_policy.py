from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def load_term(path: str) -> dict[str, object]:
    with (REPO_ROOT / path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


class DukkhaNirodhaScopePolicyTests(unittest.TestCase):
    def test_dukkha_and_nirodha_notes_encode_sn_22_86_scope(self) -> None:
        dukkha = load_term("terms/major/dukkha.json")
        nirodha = load_term("terms/major/nirodha.json")

        self.assertEqual(dukkha["preferred_translation"], "dissatisfaction")
        self.assertIn("SN 22.86", dukkha["notes"])
        self.assertIn("only dissatisfaction and the ending of dissatisfaction", dukkha["notes"])
        self.assertEqual(nirodha["preferred_translation"], "quenching")
        self.assertIn("SN 22.86", nirodha["notes"])

    def test_ariyasacca_notes_treat_dukkha_nirodha_as_governing_scope(self) -> None:
        ariyasacca = load_term("terms/major/ariyasacca.json")

        self.assertEqual(ariyasacca["preferred_translation"], "noble truth")
        self.assertIn("SN 22.86", ariyasacca["notes"])
        self.assertIn("dukkha / dukkha-nirodha scope", ariyasacca["notes"])


if __name__ == "__main__":
    unittest.main()
