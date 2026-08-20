from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts import audit_surface_leverage as audit  # noqa: E402


class OrphanClassificationTests(unittest.TestCase):
    def test_entry_is_orphan_only_when_every_anchor_is_untranslated(self) -> None:
        entries = [
            {"name": "half-anchored", "kind": "major", "refs": ["MN 9", "MN 43"]},
            {"name": "fully-orphan", "kind": "major", "refs": ["MN 43"]},
            {"name": "uncited", "kind": "minor", "refs": []},
        ]
        summary = audit.summarize(entries, {"MN 9"})

        self.assertEqual(summary["cited"], 2)
        self.assertEqual(summary["anchored"], 1)
        self.assertEqual(summary["orphans"], 1)
        self.assertEqual(summary["uncited"], 1)

    def test_translated_anchors_are_not_offered_as_candidates(self) -> None:
        entries = [{"name": "anchored", "kind": "major", "refs": ["MN 9"]}]

        leverage = audit.build_leverage(entries, {"MN 9"})

        self.assertNotIn("MN 9", leverage)

    def test_orphan_majors_and_minors_are_tracked_separately(self) -> None:
        entries = [
            {"name": "big", "kind": "major", "refs": ["MN 43"]},
            {"name": "small", "kind": "minor", "refs": ["MN 43"]},
        ]

        row = audit.build_leverage(entries, set())["MN 43"]

        self.assertEqual(row.orphan_majors, ["big"])
        self.assertEqual(row.orphan_minors, ["small"])
        self.assertEqual(row.orphan_total, 2)

    def test_anchored_entry_still_counts_toward_citing_but_not_orphans(self) -> None:
        """An entry anchored elsewhere puts no orphan pressure on this sutta."""
        entries = [{"name": "anchored", "kind": "major", "refs": ["MN 9", "MN 43"]}]

        row = audit.build_leverage(entries, {"MN 9"})["MN 43"]

        self.assertEqual(row.citing_entries, 1)
        self.assertEqual(row.orphan_total, 0)


class EnumerationStubTests(unittest.TestCase):
    def test_short_text_is_flagged_as_an_enumeration_stub(self) -> None:
        row = audit.SuttaLeverage(sutta="AN 7.11", pali_words=18)

        self.assertTrue(row.is_enumeration_stub)

    def test_full_discourse_is_not_a_stub(self) -> None:
        row = audit.SuttaLeverage(sutta="MN 43", pali_words=1481)

        self.assertFalse(row.is_enumeration_stub)

    def test_uncached_text_is_never_assumed_to_be_a_stub(self) -> None:
        row = audit.SuttaLeverage(sutta="MN 77", pali_words=None)

        self.assertFalse(row.is_enumeration_stub)
        self.assertIn("unverified", row.length_note)

    def test_stubs_rank_by_total_coverage_not_by_major_split(self) -> None:
        many_minors = audit.SuttaLeverage(
            sutta="SN 45.174", orphan_minors=["a", "b", "c"], pali_words=34
        )
        few_majors = audit.SuttaLeverage(
            sutta="SN 43.1", orphan_majors=["x", "y"], pali_words=70
        )

        ordered = audit.rank_stubs([few_majors, many_minors])

        self.assertEqual([r.sutta for r in ordered], ["SN 45.174", "SN 43.1"])

    def test_substantive_candidates_rank_by_major_pressure(self) -> None:
        many_minors = audit.SuttaLeverage(
            sutta="MN 77", orphan_minors=["a", "b", "c"], pali_words=2000
        )
        few_majors = audit.SuttaLeverage(
            sutta="SN 51.13", orphan_majors=["x", "y"], pali_words=242
        )

        ordered = audit.rank([many_minors, few_majors])

        self.assertEqual([r.sutta for r in ordered], ["SN 51.13", "MN 77"])


class PaliWordCountTests(unittest.TestCase):
    def test_front_matter_segments_are_excluded(self) -> None:
        """Titles and vagga names must not inflate a short text's word count."""
        cached = audit.pali_word_count("AN 7.11")

        if cached is None:
            self.skipTest("AN 7.11 root text is not cached")
        # The body is a count, a list of seven, and a restatement. The front
        # matter ("Anguttara Nikaya 7.11", "2. Anusayavagga", the title) would
        # add roughly half again as much if it were counted.
        self.assertLess(cached, audit.ENUMERATION_STUB_MAX_WORDS)

    def test_missing_cache_entry_returns_none_rather_than_guessing(self) -> None:
        self.assertIsNone(audit.pali_word_count("MN 99999"))


class LiveDataTests(unittest.TestCase):
    """Guards against the audit silently degrading as the corpus grows."""

    def test_audit_runs_against_the_real_corpus(self) -> None:
        entries = audit.load_entries()
        translated = audit.translated_suttas()

        self.assertGreater(len(entries), 1000)
        self.assertGreater(len(translated), 40)

        summary = audit.summarize(entries, translated)
        self.assertEqual(
            summary["cited"] + summary["uncited"], summary["terms"]
        )
        self.assertEqual(
            summary["anchored"] + summary["orphans"], summary["cited"]
        )

    def test_surface_labels_use_the_sutta_reference_id_format(self) -> None:
        """Labels are matched against sutta_references by exact string, so a
        label like "MN 10: Satipatthana Sutta" would silently make the audit
        report an already-translated text as a candidate."""
        pattern = re.compile(r"^(?:[A-Z][A-Za-z]{1,5}) \d+(?:\.\d+)?$")

        malformed = sorted(
            label for label in audit.translated_suttas() if not pattern.match(label)
        )

        self.assertEqual(
            malformed, [], f"surface labels not in reference-id format: {malformed}"
        )

    def test_surfaces_that_anchor_no_governed_vocabulary_are_known(self) -> None:
        """A surface no term record cites shows no policy in running text.

        MN 61 is the only one: it was translated by direct request rather than
        drawn from a wave audit, so nothing was written to cite it. If this
        list grows, surfaces are being added without lexicon follow-through;
        if MN 61 leaves it, the citation pass has happened and this test
        should be updated.
        """
        entries = audit.load_entries()
        all_refs = {ref for entry in entries for ref in entry["refs"]}

        uncited_surfaces = sorted(
            label for label in audit.translated_suttas() if label not in all_refs
        )

        self.assertEqual(uncited_surfaces, ["MN 61"])


class ClusterCoverageTests(unittest.TestCase):
    def test_dark_counts_uncited_terms_not_only_orphans(self) -> None:
        """A term with no citations is as invisible as an orphan."""
        row = audit.ClusterCoverage(label="x", shown=0, orphan=3, uncited=10)

        self.assertEqual(row.total, 13)
        self.assertEqual(row.dark, 13)
        self.assertEqual(row.dark_pct, 100.0)

    def test_cluster_members_resolve_regardless_of_import_path(self) -> None:
        """Regression: the report resolved cluster modules only when the
        `scripts.` package prefix was importable, so running the audit as a
        plain script reported every cluster as empty."""
        try:
            from scripts.cluster_registry import CLUSTER_SURFACES
        except ModuleNotFoundError:  # pragma: no cover
            from cluster_registry import CLUSTER_SURFACES

        resolved = [c for c in CLUSTER_SURFACES if audit.cluster_members(c)]

        self.assertGreater(len(resolved), 15)

    def test_live_clusters_report_real_coverage(self) -> None:
        entries = audit.load_entries()
        rows = audit.build_cluster_coverage(entries, audit.translated_suttas())

        self.assertGreater(len(rows), 15)
        for row in rows:
            self.assertEqual(row.total, row.shown + row.orphan + row.uncited)
            self.assertEqual(row.dark, row.orphan + row.uncited)


if __name__ == "__main__":
    unittest.main()
