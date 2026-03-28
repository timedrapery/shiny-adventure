from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def load_term(path: str) -> dict[str, object]:
    with (REPO_ROOT / path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


class IdappaccayataSourceIntegrationPolicyTests(unittest.TestCase):
    def test_idappaccayata_keeps_conditionality_default_and_blocks_rhetorical_drift(self) -> None:
        term = load_term("terms/major/idappaccayata.json")

        self.assertEqual(term["preferred_translation"], "conditionality")
        self.assertIn("god", term["discouraged_translations"])
        self.assertIn("mere causality", term["discouraged_translations"])
        self.assertIn("law of nature", term["notes"])
        self.assertIn(
            "Idappaccayatā practical talk profile",
            {item["source"] for item in term["authority_basis"]},
        )

    def test_paticcasamuppada_records_same_law_different_scope_support(self) -> None:
        term = load_term("terms/major/paticcasamuppada.json")

        self.assertEqual(term["preferred_translation"], "dependent arising")
        self.assertIn("one law under different scopes", term["notes"])
        self.assertIn(
            "Idappaccayatā practical talk profile",
            {item["source"] for item in term["authority_basis"]},
        )

    def test_kamma_blocks_moral_bookkeeping_drift(self) -> None:
        term = load_term("terms/major/kamma.json")

        self.assertEqual(term["preferred_translation"], "action")
        self.assertIn("bookkeeping", term["notes"])
        self.assertIn("bookkeeping", term["translation_policy"]["when_not_to_apply"])
        self.assertIn(
            "Idappaccayatā practical talk profile",
            {item["source"] for item in term["authority_basis"]},
        )

    def test_tathata_preserves_just_like_that_as_explanatory_only(self) -> None:
        term = load_term("terms/minor/tathata.json")

        self.assertEqual(term["preferred_translation"], "suchness")
        self.assertIn("just like that", term["alternative_translations"])
        self.assertIn("explanatory only", term["notes"])
        self.assertIn(
            "Idappaccayatā practical talk profile",
            {item["source"] for item in term["authority_basis"]},
        )


if __name__ == "__main__":
    unittest.main()
