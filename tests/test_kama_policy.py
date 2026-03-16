from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def load_term(path: str) -> dict[str, object]:
    with (REPO_ROOT / path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


class KamaPolicyTests(unittest.TestCase):
    def test_kama_headword_is_governed_as_sensuality(self) -> None:
        kama = load_term("terms/major/kama.json")

        self.assertEqual(kama["preferred_translation"], "sensuality")
        self.assertIn("desire", kama["discouraged_translations"])
        self.assertIn("pleasure", kama["discouraged_translations"])
        self.assertIn("sex", kama["discouraged_translations"])

    def test_kamacchanda_stays_distinct_from_plain_chanda(self) -> None:
        kamacchanda = load_term("terms/major/kamacchanda.json")
        chanda = load_term("terms/major/chanda.json")

        self.assertEqual(kamacchanda["preferred_translation"], "sensual distraction")
        self.assertEqual(chanda["preferred_translation"], "desire")
        self.assertIn("interest", kamacchanda["discouraged_translations"])
        self.assertIn("five-distractions framework", kamacchanda["notes"])

    def test_kama_cluster_support_terms_preserve_distinctions(self) -> None:
        kama_tanha = load_term("terms/major/kama-tanha.json")
        kama_raga = load_term("terms/major/kama-raga.json")
        kamupadana = load_term("terms/major/kamupadana.json")

        self.assertEqual(kama_tanha["preferred_translation"], "ignorant wanting for sensuality")
        self.assertEqual(kama_raga["preferred_translation"], "passion for sensuality")
        self.assertEqual(kamupadana["preferred_translation"], "sensual clinging")
        self.assertIn("sexual desire", kama_tanha["discouraged_translations"])
        self.assertIn("sexual desire", kama_raga["discouraged_translations"])
        self.assertIn("attachment to pleasure", kamupadana["discouraged_translations"])

    def test_explicitly_sexual_record_remains_narrower_than_kama_headword(self) -> None:
        kama = load_term("terms/major/kama.json")
        sexual = load_term("terms/minor/kamesu-micchacara.json")

        self.assertEqual(kama["preferred_translation"], "sensuality")
        self.assertEqual(sexual["preferred_translation"], "sexual misconduct")
        self.assertIn("should not be used to back-project a sexual default", sexual["notes"])


if __name__ == "__main__":
    unittest.main()
