#!/usr/bin/env python3
"""Report repository health signals for editorial scalability and automation."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

try:
    from scripts.text_utils import safe_text
except ModuleNotFoundError:
    from text_utils import safe_text


REPO_ROOT = Path(__file__).resolve().parent.parent
TERMS_DIR = REPO_ROOT / "terms"


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_terms(terms_dir: Path = TERMS_DIR) -> dict[str, dict[str, object]]:
    terms: dict[str, dict[str, object]] = {}
    for path in sorted(terms_dir.glob("*.json")):
        data = load_json(path)
        if isinstance(data, dict):
            terms[path.stem] = data
    return terms


def compute_summary(terms: dict[str, dict[str, object]]) -> dict[str, object]:
    entry_types = Counter(str(data.get("entry_type", "<missing>")) for data in terms.values())
    statuses = Counter(str(data.get("status", "<missing>")) for data in terms.values())
    major_terms = {stem: data for stem, data in terms.items() if data.get("entry_type") == "major"}

    return {
        "term_files": len(terms),
        "major_terms": len(major_terms),
        "minor_terms": entry_types.get("minor", 0),
        "stable_terms": statuses.get("stable", 0),
        "reviewed_terms": statuses.get("reviewed", 0),
        "draft_terms": statuses.get("draft", 0),
        "untranslated_preferred_terms": sum(
            1 for data in terms.values() if data.get("untranslated_preferred") is True
        ),
    }


def collect_major_missing_advanced_fields(
    terms: dict[str, dict[str, object]],
) -> dict[str, list[str]]:
    missing = {
        "authority_basis": [],
        "translation_policy": [],
    }
    for stem, data in sorted(terms.items()):
        if data.get("entry_type") != "major":
            continue
        if not data.get("authority_basis"):
            missing["authority_basis"].append(stem)
        if not data.get("translation_policy"):
            missing["translation_policy"].append(stem)
    return missing


def collect_generic_authority_basis_terms(
    terms: dict[str, dict[str, object]]
) -> list[str]:
    generic_terms: list[str] = []
    for stem, data in sorted(terms.items()):
        authority_basis = data.get("authority_basis")
        if not isinstance(authority_basis, list):
            continue
        for item in authority_basis:
            if isinstance(item, dict) and item.get("source") == "Repository editorial record":
                generic_terms.append(stem)
                break
    return generic_terms


def collect_example_source_gaps(terms: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    gaps: list[dict[str, object]] = []
    for stem, data in sorted(terms.items()):
        if data.get("entry_type") != "major":
            continue
        examples = data.get("example_phrases", [])
        if not isinstance(examples, list) or not examples:
            continue
        missing = [
            index + 1
            for index, example in enumerate(examples)
            if isinstance(example, dict) and not example.get("source")
        ]
        if missing:
            gaps.append(
                {
                    "term": stem,
                    "missing_example_indexes": missing,
                    "total_examples": len(examples),
                }
            )
    return gaps


def collect_example_source_gap_tags(
    terms: dict[str, dict[str, object]],
    gaps: list[dict[str, object]],
) -> list[dict[str, object]]:
    counts: defaultdict[str, int] = defaultdict(int)
    for gap in gaps:
        data = terms.get(gap["term"], {})
        tags = data.get("tags", [])
        if isinstance(tags, list):
            for tag in tags:
                if isinstance(tag, str):
                    counts[tag] += 1
    ranked = [
        {"tag": tag, "terms_with_source_gaps": count}
        for tag, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]
    return ranked


def collect_preferred_translation_collisions(
    terms: dict[str, dict[str, object]]
) -> list[dict[str, object]]:
    collisions: defaultdict[str, list[str]] = defaultdict(list)
    for stem, data in sorted(terms.items()):
        if data.get("entry_type") != "major":
            continue
        preferred = data.get("preferred_translation")
        if isinstance(preferred, str) and preferred.strip():
            collisions[preferred].append(stem)

    results = []
    for preferred, stems in sorted(collisions.items()):
        if len(stems) > 1:
            results.append({"preferred_translation": preferred, "terms": stems})
    results.sort(key=lambda item: (-len(item["terms"]), item["preferred_translation"]))
    return results


def build_report(terms: dict[str, dict[str, object]]) -> dict[str, object]:
    summary = compute_summary(terms)
    missing_advanced = collect_major_missing_advanced_fields(terms)
    generic_authority_terms = collect_generic_authority_basis_terms(terms)
    example_source_gaps = collect_example_source_gaps(terms)
    example_source_gap_tags = collect_example_source_gap_tags(terms, example_source_gaps)
    translation_collisions = collect_preferred_translation_collisions(terms)

    return {
        "summary": summary,
        "major_policy_coverage": {
            "authority_basis_missing": missing_advanced["authority_basis"],
            "translation_policy_missing": missing_advanced["translation_policy"],
            "generic_authority_basis": generic_authority_terms,
        },
        "example_source_gaps": example_source_gaps,
        "example_source_gap_tags": example_source_gap_tags,
        "preferred_translation_collisions": translation_collisions,
    }


def print_text_report(report: dict[str, object], *, top: int) -> None:
    summary = report["summary"]
    policy = report["major_policy_coverage"]
    example_source_gaps = report["example_source_gaps"]
    example_source_gap_tags = report["example_source_gap_tags"]
    collisions = report["preferred_translation_collisions"]

    print("Repository Health")
    print(f"- Term files: {summary['term_files']}")
    print(f"- Major terms: {summary['major_terms']}")
    print(f"- Minor terms: {summary['minor_terms']}")
    print(f"- Stable terms: {summary['stable_terms']}")
    print(f"- Reviewed terms: {summary['reviewed_terms']}")
    print(f"- Draft terms: {summary['draft_terms']}")
    print(f"- Terms preferring Pali untranslated: {summary['untranslated_preferred_terms']}")
    print()

    print("Major Policy Coverage")
    print(f"- Missing authority_basis: {len(policy['authority_basis_missing'])}")
    print(f"- Missing translation_policy: {len(policy['translation_policy_missing'])}")
    print(f"- Generic authority_basis needing refinement: {len(policy['generic_authority_basis'])}")
    print()

    print("Example Source Gaps")
    if not example_source_gaps:
        print("- None")
    else:
        for gap in example_source_gaps[:top]:
            indexes = ", ".join(str(index) for index in gap["missing_example_indexes"])
            print(
                f"- {safe_text(gap['term'])}: missing source on example(s) {indexes} of {gap['total_examples']}"
            )
        if len(example_source_gaps) > top:
            remaining = len(example_source_gaps) - top
            print(f"- ... {remaining} more term(s)")
    print()

    print("Example Source Gap Families")
    if not example_source_gap_tags:
        print("- None")
    else:
        for item in example_source_gap_tags[:top]:
            print(f"- {safe_text(item['tag'])}: {item['terms_with_source_gaps']} term(s)")
        if len(example_source_gap_tags) > top:
            remaining = len(example_source_gap_tags) - top
            print(f"- ... {remaining} more tag group(s)")
    print()

    print("Preferred Translation Collisions")
    if not collisions:
        print("- None")
    else:
        for collision in collisions[:top]:
            terms = ", ".join(safe_text(term) for term in collision["terms"])
            print(f"- {safe_text(collision['preferred_translation'])}: {terms}")
        if len(collisions) > top:
            remaining = len(collisions) - top
            print(f"- ... {remaining} more collision group(s)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format.",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=15,
        help="Number of rows to show for long sections in text mode.",
    )
    args = parser.parse_args()

    if not TERMS_DIR.exists():
        print(f"ERROR: Terms directory not found: {TERMS_DIR}")
        return 1

    terms = load_terms()
    if not terms:
        print("WARNING: No term files found in terms/")
        return 0

    report = build_report(terms)
    if args.format == "json":
        json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        print_text_report(report, top=args.top)
    return 0


if __name__ == "__main__":
    sys.exit(main())
