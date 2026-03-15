#!/usr/bin/env python3
"""Render a Markdown review report from candidate extraction JSON."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
CANDIDATES_DIR = REPO_ROOT / "candidates"
DEFAULT_INPUT = CANDIDATES_DIR / "candidate_terms.json"
DEFAULT_OUTPUT = CANDIDATES_DIR / "candidate_terms.md"
PRIORITY_ORDER = ("create_now", "review_soon", "low_priority", "ignore")


def load_report(path: Path) -> dict[str, object]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("Candidate report must be a JSON object.")
    return data


def render_candidate(candidate: dict[str, object]) -> str:
    reasons = ", ".join(candidate.get("reasons", []))
    matched = ", ".join(candidate.get("matched_terms", [])) or "none"
    snippets = candidate.get("snippets", [])
    snippet_line = ""
    if isinstance(snippets, list) and snippets:
        first = snippets[0]
        if isinstance(first, dict):
            snippet_line = f" | example: {first.get('path')}:{first.get('line')} `{first.get('snippet', '')}`"
    return (
        f"- `{candidate.get('text')}` | count {candidate.get('total_count')} | docs {candidate.get('document_count')} "
        f"| status {candidate.get('status')} | matches {matched} | {reasons}{snippet_line}"
    )


def render_markdown(report: dict[str, object]) -> str:
    summary = report.get("summary", {})
    candidates = report.get("candidates", [])
    sources = report.get("source_documents", [])
    if not isinstance(summary, dict) or not isinstance(candidates, list) or not isinstance(sources, list):
        raise ValueError("Candidate report has invalid structure.")

    lines = [
        "# Candidate Term Report",
        "",
        "## Source Files",
        "",
    ]
    for source in sources:
        lines.append(f"- `{source}`")

    lines.extend(
        [
            "",
            "## Summary",
            "",
            f"- Documents scanned: {summary.get('documents', 0)}",
            f"- Candidates found: {summary.get('total_candidates', 0)}",
        ]
    )

    priority_counts = summary.get("priority_counts", {})
    if isinstance(priority_counts, dict):
        for priority in PRIORITY_ORDER:
            lines.append(f"- {priority}: {priority_counts.get(priority, 0)}")

    lines.append("")

    for priority in PRIORITY_ORDER:
        lines.append(f"## {priority.replace('_', ' ').title()}")
        lines.append("")
        priority_items = [
            item for item in candidates
            if isinstance(item, dict) and item.get("priority") == priority
        ]
        if not priority_items:
            lines.append("- None")
            lines.append("")
            continue
        for item in priority_items:
            lines.append(render_candidate(item))
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="Candidate extraction JSON file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Markdown report destination.",
    )
    args = parser.parse_args()

    try:
        report = load_report(args.input)
        markdown = render_markdown(report)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(markdown, encoding="utf-8")
    print(f"Wrote candidate review report to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
