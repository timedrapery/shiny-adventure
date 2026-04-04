from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def load_term(path: str) -> dict[str, object]:
    with (REPO_ROOT / path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


class ExperienceProcessPolicyTests(unittest.TestCase):
    def test_headword_defaults_are_governed(self) -> None:
        phassa = load_term("terms/major/phassa.json")
        vedana = load_term("terms/major/vedana.json")
        sanna = load_term("terms/major/sanna.json")
        cetana = load_term("terms/major/cetana.json")
        vinnana = load_term("terms/major/vinnana.json")

        self.assertEqual(phassa["preferred_translation"], "contact")
        self.assertEqual(vedana["preferred_translation"], "felt experience")
        self.assertEqual(sanna["preferred_translation"], "recognition")
        self.assertEqual(cetana["preferred_translation"], "intention")
        self.assertEqual(vinnana["preferred_translation"], "knowing")

    def test_phassa_is_not_left_as_touch_or_sensation(self) -> None:
        phassa = load_term("terms/major/phassa.json")

        self.assertIn("sensation", phassa["discouraged_translations"])
        self.assertIn("encounter", phassa["discouraged_translations"])
        self.assertIn("bodily touch", phassa["translation_policy"]["when_not_to_apply"])

    def test_vedana_is_not_flattened_into_emotion_or_mood(self) -> None:
        vedana = load_term("terms/major/vedana.json")
        mixed = load_term("terms/minor/adukkhamasukha-vedana.json")

        self.assertIn("emotion", vedana["discouraged_translations"])
        self.assertIn("mood", vedana["discouraged_translations"])
        self.assertIn("felt experience", vedana["translation_policy"]["default_scope"])
        self.assertIn("mixed", vedana["definition"])
        self.assertEqual(mixed["preferred_translation"], "mixed feeling")

    def test_sanna_is_not_flattened_into_thought_or_concept(self) -> None:
        sanna = load_term("terms/major/sanna.json")

        self.assertIn("thought", sanna["discouraged_translations"])
        self.assertIn("concept", sanna["discouraged_translations"])
        self.assertIn("memory", sanna["discouraged_translations"])

    def test_cetana_is_not_treated_as_desire_or_willpower(self) -> None:
        cetana = load_term("terms/major/cetana.json")
        nutriment = load_term("terms/major/manosancetana-ahara.json")

        self.assertIn("desire", cetana["discouraged_translations"])
        self.assertIn("willpower", cetana["discouraged_translations"])
        self.assertEqual(nutriment["preferred_translation"], "mental-intention nutriment")

    def test_vinnana_is_not_left_open_to_self_or_awareness_metaphysics(self) -> None:
        vinnana = load_term("terms/major/vinnana.json")

        self.assertIn("self", vinnana["discouraged_translations"])
        self.assertIn("soul", vinnana["discouraged_translations"])
        self.assertIn("pure awareness", vinnana["discouraged_translations"])
        self.assertIn("knowing", vinnana["translation_policy"]["default_scope"])

    def test_formula_record_preserves_phassa_vedana_distinction(self) -> None:
        formula = load_term("terms/minor/phassapaccaya-vedana.json")

        self.assertEqual(formula["preferred_translation"], "with contact as condition, felt experience")
        self.assertIn("emotion", formula["translation_policy"]["when_not_to_apply"])


if __name__ == "__main__":
    unittest.main()
