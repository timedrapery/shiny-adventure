"""Regression coverage for the next-sutta priority table generator."""

from __future__ import annotations

import unittest
from pathlib import Path

from scripts import next_sutta_priority_report as report
from scripts.audit_surface_leverage import load_entries, translated_suttas


REPO_ROOT = Path(__file__).resolve().parent.parent


class PriorityReportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.terms = report.load_terms()

    def test_counts_match_the_leverage_audit(self) -> None:
        """The table's numbers are the audit's numbers, not a separate tally."""
        summary = report.build_report(self.terms)
        entries = load_entries(REPO_ROOT / "terms")
        translated = translated_suttas()
        cited = [entry for entry in entries if entry["refs"]]
        orphans = [e for e in cited if not (set(e["refs"]) & translated)]
        self.assertEqual(summary["surfaces"], len(translated))
        self.assertEqual(summary["records"], len(entries))
        self.assertEqual(summary["cited"], len(cited))
        self.assertEqual(summary["orphans"], len(orphans))
        self.assertEqual(summary["anchored"], len(cited) - len(orphans))

    def test_every_complete_queue_item_is_a_registered_surface(self) -> None:
        """A row cannot claim `complete` unless the corpus actually has it."""
        translated = translated_suttas()
        for item in report.QUEUE:
            if item.position == "complete":
                self.assertIn(item.sutta, translated, item.sutta)

    def test_at_most_one_next_item_and_it_is_untranslated(self) -> None:
        """A handoff is unambiguous: one next translation, or none at all."""
        nexts = [item for item in report.QUEUE if item.position == "next"]
        self.assertLessEqual(len(nexts), 1)
        for item in nexts:
            self.assertNotIn(item.sutta, translated_suttas())

    def test_a_finished_queue_asks_for_a_fresh_audit(self) -> None:
        """With nothing left to translate, the table must not read as a plan."""
        if any(item.position == "next" for item in report.QUEUE):
            self.skipTest("the queue still has an unfinished item")
        rendered = report.render_table(report.build_report(self.terms))
        self.assertIn("there is no next item", rendered)
        self.assertIn("run a fresh audit", rendered)

    def test_render_is_deterministic(self) -> None:
        summary = report.build_report(self.terms)
        self.assertEqual(report.render_table(summary), report.render_table(summary))


if __name__ == "__main__":
    unittest.main()
