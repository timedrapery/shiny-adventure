"""Tests for the citation stem triage.

These exercise the screen itself rather than the network path: `triage` is
given a fake findings list and a cache directory it never needs to read,
because the sources are stubbed.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import triage_citation_stems as triage_mod  # noqa: E402


class BandTests(unittest.TestCase):
    def test_bands_sort_least_explained_first(self):
        self.assertEqual(triage_mod.band_for(0.0), "A")
        self.assertEqual(triage_mod.band_for(0.40), "A")
        self.assertEqual(triage_mod.band_for(0.41), "B")
        self.assertEqual(triage_mod.band_for(0.60), "B")
        self.assertEqual(triage_mod.band_for(0.61), "C")


class LongestSharedRunTests(unittest.TestCase):
    def test_absent_word_explains_nothing(self):
        self.assertEqual(triage_mod.longest_shared_run("cagena", "saccam saccavadi"), 0)

    def test_word_inside_a_compound_is_mostly_explained(self):
        # The screen must not treat a word the sutta carries inside a longer
        # form as missing evidence; that is the main false-positive mode.
        run = triage_mod.longest_shared_run("punnakkhetta", "anuttaram punnakkhettam lokassa")
        self.assertEqual(run, len("punnakkhetta"))


class TriageTests(unittest.TestCase):
    def setUp(self):
        self._resolve = triage_mod.ves.resolve_source
        triage_mod.ves.resolve_source = lambda src, cache: self.sources.get(src)

    def tearDown(self):
        triage_mod.ves.resolve_source = self._resolve

    def test_only_the_two_soft_verdicts_are_triaged(self):
        self.sources = {"MN 1": "ekam samayam bhagava ukkatthayam viharati"}
        findings = [
            {"record": "r1", "source": "MN 1", "verdict": "ok", "pali": "savatthiyam"},
            {"record": "r2", "source": "MN 1", "verdict": "absent", "pali": "savatthiyam"},
            {"record": "r3", "source": "MN 1", "verdict": "partial", "pali": "savatthiyam"},
        ]
        self.assertEqual(triage_mod.triage(findings, Path(".")), [])

    def test_missing_word_is_flagged_and_present_word_is_not(self):
        self.sources = {"MN 1": "ekam samayam bhagava ukkatthayam viharati subhagavane"}
        findings = [
            # `savatthiyam` is not in MN 1 -- this is the real 2026-08-21 finding.
            {"record": "bhagava", "source": "MN 1", "verdict": "inconclusive",
             "pali": "ekam samayam bhagava savatthiyam viharati"},
            # every word present, so not a suspect at all
            {"record": "other", "source": "MN 1", "verdict": "inflected",
             "pali": "ekam samayam bhagava viharati"},
        ]
        rows = triage_mod.triage(findings, Path("."))
        self.assertEqual([r["record"] for r in rows], ["bhagava"])
        self.assertEqual([d["word"] for d in rows[0]["missing"]], ["savatthiyam"])
        self.assertEqual(rows[0]["band"], "A")

    def test_unresolvable_source_is_skipped_rather_than_reported(self):
        # An unfetchable sutta proves nothing either way, so it must not appear
        # as a suspect.
        self.sources = {}
        findings = [{"record": "r", "source": "Iti 44", "verdict": "inconclusive",
                     "pali": "anupadisesa nibbanadhatu"}]
        self.assertEqual(triage_mod.triage(findings, Path(".")), [])


if __name__ == "__main__":
    unittest.main()
