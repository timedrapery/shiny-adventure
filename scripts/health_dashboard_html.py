#!/usr/bin/env python3
"""Render the health dashboard report as a self-contained HTML page.

This is a renderer over the dict `health_dashboard.build_report` produces —
the same data the Markdown and JSON views read. It knows nothing about term
files or git; everything it shows arrives in the report.

The page is meant to be looked at, not committed: `health_dashboard.py
--format html` writes it on demand and CI uploads it as an artifact. Because it
is never freshness-checked, it can carry what the committed Markdown cannot —
live day counts and the date it was generated.

Charts are inline SVG built here, with no library. Every chart sits beside its
table twin, so no value is reachable only through colour or hover.
"""

from __future__ import annotations

from html import escape
from typing import Sequence

# Chart and status colours follow the validated reference palette in the
# data-viz method: categorical slots in fixed order, status colours reserved
# for state and never reused as a series. Light and dark are separate selected
# steps, not an automatic flip.
SERIES_LIGHT = ("#2a78d6", "#eb6834", "#1baf7a")
SERIES_DARK = ("#3987e5", "#d95926", "#199e70")
ORDINAL_LIGHT = ("#86b6ef", "#5598e7", "#2a78d6", "#1c5cab")
ORDINAL_DARK = ("#9ec5f4", "#6da7ec", "#3987e5", "#256abf")

BAR_THICKNESS = 22
SURFACE_GAP = 2
# The chart cards sit at roughly this width on a desktop page. Drawing on a
# viewBox the same width keeps SVG text near its nominal size instead of
# shrinking with the scale.
CHART_WIDTH = 440


def fmt_int(value: object) -> str:
    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return escape(str(value))


def fmt_pct(value: object) -> str:
    try:
        return f"{float(value):.1f}%"
    except (TypeError, ValueError):
        return escape(str(value))


def status_chip(level: str, text: str) -> str:
    """A state marker that never relies on colour alone: glyph + label."""
    glyph = {"good": "●", "warning": "▲", "critical": "■", "neutral": "○"}[level]
    return (
        f'<span class="chip chip-{level}"><span class="chip-glyph" aria-hidden="true">{glyph}</span>'
        f"{escape(text)}</span>"
    )


def stat_tile(label: str, value: str, note: str, chip: str) -> str:
    return (
        '<div class="tile">'
        f'<div class="tile-label">{escape(label)}</div>'
        f'<div class="tile-value">{value}</div>'
        f'<div class="tile-foot">{chip}<span class="tile-note">{escape(note)}</span></div>'
        "</div>"
    )


def svg_stacked_bar(
    segments: Sequence[tuple[str, int, str]],
    *,
    width: int = CHART_WIDTH,
) -> str:
    """One horizontal part-to-whole bar.

    `segments` are (label, count, css_class). Segments touch across a
    surface-coloured gap rather than a stroke, and a segment is labelled
    inside only when the text plainly fits; the legend and tooltip carry the
    rest.
    """
    total = sum(count for _label, count, _cls in segments) or 1
    height = BAR_THICKNESS + 8
    parts = [
        f'<svg class="chart" viewBox="0 0 {width} {height}" role="img" '
        f'aria-label="Surfaces by match route">'
    ]
    x = 0.0
    for label, count, cls in segments:
        if count <= 0:
            continue
        w = width * count / total
        inner = max(w - SURFACE_GAP, 0)
        tip = f"{label}: {count:,} surfaces ({100 * count / total:.1f}%)"
        parts.append(
            f'<rect class="seg {cls}" x="{x:.1f}" y="4" width="{inner:.1f}" height="{BAR_THICKNESS}" '
            f'rx="0" tabindex="0" data-tip="{escape(tip)}"><title>{escape(tip)}</title></rect>'
        )
        # Roughly 7px per character at this size; label only when it fits
        # with padding on both sides.
        text = f"{label} {count:,}"
        if inner >= len(text) * 7 + 16:
            parts.append(
                f'<text class="seg-label" x="{x + 8:.1f}" y="{4 + BAR_THICKNESS / 2 + 4:.1f}">'
                f"{escape(text)}</text>"
            )
        x += w
    parts.append("</svg>")
    return "".join(parts)


def svg_columns(
    groups: Sequence[tuple[str, Sequence[tuple[str, int, str]]]],
    *,
    aria: str,
    width: int = CHART_WIDTH,
    label_caps: bool = True,
) -> str:
    """Grouped columns from a single baseline.

    `groups` are (x_label, [(series_label, value, css_class), ...]). One
    scale places every mark and tick. Caps are labelled directly only when
    asked; the y ticks carry the values otherwise.
    """
    n_groups = max(len(groups), 1)
    n_series = max((len(series) for _x, series in groups), default=1) or 1
    values = [value for _x, series in groups for _label, value, _cls in series]
    top = max(values + [1])
    # Clean tick ceiling: 1, 2, 5, 10, 20, 50 ...
    magnitude = 1
    while magnitude * 5 < top:
        magnitude *= 10
    ceiling = next(step for step in (magnitude, magnitude * 2, magnitude * 5, magnitude * 10) if step >= top)
    ticks = [0, ceiling // 2, ceiling] if ceiling >= 2 else [0, 1]

    pad_left, pad_right, pad_top, pad_bottom = 36, 12, 18, 30
    plot_w = width - pad_left - pad_right
    plot_h = 140
    height = plot_h + pad_top + pad_bottom
    baseline_y = pad_top + plot_h
    band = plot_w / n_groups
    col_w = min(BAR_THICKNESS, (band - 12) / n_series - SURFACE_GAP)
    group_w = n_series * (col_w + SURFACE_GAP) - SURFACE_GAP

    parts = [f'<svg class="chart" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(aria)}">']
    for tick in ticks:
        y = baseline_y - plot_h * tick / ceiling
        parts.append(f'<line class="grid" x1="{pad_left}" x2="{width - pad_right}" y1="{y:.1f}" y2="{y:.1f}"/>')
        parts.append(f'<text class="tick" x="{pad_left - 8}" y="{y + 4:.1f}" text-anchor="end">{tick}</text>')
    parts.append(
        f'<line class="axis" x1="{pad_left}" x2="{width - pad_right}" y1="{baseline_y}" y2="{baseline_y}"/>'
    )
    for index, (x_label, series) in enumerate(groups):
        group_x = pad_left + band * index + (band - group_w) / 2
        for s_index, (s_label, value, cls) in enumerate(series):
            x = group_x + s_index * (col_w + SURFACE_GAP)
            h = plot_h * value / ceiling
            y = baseline_y - h
            tip = f"{x_label} · {s_label}: {value:,}"
            if value > 0:
                # Rounded data-end, square at the baseline: a path, not a rx
                # rect, so the baseline corners stay sharp.
                r = min(4, col_w / 2, h)
                d = (
                    f"M{x:.1f},{baseline_y} V{y + r:.1f} Q{x:.1f},{y:.1f} {x + r:.1f},{y:.1f} "
                    f"H{x + col_w - r:.1f} Q{x + col_w:.1f},{y:.1f} {x + col_w:.1f},{y + r:.1f} "
                    f"V{baseline_y} Z"
                )
                parts.append(
                    f'<path class="col {cls}" d="{d}" tabindex="0" data-tip="{escape(tip)}">'
                    f"<title>{escape(tip)}</title></path>"
                )
            else:
                # A zero still gets a hit target so the tooltip can say so.
                parts.append(
                    f'<rect class="col col-zero" x="{x:.1f}" y="{baseline_y - 2}" width="{col_w:.1f}" height="2" '
                    f'tabindex="0" data-tip="{escape(tip)}"><title>{escape(tip)}</title></rect>'
                )
            # A zero column has nothing to cap; its value is in the tooltip
            # and the table, and a row of "0"s only adds noise.
            if label_caps and value > 0:
                parts.append(
                    f'<text class="cap" x="{x + col_w / 2:.1f}" y="{y - 6:.1f}" text-anchor="middle">{value:,}</text>'
                )
        parts.append(
            f'<text class="tick" x="{pad_left + band * index + band / 2:.1f}" y="{baseline_y + 18}" '
            f'text-anchor="middle">{escape(x_label)}</text>'
        )
    parts.append("</svg>")
    return "".join(parts)


def legend(items: Sequence[tuple[str, str]]) -> str:
    return (
        '<ul class="legend">'
        + "".join(
            f'<li><span class="swatch {cls}" aria-hidden="true"></span>{escape(label)}</li>' for label, cls in items
        )
        + "</ul>"
    )


def table(headers: Sequence[str], rows: Sequence[Sequence[str]], *, empty: str) -> str:
    if not rows:
        return f'<p class="empty">{escape(empty)}</p>'
    head = "".join(f"<th>{escape(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows)
    return f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def mono(value: object) -> str:
    return f'<code>{escape(str(value))}</code>'


def render_html(
    report: dict[str, object],
    *,
    generated_on: str,
    head_commit: str | None,
    top: int = 15,
    fragment: bool = False,
) -> str:
    coverage = report["coverage"]
    drift = report["drift"]
    queue = report["review_queue"]
    aged = report.get("review_queue_aged") or {"as_of": generated_on, "buckets": {}, "items": []}
    failures = report["check_failures"]

    # --- Summary tiles ---------------------------------------------------
    surface_pct = float(coverage["surface_coverage_pct"])
    cov_chip = status_chip("good" if surface_pct >= 60 else "warning" if surface_pct >= 30 else "critical",
                           "governed by surface")
    drift_total = int(drift["findings_total"])
    drift_chip = status_chip("good" if drift_total == 0 else "warning" if drift_total <= 5 else "critical",
                             "no conflicts" if drift_total == 0 else "needs a look")
    items_aged = aged.get("items", [])
    oldest_days = max((row.get("waiting_days") or 0 for row in items_aged), default=0)
    queue_chip = status_chip(
        "good" if oldest_days <= 30 else "warning" if oldest_days <= 90 else "critical",
        "oldest " + (f"{oldest_days} days" if items_aged else "—"),
    )
    failing_weeks = int(failures["failing_weeks"])
    weeks_recorded = int(failures["weeks_recorded"])
    fail_chip = status_chip(
        "neutral" if not weeks_recorded else "good" if failing_weeks == 0 else "critical",
        "no history" if not weeks_recorded else f"{weeks_recorded} weeks recorded",
    )

    formulas = report.get("formula_agreement") or {"unexplained": 0, "waived": 0, "regressions": 0, "stale_baseline": 0, "groups": []}
    evidence = report.get("human_evidence") or {
        "surfaces": 0, "source_fidelity_complete": 0, "read_aloud_complete": 0,
        "newcomer_reviews_recorded": 0, "newcomer_reviews_counting": 0, "surfaces_validated": 0,
    }
    formula_chip = status_chip(
        "critical" if formulas["regressions"] or formulas["stale_baseline"]
        else "warning" if formulas["unexplained"] else "good",
        "outside baseline" if formulas["regressions"] else "acknowledged backlog" if formulas["unexplained"] else "all agree",
    )
    reviews_done = int(evidence["newcomer_reviews_recorded"])
    evidence_chip = status_chip(
        "good" if evidence["surfaces_validated"] else "warning" if reviews_done else "critical",
        f"{evidence['surfaces_validated']} validated" if evidence["surfaces_validated"] else "no human evidence yet" if not reviews_done else "in progress",
    )

    tiles = "".join(
        [
            stat_tile("Coverage by occurrence", fmt_pct(coverage["occurrence_coverage_pct"]),
                      f"{fmt_pct(surface_pct)} of {fmt_int(coverage['distinct_surfaces'])} distinct surfaces", cov_chip),
            stat_tile("Declared-rendering conflicts", fmt_int(drift_total),
                      f"across {fmt_int(drift['declared_renderings'])} declared renderings", drift_chip),
            stat_tile("Formula disagreements", fmt_int(formulas["unexplained"]),
                      f"{fmt_int(formulas['waived'])} waived by exception", formula_chip),
            stat_tile("Newcomer reviews recorded", fmt_int(reviews_done),
                      f"{fmt_int(evidence['read_aloud_complete'])} read-alouds of {fmt_int(evidence['surfaces'])} surfaces", evidence_chip),
            stat_tile("Waiting for review", fmt_int(queue["total"]),
                      "candidates, drafts, and unfinished newcomer reviews", queue_chip),
            stat_tile("Weeks with a failure", fmt_int(failing_weeks) if weeks_recorded else "—",
                      "schema or lint, replayed from git", fail_chip),
        ]
    )

    # --- Coverage --------------------------------------------------------
    routes = coverage["match_routes"]
    route_segments = [
        ("Exact", int(routes.get("exact", 0)), "s1"),
        ("Inflected", int(routes.get("inflected", 0)), "s2"),
        ("Compound", int(routes.get("compound", 0)), "s3"),
        ("Ungoverned", int(routes.get("none", 0)), "s-none"),
    ]
    coverage_chart = svg_stacked_bar(route_segments)
    coverage_legend = legend([(label, cls) for label, _count, cls in route_segments])
    ungoverned_rows = [
        [mono(row["surface"]), fmt_int(row["occurrences"]),
         escape(", ".join(str(d) for d in row["documents"]))]
        for row in coverage["top_ungoverned"][:top]
    ]
    coverage_table = table(["Surface", "Occurrences", "Documents"], ungoverned_rows,
                           empty="Every quoted surface is governed.")

    # --- Drift -----------------------------------------------------------
    kinds = drift["by_kind"]
    kind_order = ("self_contradiction", "discouraged", "unlisted")
    drift_groups = [(kind.replace("_", " "), [("findings", int(kinds.get(kind, 0)), "s1")]) for kind in kind_order]
    drift_chart = svg_columns(drift_groups, aria="Drift findings by kind")
    drift_rows = [
        [escape(str(f["document"])), mono(f["headword"]), escape(str(f["kind"]).replace("_", " ")),
         escape(", ".join(str(d) for d in f["declared"])), escape(str(f["preferred"]) or "—")]
        for f in drift["findings"][:top]
    ]
    drift_table = table(["Document", "Headword", "Kind", "Declared", "Preferred"], drift_rows,
                        empty="No declared rendering fights its record.")

    # --- Review queue ----------------------------------------------------
    bucket_order = ("0-7 days", "8-30 days", "31-90 days", "over 90 days", "unknown")
    buckets = aged.get("buckets", {})
    queue_groups = [
        (name, [("items", int(buckets.get(name, 0)), f"o{index + 1}" if index < 4 else "s-none")])
        for index, name in enumerate(bucket_order)
        if name != "unknown" or buckets.get("unknown")
    ]
    queue_chart = svg_columns(queue_groups, aria="Review queue by waiting time")
    queue_rows = [
        [escape(str(row["kind"]).replace("_", " ")), mono(row["id"]), mono(row.get("waiting_since") or "unknown"),
         fmt_int(row["waiting_days"]) if row.get("waiting_days") is not None else "—"]
        for row in items_aged[:top]
    ]
    queue_table = table(["Kind", "Item", "Waiting since", "Days"], queue_rows, empty="Nothing is waiting for review.")

    # --- Failures per week ----------------------------------------------
    series_rows = failures["series"]
    fail_groups = [
        (str(row.get("week", "")).replace("2026-", ""),
         [("schema", int(row.get("schema_failures", 0) or 0), "s1"),
          ("lint", int(row.get("lint_failures", 0) or 0), "s2")])
        for row in series_rows
    ]
    fail_chart = svg_columns(fail_groups, aria="Schema and lint findings per week", label_caps=False) if fail_groups else ""
    fail_legend = legend([("Schema findings", "s1"), ("Lint findings", "s2")])
    fail_rows = [
        [mono(row.get("week", "")), mono(row.get("commit", "")), fmt_int(row.get("commits_checked", 0)),
         fmt_int(row.get("commits_failing", 0)), fmt_int(row.get("schema_failures", 0)), fmt_int(row.get("lint_failures", 0))]
        for row in series_rows
    ]
    fail_table = table(["Week", "Last commit", "Commits", "Failing", "Schema", "Lint"], fail_rows,
                       empty="No history recorded. Run scripts/backfill_check_history.py.")
    fail_note = (
        "Every recorded commit passes both checks. Until one fails, read this panel as a tripwire, not a trend."
        if weeks_recorded and failing_weeks == 0 else ""
    )

    provenance = f"Generated {escape(generated_on)}"
    if head_commit:
        provenance += f" from {mono(head_commit)}"

    head_inner = f"""<title>Editorial Health</title>
<meta name="description" content="Coverage, drift, review latency, and check failures for the Pali term lexicon.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap">
<style>
:root {{
  color-scheme: light;
  --ground: #f5f6f9; --surface: #ffffff; --ink: #1b1f2e; --ink-2: #545b73; --muted: #8a90a6;
  --line: #dfe2eb; --accent: #3d4ea6; --accent-ink: #ffffff;
  --good: #0ca30c; --good-ink: #006300; --warning: #fab219; --warning-ink: #6b4a00;
  --critical: #d03b3b; --critical-ink: #8f1f1f;
  --s1: {SERIES_LIGHT[0]}; --s2: {SERIES_LIGHT[1]}; --s3: {SERIES_LIGHT[2]}; --s-none: #c9cdd9;
  --o1: {ORDINAL_LIGHT[0]}; --o2: {ORDINAL_LIGHT[1]}; --o3: {ORDINAL_LIGHT[2]}; --o4: {ORDINAL_LIGHT[3]};
  --grid: #e9ebf1; --axis: #cfd3de;
  --sans: "Instrument Sans", system-ui, -apple-system, "Segoe UI", sans-serif;
  --mono: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    color-scheme: dark;
    --ground: #14171f; --surface: #1c2029; --ink: #e8eaf2; --ink-2: #aab0c4; --muted: #7c8299;
    --line: #2c3140; --accent: #93a3f2; --accent-ink: #0f1220;
    --good-ink: #5ed35e; --warning-ink: #fac54a; --critical-ink: #f07878;
    --s1: {SERIES_DARK[0]}; --s2: {SERIES_DARK[1]}; --s3: {SERIES_DARK[2]}; --s-none: #3a4052;
    --o1: {ORDINAL_DARK[0]}; --o2: {ORDINAL_DARK[1]}; --o3: {ORDINAL_DARK[2]}; --o4: {ORDINAL_DARK[3]};
    --grid: #262b38; --axis: #3a4052;
  }}
}}
:root[data-theme="dark"] {{
  color-scheme: dark;
  --ground: #14171f; --surface: #1c2029; --ink: #e8eaf2; --ink-2: #aab0c4; --muted: #7c8299;
  --line: #2c3140; --accent: #93a3f2; --accent-ink: #0f1220;
  --good-ink: #5ed35e; --warning-ink: #fac54a; --critical-ink: #f07878;
  --s1: {SERIES_DARK[0]}; --s2: {SERIES_DARK[1]}; --s3: {SERIES_DARK[2]}; --s-none: #3a4052;
  --o1: {ORDINAL_DARK[0]}; --o2: {ORDINAL_DARK[1]}; --o3: {ORDINAL_DARK[2]}; --o4: {ORDINAL_DARK[3]};
  --grid: #262b38; --axis: #3a4052;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0; background: var(--ground); color: var(--ink); font-family: var(--sans);
  font-size: 15px; line-height: 1.5; padding-block: 32px 64px; padding-inline: 20px;
}}
.page {{ max-width: 1120px; margin-inline: auto; display: grid; gap: 40px; }}
header {{ display: flex; flex-wrap: wrap; align-items: baseline; justify-content: space-between; gap: 8px 24px; }}
h1 {{ font-size: 26px; font-weight: 700; letter-spacing: -0.01em; margin: 0; text-wrap: balance; }}
.provenance {{ color: var(--ink-2); font-size: 14px; }}
code {{ font-family: var(--mono); font-size: 0.92em; }}
.tiles {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; }}
.tile {{ background: var(--surface); border: 1px solid var(--line); border-radius: 6px; padding: 18px 20px 16px; display: grid; gap: 6px; }}
.tile-label {{ font-size: 12px; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; color: var(--ink-2); }}
.tile-value {{ font-size: 40px; font-weight: 600; line-height: 1.05; letter-spacing: -0.02em; }}
.tile-foot {{ display: flex; flex-wrap: wrap; align-items: center; gap: 8px; margin-top: 4px; }}
.tile-note {{ color: var(--muted); font-size: 13px; }}
.chip {{ display: inline-flex; align-items: center; gap: 6px; font-size: 12px; font-weight: 600; padding: 3px 9px; border-radius: 999px; border: 1px solid var(--line); background: var(--ground); white-space: nowrap; }}
.chip-glyph {{ font-size: 9px; }}
.chip-good {{ color: var(--good-ink); }} .chip-good .chip-glyph {{ color: var(--good); }}
.chip-warning {{ color: var(--warning-ink); }} .chip-warning .chip-glyph {{ color: var(--warning); }}
.chip-critical {{ color: var(--critical-ink); }} .chip-critical .chip-glyph {{ color: var(--critical); }}
.chip-neutral {{ color: var(--ink-2); }}
section {{ display: grid; gap: 16px; }}
.section-head {{ display: grid; gap: 4px; max-width: 68ch; }}
h2 {{ font-size: 20px; font-weight: 600; margin: 0; letter-spacing: -0.01em; }}
.section-head p {{ margin: 0; color: var(--ink-2); }}
.pair {{ display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 7fr); gap: 16px; align-items: start; }}
@media (max-width: 760px) {{ .pair {{ grid-template-columns: minmax(0, 1fr); }} }}
.card {{ background: var(--surface); border: 1px solid var(--line); border-radius: 6px; padding: 16px 18px; display: grid; gap: 12px; min-width: 0; }}
.card h3 {{ margin: 0; font-size: 13px; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; color: var(--ink-2); }}
.chart {{ width: 100%; height: auto; display: block; overflow: visible; }}
.seg, .col {{ fill: var(--s1); }}
.s1 {{ fill: var(--s1); }} .s2 {{ fill: var(--s2); }} .s3 {{ fill: var(--s3); }} .s-none {{ fill: var(--s-none); }}
.o1 {{ fill: var(--o1); }} .o2 {{ fill: var(--o2); }} .o3 {{ fill: var(--o3); }} .o4 {{ fill: var(--o4); }}
.col-zero {{ fill: var(--axis); }}
.seg:focus-visible, .col:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
.seg-label {{ font: 500 12px var(--sans); fill: #ffffff; pointer-events: none; }}
.s-none + .seg-label {{ fill: var(--ink); }}
.grid {{ stroke: var(--grid); stroke-width: 1; }}
.axis {{ stroke: var(--axis); stroke-width: 1; }}
.tick {{ font: 11px var(--mono); fill: var(--muted); }}
.cap {{ font: 500 12px var(--sans); fill: var(--ink-2); font-variant-numeric: tabular-nums; }}
.legend {{ list-style: none; margin: 0; padding: 0; display: flex; flex-wrap: wrap; gap: 6px 18px; font-size: 13px; color: var(--ink-2); }}
.legend li {{ display: inline-flex; align-items: center; gap: 7px; }}
.swatch {{ width: 10px; height: 10px; border-radius: 2px; display: inline-block; background: var(--s1); }}
.swatch.s1 {{ background: var(--s1); }} .swatch.s2 {{ background: var(--s2); }} .swatch.s3 {{ background: var(--s3); }} .swatch.s-none {{ background: var(--s-none); }}
.note {{ margin: 0; font-size: 13px; color: var(--ink-2); }}
.table-wrap {{ overflow-x: auto; }}
table {{ border-collapse: collapse; width: 100%; font-size: 13.5px; }}
th, td {{ text-align: left; padding: 7px 10px; border-bottom: 1px solid var(--line); vertical-align: top; }}
th {{ font-size: 11.5px; letter-spacing: 0.05em; text-transform: uppercase; color: var(--ink-2); font-weight: 600; white-space: nowrap; }}
td:nth-child(n+2):not(:last-child) {{ white-space: nowrap; }}
td {{ font-variant-numeric: tabular-nums; }}
tr:last-child td {{ border-bottom: 0; }}
.empty {{ margin: 0; color: var(--ink-2); }}
#tip {{ position: fixed; pointer-events: none; background: var(--ink); color: var(--ground); font-size: 12.5px; padding: 6px 9px; border-radius: 4px; max-width: 280px; z-index: 10; }}
#tip[hidden] {{ display: none; }}
@media (prefers-reduced-motion: no-preference) {{ .seg, .col {{ transition: opacity 120ms; }} }}
.seg:hover, .col:hover {{ opacity: 0.85; }}
</style>"""

    body_inner = f"""<main class="page">
<header>
  <h1>Editorial Health</h1>
  <div class="provenance">{provenance} · ages as of {mono(aged.get("as_of", generated_on))}</div>
</header>

<div class="tiles">{tiles}</div>

<section aria-labelledby="coverage">
  <div class="section-head">
    <h2 id="coverage">Coverage</h2>
    <p>How much of the Pali the repository actually quotes is governed by a term record. {fmt_int(coverage['governed_surfaces'])} of {fmt_int(coverage['distinct_surfaces'])} distinct surfaces reach a record; by occurrence, {fmt_pct(coverage['occurrence_coverage_pct'])} of quoted Pali does.</p>
  </div>
  <div class="pair">
    <div class="card"><h3>Surfaces by match route</h3>{coverage_chart}{coverage_legend}
      <p class="note">Inflected and compound matches are heuristic: a lead to check, not a fact.</p></div>
    <div class="card"><h3>Ungoverned, by frequency ({fmt_int(coverage['ungoverned_total'])} total)</h3>{coverage_table}</div>
  </div>
</section>

<section aria-labelledby="drift">
  <div class="section-head">
    <h2 id="drift">Drift</h2>
    <p>Renderings a translation document declares against the record that governs the headword. {fmt_int(drift['declared_renderings'])} declarations across {fmt_int(drift['documents_with_declarations'])} documents; prose is deliberately not scanned.</p>
  </div>
  <div class="pair">
    <div class="card"><h3>Findings by kind</h3>{drift_chart}</div>
    <div class="card"><h3>Findings</h3>{drift_table}</div>
  </div>
</section>

<section aria-labelledby="queue">
  <div class="section-head">
    <h2 id="queue">Review queue</h2>
    <p>Everything waiting on an editorial decision, dated from the commit that added it or the ledger date it carries. Oldest first.</p>
  </div>
  <div class="pair">
    <div class="card"><h3>By waiting time</h3>{queue_chart}</div>
    <div class="card"><h3>Waiting ({fmt_int(queue['total'])})</h3>{queue_table}</div>
  </div>
</section>

<section aria-labelledby="formulas">
  <div class="section-head">
    <h2 id="formulas">Formula agreement</h2>
    <p>Pali phrases quoted by more than one record whose English differs between them — a different question from declared-rendering conflicts, and kept separate so one zero cannot stand in for the other. {fmt_int(formulas['unexplained'])} unexplained, {fmt_int(formulas['waived'])} waived, {fmt_int(formulas['regressions'])} outside the acknowledged baseline.</p>
  </div>
  <div class="card"><h3>Disagreeing formulas</h3>{table(
        ["Formula", "Records", "Renderings"],
        [[mono(g["pali"]), fmt_int(len(g["records"])),
          "<br>".join(f"{mono(k)} {escape(t)}" for k, t in g["renderings"])] for g in formulas["groups"][:top]],
        empty="Every shared formula is rendered the same way wherever it is quoted.")}</div>
</section>

<section aria-labelledby="evidence">
  <div class="section-head">
    <h2 id="evidence">Human review evidence</h2>
    <p>What the newcomer ledger actually records. Every structural check on this page can pass with these at zero. Source verification is not shown: it depends on a cache outside the repository.</p>
  </div>
  <div class="card"><h3>Newcomer ledger</h3>{table(
        ["Measure", "Value"],
        [["Surfaces in the cohort", fmt_int(evidence["surfaces"])],
         ["Source fidelity signed off", fmt_int(evidence["source_fidelity_complete"])],
         ["Human read-aloud complete", fmt_int(evidence["read_aloud_complete"])],
         ["Newcomer reviews recorded", fmt_int(evidence["newcomer_reviews_recorded"])],
         ["Newcomer reviews counting for the current body",
          fmt_int(evidence.get("newcomer_reviews_counting", 0))],
         ["Surfaces validated", fmt_int(evidence["surfaces_validated"])]],
        empty="No ledger.")}</div>
</section>

<section aria-labelledby="failures">
  <div class="section-head">
    <h2 id="failures">Schema and lint failures per week</h2>
    <p>Both checks replayed against every commit and grouped by ISO week. A week reports its worst commit, so a failure that survives several commits counts once.</p>
  </div>
  <div class="pair">
    <div class="card"><h3>Findings per week</h3>{fail_chart}{fail_legend}{f'<p class="note">{escape(fail_note)}</p>' if fail_note else ''}</div>
    <div class="card"><h3>Weeks</h3>{fail_table}</div>
  </div>
</section>
</main>
<div id="tip" role="status" hidden></div>
<script>
(function () {{
  var tip = document.getElementById('tip');
  function show(el, x, y) {{
    tip.textContent = el.getAttribute('data-tip'); tip.hidden = false;
    var w = tip.offsetWidth, h = tip.offsetHeight;
    tip.style.left = Math.min(x + 12, window.innerWidth - w - 8) + 'px';
    tip.style.top = (y - h - 12 < 8 ? y + 16 : y - h - 12) + 'px';
  }}
  function hide() {{ tip.hidden = true; }}
  document.querySelectorAll('[data-tip]').forEach(function (el) {{
    el.addEventListener('mousemove', function (e) {{ show(el, e.clientX, e.clientY); }});
    el.addEventListener('mouseleave', hide);
    el.addEventListener('focus', function () {{ var r = el.getBoundingClientRect(); show(el, r.left + r.width / 2, r.top); }});
    el.addEventListener('blur', hide);
  }});
}})();
</script>"""

    if fragment:
        return head_inner + "\n" + body_inner + "\n"
    return (
        '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"{head_inner}\n</head>\n<body>\n{body_inner}\n</body>\n</html>\n"
    )
