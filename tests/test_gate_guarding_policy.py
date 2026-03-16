from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def load_term(path: str) -> dict[str, object]:
    with (REPO_ROOT / path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


class GateGuardingPolicyTests(unittest.TestCase):
    def test_sati_keeps_gatekeeper_practice_frame(self) -> None:
        sati = load_term("terms/major/sati.json")

        self.assertEqual(sati["preferred_translation"], "remembering")
        self.assertIn("gatekeeper", sati["notes"])
        self.assertTrue(any("sense-door guarding" in rule["context"] for rule in sati["context_rules"]))

    def test_phassa_marks_the_early_practical_pivot(self) -> None:
        phassa = load_term("terms/major/phassa.json")

        self.assertEqual(phassa["preferred_translation"], "contact")
        self.assertIn("earliest practical pivot", phassa["notes"])
        self.assertIn("OSF dhamma interaction on guarding the gate", [item["source"] for item in phassa["authority_basis"]])

    def test_samvara_and_indriya_samvara_block_interior_fixing_language(self) -> None:
        samvara = load_term("terms/major/samvara.json")
        indriya_samvara = load_term("terms/minor/indriya-samvara.json")

        self.assertIn("good administration at the gate", samvara["notes"])
        self.assertIn("diagnostic-code language", indriya_samvara["notes"])
        self.assertEqual(indriya_samvara["preferred_translation"], "guarding the faculties")

    def test_luminous_mind_record_supports_non_moralized_practice_explanation(self) -> None:
        pabhassara_citta = load_term("terms/minor/pabhassara-citta.json")

        self.assertEqual(pabhassara_citta["preferred_translation"], "luminous mind")
        self.assertIn("visitors or invasions", pabhassara_citta["notes"])
        self.assertIn("AN 1.49-52", pabhassara_citta["sutta_references"])

    def test_vedana_to_tanha_formula_keeps_early_interception_note(self) -> None:
        formula = load_term("terms/minor/vedanapaccaya-tanha.json")

        self.assertIn("early interception", formula["notes"])
        self.assertIn("need not simply continue by default", formula["notes"])


if __name__ == "__main__":
    unittest.main()
