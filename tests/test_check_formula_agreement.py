from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tests.helpers import load_module


check = load_module("check_formula_agreement", "scripts/check_formula_agreement.py")


def record(key: str, *phrases: tuple[str, str]) -> dict[str, object]:
    return {
        "term": key,
        "normalized_term": key,
        "example_phrases": [{"pali": pali, "translation": translation} for pali, translation in phrases],
    }


class NormalizationTests(unittest.TestCase):
    def test_anusvara_spellings_fold_to_one_phrase(self) -> None:
        # Records write the anusvāra both ways; without folding, the same
        # formula looks like two unrelated phrases and never gets compared.
        self.assertEqual(
            check.normalize_pali("vivekajaṁ pītisukhaṁ"),
            check.normalize_pali("Vivekajaṃ pītisukhaṃ."),
        )

    def test_punctuation_and_spacing_do_not_split_a_phrase(self) -> None:
        self.assertEqual(check.normalize_pali("sabbe  saṅkhārā, aniccā"), "sabbe saṅkhārā aniccā")


class DisagreementTests(unittest.TestCase):
    def test_agreeing_copies_are_silent(self) -> None:
        terms = {
            "piti": record("piti", ("vivekajaṃ pītisukhaṃ", "rejoicing and satisfaction born of seclusion")),
            "sukha": record("sukha", ("vivekajaṁ pītisukhaṁ", "Rejoicing and satisfaction born of seclusion")),
        }
        unexplained, waived = check.collect_disagreements(terms)
        self.assertEqual((unexplained, waived), ([], []))

    def test_disagreeing_copies_are_reported_with_every_rendering(self) -> None:
        terms = {
            "piti": record("piti", ("vivekajaṃ pītisukhaṃ", "rejoicing and satisfaction born of seclusion")),
            "sukha": record("sukha", ("vivekajaṃ pītisukhaṃ", "delight and satisfaction born of seclusion")),
            "jhana": record("jhana", ("paṭhamaṃ jhānaṃ", "the first mental theme")),
        }
        unexplained, _waived = check.collect_disagreements(terms)
        self.assertEqual(len(unexplained), 1)
        self.assertEqual(unexplained[0]["records"], ["piti", "sukha"])
        self.assertEqual(len(unexplained[0]["renderings"]), 2)

    def test_a_scoped_exception_waives_the_disagreement(self) -> None:
        terms = {
            "piti": record("piti", ("vivekajaṃ pītisukhaṃ", "rejoicing and satisfaction born of seclusion")),
            "sukha": record("sukha", ("vivekajaṃ pītisukhaṃ", "delight and satisfaction born of seclusion")),
        }
        exceptions = {
            check.normalize_pali("vivekajaṃ pītisukhaṃ"): {
                "pali": "vivekajaṃ pītisukhaṃ",
                "records": ["piti", "sukha"],
                "rationale": "sukha quotes the formula under its own contrast rule",
            }
        }
        unexplained, waived = check.collect_disagreements(terms, exceptions)
        self.assertEqual(unexplained, [])
        self.assertEqual(len(waived), 1)
        self.assertIn("contrast rule", waived[0]["rationale"])

    def test_an_exception_does_not_cover_a_record_it_does_not_name(self) -> None:
        # A new copy of the formula drifted after the exception was written:
        # the waiver must not silently stretch to cover it.
        terms = {
            "piti": record("piti", ("vivekajaṃ pītisukhaṃ", "rejoicing and satisfaction born of seclusion")),
            "sukha": record("sukha", ("vivekajaṃ pītisukhaṃ", "delight and satisfaction born of seclusion")),
            "jhana": record("jhana", ("vivekajaṃ pītisukhaṃ", "rapture and ease born of seclusion")),
        }
        exceptions = {
            check.normalize_pali("vivekajaṃ pītisukhaṃ"): {
                "pali": "vivekajaṃ pītisukhaṃ",
                "records": ["piti", "sukha"],
                "rationale": "scoped to two records",
            }
        }
        unexplained, waived = check.collect_disagreements(terms, exceptions)
        self.assertEqual(waived, [])
        self.assertEqual(unexplained[0]["exception_gap"], ["jhana"])


class ExceptionFileTests(unittest.TestCase):
    def test_missing_file_means_no_exceptions(self) -> None:
        self.assertEqual(check.load_exceptions(Path("does-not-exist.json")), {})

    def test_an_exception_without_a_rationale_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "formula-exceptions.json"
            path.write_text(json.dumps({"exceptions": [{"pali": "x y", "records": ["a"]}]}), encoding="utf-8")
            with self.assertRaises(ValueError):
                check.load_exceptions(path)

    def test_exceptions_are_keyed_by_normalized_pali(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "formula-exceptions.json"
            path.write_text(
                json.dumps({"exceptions": [{"pali": "Vivekajaṁ pītisukhaṁ", "rationale": "why"}]}),
                encoding="utf-8",
            )
            loaded = check.load_exceptions(path)
        self.assertIn(check.normalize_pali("vivekajaṃ pītisukhaṃ"), loaded)


if __name__ == "__main__":
    unittest.main()
