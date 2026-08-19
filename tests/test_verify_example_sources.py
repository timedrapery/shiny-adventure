from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tests.helpers import load_module


verify = load_module("verify_example_sources", "scripts/verify_example_sources.py")


class NormalizeTests(unittest.TestCase):
    def test_diacritics_fold_to_base_letters(self) -> None:
        # The records use `paṭhavi` where the Bilara MS edition has `pathavi`.
        # Folding is what stops that from looking like a bad citation.
        self.assertEqual(verify.normalize("paṭhaviṃ"), verify.normalize("pathaviṁ"))

    def test_niggahita_variants_fold(self) -> None:
        self.assertEqual(verify.normalize("kammaṃ"), verify.normalize("kammaṁ"))

    def test_punctuation_is_stripped(self) -> None:
        self.assertEqual(
            verify.normalize("Cetanāhaṁ, bhikkhave, kammaṁ vadāmi."),
            verify.normalize("cetanāhaṃ bhikkhave kammaṃ vadāmi"),
        )


class SourceUrlTests(unittest.TestCase):
    def test_mn_and_dn_are_flat(self) -> None:
        self.assertTrue(verify.source_url("MN 1").endswith("/mn/mn1_root-pli-ms.json"))
        self.assertTrue(verify.source_url("DN 15").endswith("/dn/dn15_root-pli-ms.json"))

    def test_sn_and_an_are_nested_by_vagga(self) -> None:
        self.assertTrue(
            verify.source_url("SN 12.11").endswith("/sn/sn12/sn12.11_root-pli-ms.json")
        )
        self.assertTrue(
            verify.source_url("AN 6.63").endswith("/an/an6/an6.63_root-pli-ms.json")
        )

    def test_verse_collections_are_unsupported(self) -> None:
        self.assertIsNone(verify.source_url("Dhp 21"))
        self.assertIsNone(verify.source_url("Ud 8.3"))

    def test_unparseable_citation_returns_none(self) -> None:
        self.assertIsNone(verify.source_url("somewhere"))


class CheckPhraseTests(unittest.TestCase):
    HAY = verify.normalize(
        "cattārome bhikkhave āhārā bhūtānaṁ vā sattānaṁ ṭhitiyā "
        "kabaḷīkāro āhāro oḷāriko vā sukhumo vā phasso dutiyo"
    )

    def test_present_phrase_is_ok(self) -> None:
        self.assertEqual(verify.check_phrase("phasso dutiyo", self.HAY), "ok")

    def test_wrong_ending_is_inflected(self) -> None:
        self.assertEqual(verify.check_phrase("phassassa", self.HAY), "inflected")

    def test_right_source_wrong_wording_is_partial(self) -> None:
        # `phasso` is present, `viññāṇaṁ` is not.
        self.assertEqual(verify.check_phrase("phasso viññāṇaṁ", self.HAY), "partial")

    def test_wholly_missing_phrase_is_absent(self) -> None:
        self.assertEqual(verify.check_phrase("anāgāmimagga", self.HAY), "absent")

    def test_abridged_source_downgrades_absent_to_inconclusive(self) -> None:
        self.assertEqual(
            verify.check_phrase("anāgāmimagga", self.HAY, abridged=True), "inconclusive"
        )

    def test_ellipsis_in_citation_is_split_into_chunks(self) -> None:
        self.assertEqual(
            verify.check_phrase("cattārome bhikkhave ... phasso dutiyo", self.HAY), "ok"
        )


class AbridgementTests(unittest.TestCase):
    def test_peyyala_marker_is_detected(self) -> None:
        self.assertTrue(verify.is_abridged("saṅkhāranirodhā viññāṇanirodho …pe…"))

    def test_plain_text_is_not_abridged(self) -> None:
        self.assertFalse(verify.is_abridged("saṅkhāranirodhā viññāṇanirodho"))


class ReportTests(unittest.TestCase):
    def _repo(self, tmp: str):
        root = Path(tmp)
        terms = root / "minor"
        terms.mkdir(parents=True)
        (terms / "x.json").write_text(
            json.dumps(
                {
                    "example_phrases": [
                        {"pali": "phasso dutiyo", "source": "Dhp 21"},
                        {"pali": "no source here"},
                    ]
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        return root, terms

    def test_examples_without_a_source_are_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, terms = self._repo(tmp)
            rows = verify.collect_examples(terms)
        self.assertEqual(len(rows), 1)

    def test_unsupported_collection_needs_no_network(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, terms = self._repo(tmp)
            report = verify.build_report(terms, cache_dir=root / "cache")
        self.assertEqual(report["summary"]["unsupported"], 1)
        self.assertEqual(report["summary"]["sources"], 0)


if __name__ == "__main__":
    unittest.main()
