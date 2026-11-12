#!/usr/bin/env python3
"""Shared helpers for the `*_cluster_report.py` scripts.

Each cluster script keeps what is its own: its term lists, its checks, and the
sheets it writes. This module holds the parts they all share: loading term
records, the common checks, the text report, and the command line.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from types import ModuleType

try:
    from scripts.text_utils import safe_text
    from scripts.term_store import iter_term_files
except ModuleNotFoundError:
    from text_utils import safe_text
    from term_store import iter_term_files


REPO_ROOT = Path(__file__).resolve().parent.parent
TERMS_DIR = REPO_ROOT / "terms"
OUTPUT_DIR = REPO_ROOT / "docs" / "generated"

Terms = dict[str, dict[str, object]]


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_terms(terms_dir: Path = TERMS_DIR) -> Terms:
    terms: Terms = {}
    for path in iter_term_files(terms_dir):
        data = load_json(path)
        if isinstance(data, dict):
            terms[path.stem] = data
    return terms


def missing_terms(terms: Terms, stems: list[str]) -> list[str]:
    return [stem for stem in stems if stem not in terms]


def example_source_gaps(terms: Terms, stems: list[str]) -> list[str]:
    """Terms with no example phrases, or an example without a source."""
    gaps: list[str] = []
    for stem in stems:
        data = terms.get(stem)
        if not isinstance(data, dict):
            continue
        examples = data.get("example_phrases")
        if not isinstance(examples, list) or not examples:
            gaps.append(stem)
            continue
        if any(not isinstance(item, dict) or not item.get("source") for item in examples):
            gaps.append(stem)
    return gaps


def weak_authority_terms(terms: Terms, stems: list[str]) -> list[str]:
    """Terms with fewer than two authority sources."""
    weak: list[str] = []
    for stem in stems:
        data = terms.get(stem)
        if not isinstance(data, dict):
            continue
        authority = data.get("authority_basis")
        if not isinstance(authority, list) or len(authority) < 2:
            weak.append(stem)
    return weak


def contains_all(blob: str, tokens: list[str]) -> bool:
    return all(token in blob for token in tokens)


def summary_lines(summary: dict[str, object]) -> list[str]:
    """One line per `<name>_present` / `<name>_expected` pair, in order."""
    lines: list[str] = []
    for key in summary:
        if key.endswith("_present"):
            name = key[: -len("_present")]
            label = name.replace("_", " ").capitalize()
            lines.append(f"- {label}: {summary[key]} / {summary[name + '_expected']}")
    return lines


def print_text_report(title: str, report: dict[str, object]) -> None:
    print(title)
    for line in summary_lines(report["summary"]):
        print(line)
    for heading in ("errors", "warnings"):
        print()
        print(heading.capitalize())
        for key, items in report[heading].items():
            if items:
                print(f"- {safe_text(key)}: {', '.join(safe_text(item) for item in items)}")
            else:
                print(f"- {safe_text(key)}: none")


def run_cli(module: ModuleType) -> int:
    """The shared command line for a cluster script.

    It looks up `load_terms`, `build_report`, `write_outputs`, and
    `print_text_report` on the script module, so tests can patch them there.
    """
    parser = argparse.ArgumentParser(description=module.__doc__)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--strict", action="store_true", help="Fail if the report has errors.")
    parser.add_argument("--write-docs", action="store_true", help="Write generated docs to docs/generated.")
    args = parser.parse_args()

    if not module.TERMS_DIR.exists():
        print(f"ERROR: Terms directory not found: {module.TERMS_DIR}")
        return 1

    terms = module.load_terms()
    report = module.build_report(terms)

    if args.write_docs:
        module.write_outputs(terms)

    if args.format == "json":
        json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        module.print_text_report(report)

    if args.strict and any(report["errors"].values()):
        return 1
    return 0
