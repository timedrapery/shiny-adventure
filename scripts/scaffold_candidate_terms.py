#!/usr/bin/env python3
"""Scaffold review packets for extracted candidates without writing term entries."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
CANDIDATES_DIR = REPO_ROOT / "candidates"
DEFAULT_INPUT = CANDIDATES_DIR / "candidate_terms.json"
DEFAULT_OUTPUT_DIR = CANDIDATES_DIR / "scaffolds"


def load_report(path: Path) -> dict[str, object]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("Candidate report must be a JSON object.")
    return data


def build_review_packet(candidate: dict[str, object]) -> dict[str, object]:
    matched_terms = candidate.get("matched_terms", [])
    suggested_type = "major" if candidate.get("doctrinal_signal") or candidate.get("formula_signal") else "minor"
    return {
        "candidate_term": candidate.get("text"),
        "normalized_term": candidate.get("normalized"),
        "review_status": "review-required",
        "suggested_entry_type": suggested_type,
        "do_not_merge_into_terms_without_editorial_review": True,
        "source_evidence": {
            "total_count": candidate.get("total_count"),
            "document_count": candidate.get("document_count"),
            "document_paths": candidate.get("document_paths", []),
            "snippets": candidate.get("snippets", []),
        },
        "priority": candidate.get("priority"),
        "reasons": candidate.get("reasons", []),
        "possible_existing_matches": matched_terms,
        "editorial_todo": [
            "Confirm the headword spelling and normalization.",
            "Check whether this should be a new term or an existing-term variant.",
            "Do not approve a preferred_translation without house-style review.",
            "If promoted to a real term entry, follow STYLE_GUIDE.md and TERM_ENTRY_STANDARD.md.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="Candidate extraction JSON file.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for review packet JSON files.",
    )
    parser.add_argument(
        "--priority",
        choices=("create_now", "review_soon", "low_priority"),
        default="create_now",
        help="Minimum priority to scaffold.",
    )
    args = parser.parse_args()

    try:
        report = load_report(args.input)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 1

    candidates = report.get("candidates", [])
    if not isinstance(candidates, list):
        print("ERROR: Candidate report is missing a candidates list.")
        return 1

    priority_order = {"create_now": 0, "review_soon": 1, "low_priority": 2, "ignore": 3}
    threshold = priority_order[args.priority]
    selected = [
        item for item in candidates
        if isinstance(item, dict)
        and priority_order.get(str(item.get("priority")), 99) <= threshold
        and item.get("status") != "covered"
    ]

    args.output_dir.mkdir(parents=True, exist_ok=True)
    written = 0
    for item in selected:
        normalized = item.get("normalized")
        if not isinstance(normalized, str) or not normalized:
            continue
        output_path = args.output_dir / f"{normalized}.review.json"
        output_path.write_text(
            json.dumps(build_review_packet(item), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        written += 1

    print(f"Wrote {written} candidate review packet(s) to {args.output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
