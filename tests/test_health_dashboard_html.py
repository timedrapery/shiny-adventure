from __future__ import annotations

import unittest
from pathlib import Path

from tests.helpers import load_module


health_dashboard = load_module("health_dashboard", "scripts/health_dashboard.py")
health_dashboard_html = load_module("health_dashboard_html", "scripts/health_dashboard_html.py")


def make_record(stem: str, **overrides: object) -> dict[str, object]:
    data: dict[str, object] = {
        "term": stem,
        "normalized_term": stem,
        "entry_type": "major",
        "part_of_speech": "noun",
        "preferred_translation": f"{stem} rendering",
        "definition": f"{stem} definition",
        "tags": ["core-doctrine"],
        "status": "reviewed",
    }
    data.update(overrides)
    return data


def sample_report(**overrides: object) -> dict[str, object]:
    report = health_dashboard.build_report(
        {"citta": make_record("citta"), "alpha": make_record("alpha", status="draft")},
        translations_dir=Path("does-not-exist"),
        history_path=Path("does-not-exist"),
    )
    report["review_queue_aged"] = {
        "as_of": "2026-09-12",
        "buckets": {"8-30 days": 1},
        "items": [{"kind": "draft_entry", "id": "alpha", "waiting_since": "2026-08-24", "waiting_days": 19}],
    }
    report.update(overrides)
    return report


class RenderTests(unittest.TestCase):
    def test_page_is_a_complete_document_with_every_section(self) -> None:
        page = health_dashboard_html.render_html(sample_report(), generated_on="2026-09-12", head_commit="abc1234")
        self.assertTrue(page.startswith("<!doctype html>"))
        for marker in ('id="coverage"', 'id="drift"', 'id="queue"', 'id="failures"', "<title>Editorial Health</title>"):
            self.assertIn(marker, page)
        self.assertIn("abc1234", page)

    def test_fragment_omits_the_document_shell(self) -> None:
        page = health_dashboard_html.render_html(
            sample_report(), generated_on="2026-09-12", head_commit=None, fragment=True
        )
        self.assertTrue(page.startswith("<title>"))
        self.assertNotIn("<html", page)
        self.assertNotIn("<body", page)

    def test_live_ages_appear_in_the_html(self) -> None:
        # The committed Markdown withholds day counts to stay byte-stable.
        # This page is never freshness-checked, so it may show them.
        page = health_dashboard_html.render_html(sample_report(), generated_on="2026-09-12", head_commit=None)
        self.assertIn("oldest 19 days", page)
        self.assertIn("<td>19</td>", page)

    def test_report_strings_are_escaped(self) -> None:
        report = sample_report()
        report["coverage"]["top_ungoverned"] = [
            {"surface": "<script>alert(1)</script>", "occurrences": 1, "documents": ["a&b.md"]}
        ]
        report["coverage"]["ungoverned_total"] = 1
        page = health_dashboard_html.render_html(report, generated_on="2026-09-12", head_commit=None)
        self.assertNotIn("<script>alert(1)</script>", page)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", page)
        self.assertIn("a&amp;b.md", page)

    def test_every_chart_has_a_table_twin(self) -> None:
        page = health_dashboard_html.render_html(sample_report(), generated_on="2026-09-12", head_commit=None)
        # Four sections, each with a chart card and a table (or its empty-state
        # sentence) beside it.
        self.assertEqual(page.count('<svg class="chart"'), 3)  # failures chart absent without history
        self.assertIn("No history recorded", page)
        self.assertGreaterEqual(page.count("<table>") + page.count('class="empty"'), 4)

    def test_status_chips_carry_a_glyph_and_a_label(self) -> None:
        chip = health_dashboard_html.status_chip("critical", "needs a look")
        self.assertIn('class="chip chip-critical"', chip)
        self.assertIn('aria-hidden="true"', chip)
        self.assertIn("needs a look", chip)

    def test_every_theme_token_is_declared_on_bare_root(self) -> None:
        # A colour whose only definition sits behind a media query or a
        # data-theme stamp never applies in the un-stamped state.
        page = health_dashboard_html.render_html(sample_report(), generated_on="2026-09-12", head_commit=None)
        root_block = page.split(":root {", 1)[1].split("}", 1)[0]
        for token in ("--ground", "--surface", "--ink", "--s1", "--s2", "--s3", "--o1", "--o4", "--good", "--critical"):
            self.assertIn(token + ":", root_block, token)


class ChartTests(unittest.TestCase):
    def test_stacked_bar_labels_only_segments_that_fit(self) -> None:
        svg = health_dashboard_html.svg_stacked_bar(
            [("Exact", 900, "s1"), ("Tiny", 1, "s2")], width=640
        )
        self.assertIn("Exact 900", svg)
        self.assertNotIn(">Tiny 1<", svg)
        # The value is still reachable through the hover/focus tooltip.
        self.assertIn("Tiny: 1 surfaces", svg)

    def test_columns_grow_from_one_baseline_with_clean_ticks(self) -> None:
        svg = health_dashboard_html.svg_columns(
            [("W01", [("schema", 3, "s1"), ("lint", 0, "s2")]), ("W02", [("schema", 0, "s1"), ("lint", 7, "s2")])],
            aria="test",
        )
        self.assertIn('aria-label="test"', svg)
        self.assertEqual(svg.count('class="col s'), 2)  # two non-zero columns
        self.assertEqual(svg.count("col-zero"), 2)  # two zero hit targets
        for tick in (">0<", ">5<", ">10<"):
            self.assertIn(tick, svg)

    def test_zero_only_series_still_renders_a_scale(self) -> None:
        svg = health_dashboard_html.svg_columns([("W01", [("schema", 0, "s1")])], aria="flat")
        self.assertIn(">0<", svg)
        self.assertIn(">1<", svg)


if __name__ == "__main__":
    unittest.main()
