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

    def test_short_collection_urls_follow_bilara_layouts(self) -> None:
        self.assertIsNone(verify.source_url("Dhp 21"))
        self.assertTrue(verify.source_url("Ud 8.3").endswith("/kn/ud/vagga8/ud8.3_root-pli-ms.json"))
        self.assertTrue(verify.source_url("Snp 1.1").endswith("/kn/snp/vagga1/snp1.1_root-pli-ms.json"))
        self.assertTrue(verify.source_url("Thag 1.1").endswith("/kn/thag/thag1.1_root-pli-ms.json"))
        self.assertTrue(verify.source_url("Thig 1.1").endswith("/kn/thig/thig1.1_root-pli-ms.json"))
        self.assertTrue(verify.source_url("Iti 44").endswith("/kn/iti/vagga5/iti44_root-pli-ms.json"))
        self.assertTrue(verify.citation_supported("Dhp 21"))

    def test_unparseable_citation_returns_none(self) -> None:
        self.assertIsNone(verify.source_url("somewhere"))


class CheckPhraseTests(unittest.TestCase):
    HAY = verify.normalize(
        "cattārome bhikkhave āhārā bhūtānaṁ vā sattānaṁ ṭhitiyā "
        "kabaḷīkāro āhāro oḷāriko vā sukhumo vā phasso dutiyo"
    )

    def test_present_phrase_is_exact(self) -> None:
        self.assertEqual(verify.check_phrase("phasso dutiyo", self.HAY), "exact")

    def test_a_word_inside_a_longer_word_is_not_verified(self) -> None:
        # Substring containment reported `sati` as found in a text whose only
        # match is `satipaṭṭhānā`, and `paṭṭhāna` as found in
        # `satipaṭṭhānasutta`. Neither is an occurrence of the quoted word, so
        # neither may pass as `exact`; the relationship is real, so it is
        # reported rather than dropped.
        haystack = verify.normalize("Satipaṭṭhānasutta. Cattāro satipaṭṭhānā bhāvetabbā.")
        self.assertEqual(verify.check_phrase("sati", haystack), "compound")
        self.assertEqual(verify.check_phrase("paṭṭhāna", haystack), "compound")
        self.assertEqual(verify.check_phrase("cattāro satipaṭṭhānā", haystack), "exact")

    def test_dhammata_is_matched_as_a_whole_word_only(self) -> None:
        self.assertEqual(
            verify.check_phrase("dhammatā", verify.normalize("ayaṁ dhammatā hoti")), "exact"
        )
        self.assertEqual(
            verify.check_phrase("dhammatā", verify.normalize("dhammataññeva sandhāya")),
            "compound",
        )

    def test_a_sandhi_joined_citation_is_not_a_failure(self) -> None:
        # SN 1.1 has `oghamatarī` where the record quotes `oghaṃ atariṃ`. The
        # words are not there as quoted, but the citation is sound.
        haystack = verify.normalize("“kathaṁ nu tvaṁ, mārisa, oghamatarī”ti?")
        self.assertIn(verify.check_phrase("oghaṃ atariṃ", haystack), {"compound", "inflected"})

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
            verify.check_phrase("cattārome bhikkhave ... phasso dutiyo", self.HAY), "exact"
        )


class WaiverTests(unittest.TestCase):
    def write(self, tmpdir: str, entries: list[dict[str, object]]) -> Path:
        path = Path(tmpdir) / "source-verification-waivers.json"
        path.write_text(json.dumps({"waivers": entries}), encoding="utf-8")
        return path

    def test_missing_file_means_no_waivers(self) -> None:
        self.assertEqual(verify.load_waivers(Path("does-not-exist.json")), {})

    def test_a_waiver_without_a_reason_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self.write(tmpdir, [{"record": "sati", "index": 0}])
            with self.assertRaises(ValueError):
                verify.load_waivers(path)

    def test_duplicate_waivers_for_one_example_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self.write(
                tmpdir,
                [
                    {"record": "sati", "index": 0, "reason": "first"},
                    {"record": "sati", "index": 0, "reason": "second"},
                ],
            )
            with self.assertRaises(ValueError):
                verify.load_waivers(path)

    def test_an_unresolved_example_is_waived_by_record_and_index(self) -> None:
        # An unsupported collection needs no network, so this exercises the
        # whole path: unresolved, then explicitly accepted with a reason.
        with tempfile.TemporaryDirectory() as tmp:
            terms = Path(tmp) / "minor"
            terms.mkdir(parents=True)
            (terms / "x.json").write_text(
                json.dumps({"example_phrases": [{"pali": "phasso", "source": "KN 1.1"}]}),
                encoding="utf-8",
            )
            bare = verify.build_report(terms, cache_dir=Path(tmp) / "cache")
            waived = verify.build_report(
                terms,
                cache_dir=Path(tmp) / "cache",
                waivers={("x", 0): "KN citations name no collection; checked by hand."},
            )

        self.assertEqual(bare["summary"]["unresolved"], 1)
        self.assertEqual(bare["summary"]["unresolved_waived"], 0)
        self.assertEqual(waived["summary"]["unresolved_waived"], 1)
        self.assertIn("by hand", waived["findings"][0]["waiver"])


class PinTests(unittest.TestCase):
    def test_pins_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "source-pins.json"
            verify.write_pins({"MN 1": "a" * 64}, path)
            self.assertEqual(verify.load_pins(path), {"MN 1": "a" * 64})

    def test_missing_pin_file_means_no_pins(self) -> None:
        self.assertEqual(verify.load_pins(Path("does-not-exist.json")), {})

    def test_the_repository_pins_are_well_formed(self) -> None:
        pins = verify.load_pins()
        self.assertTrue(pins)
        for citation, digest in pins.items():
            with self.subTest(citation=citation):
                self.assertTrue(verify.citation_supported(citation), citation)
                self.assertRegex(digest, r"^[0-9a-f]{64}$")


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
                        {"pali": "phasso dutiyo", "source": "KN 1.1"},
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

    def test_render_text_lists_partial_and_absent_findings(self) -> None:
        report = {
            "summary": {
                "examples": 2, "sources": 1, "pinned_sources": 0,
                "verified": 0, "qualified": 0, "failed": 2,
                "unresolved": 0, "unresolved_waived": 0,
                "exact": 0, "compound": 0, "inflected": 0,
                "inconclusive": 0, "partial": 1, "absent": 1,
                "unfetched": 0, "unsupported": 0, "source-changed": 0,
            },
            "findings": [
                {"verdict": "partial", "record": "a", "index": 0,
                 "source": "MN 1", "pali": "some words"},
                {"verdict": "absent", "record": "b", "index": 0,
                 "source": "MN 2", "pali": "missing words"},
            ],
        }

        rendered = verify.render_text(report, top=10)

        self.assertIn("[partial] a", rendered)
        self.assertIn("[absent] b", rendered)
        self.assertNotIn("Every verifiable citation checks out", rendered)


class RangeBundleTests(unittest.TestCase):
    """SuttaCentral bundles peyyala vaggas, so a per-sutta URL can 404.

    Before this fallback existed those citations were recorded as `unfetched`,
    a verdict that neither passes nor fails and so read like a pass.
    """

    LISTING = [
        "sn50.1-12_root-pli-ms.json",
        "sn50.13-22_root-pli-ms.json",
        "sn50.23-34_root-pli-ms.json",
    ]

    def test_first_sutta_of_a_bundle_resolves(self) -> None:
        self.assertEqual(
            verify.find_range_file(self.LISTING, "sn50", 1),
            "sn50.1-12_root-pli-ms.json",
        )

    def test_interior_and_boundary_numbers_resolve(self) -> None:
        self.assertEqual(
            verify.find_range_file(self.LISTING, "sn50", 12),
            "sn50.1-12_root-pli-ms.json",
        )
        self.assertEqual(
            verify.find_range_file(self.LISTING, "sn50", 13),
            "sn50.13-22_root-pli-ms.json",
        )
        self.assertEqual(
            verify.find_range_file(self.LISTING, "sn50", 30),
            "sn50.23-34_root-pli-ms.json",
        )

    def test_number_outside_every_range_returns_none(self) -> None:
        self.assertIsNone(verify.find_range_file(self.LISTING, "sn50", 99))

    def test_dhammapada_verse_bundle_resolves(self) -> None:
        listing = ["dhp1-20_root-pli-ms.json", "dhp21-32_root-pli-ms.json"]
        self.assertEqual(
            verify.find_dhp_range_file(listing, 21),
            "dhp21-32_root-pli-ms.json",
        )

    def test_other_vagga_ranges_are_not_borrowed(self) -> None:
        """A range file for sn49 must never satisfy an sn50 citation."""
        listing = ["sn49.1-12_root-pli-ms.json"]

        self.assertIsNone(verify.find_range_file(listing, "sn50", 1))

    def test_plain_per_sutta_files_are_ignored_as_ranges(self) -> None:
        listing = ["sn50.13_root-pli-ms.json"]

        self.assertIsNone(verify.find_range_file(listing, "sn50", 13))

    def test_range_split_only_applies_to_numbered_sn_and_an(self) -> None:
        self.assertEqual(verify.range_candidates("SN 50.1"), ("sn50", 1))
        self.assertEqual(verify.range_candidates("AN 2.9"), ("an2", 9))
        self.assertIsNone(verify.range_candidates("MN 43"))
        self.assertIsNone(verify.range_candidates("Dhp 21"))
        self.assertIsNone(verify.range_candidates("nonsense"))

    def test_listing_failure_degrades_quietly(self) -> None:
        """A directory listing that cannot be reached must not raise; the
        citation simply stays unresolved as it did before."""
        with tempfile.TemporaryDirectory() as tmp:
            names = verify.list_directory("zz999", Path(tmp), timeout=5)

        self.assertEqual(names, [])


if __name__ == "__main__":
    unittest.main()
