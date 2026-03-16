#!/usr/bin/env python3
"""Report the current queue of draft major entries that still need editorial review."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

try:
    from scripts.term_store import iter_term_files
except ModuleNotFoundError:
    from term_store import iter_term_files


REPO_ROOT = Path(__file__).resolve().parent.parent
TERMS_DIR = REPO_ROOT / "terms"


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_terms(terms_dir: Path = TERMS_DIR) -> dict[str, dict[str, object]]:
    terms: dict[str, dict[str, object]] = {}
    for path in iter_term_files(terms_dir):
        data = load_json(path)
        if isinstance(data, dict):
            terms[path.stem] = data
    return terms


def collect_draft_major_entries(terms: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for stem, data in sorted(terms.items()):
        if data.get("entry_type") != "major" or data.get("status") != "draft":
            continue
        tags = [tag for tag in data.get("tags", []) if isinstance(tag, str)]
        related_terms = [term for term in data.get("related_terms", []) if isinstance(term, str)]
        references = [ref for ref in data.get("sutta_references", []) if isinstance(ref, str)]
        entries.append(
            {
                "normalized_term": stem,
                "term": data.get("term", stem),
                "preferred_translation": data.get("preferred_translation", ""),
                "tags": tags,
                "related_terms": related_terms,
                "sutta_references": references,
            }
        )
    return entries


def build_report(terms: dict[str, dict[str, object]]) -> dict[str, object]:
    major_total = sum(1 for data in terms.values() if data.get("entry_type") == "major")
    queue = collect_draft_major_entries(terms)
    tag_counter = Counter(tag for entry in queue for tag in entry["tags"])
    tag_clusters = [
        {"tag": tag, "draft_terms": count}
        for tag, count in sorted(tag_counter.items(), key=lambda item: (-item[1], item[0]))
    ]

    return {
        "summary": {
            "draft_major_terms": len(queue),
            "major_terms": major_total,
            "reviewed_or_stable_major_terms": max(major_total - len(queue), 0),
        },
        "tag_clusters": tag_clusters,
        "queue": queue,
    }


def print_text_report(report: dict[str, object], *, top_tags: int) -> None:
    summary = report["summary"]
    tag_clusters = report["tag_clusters"]
    queue = report["queue"]

    print("Draft Major Review Queue")
    print(f"- Draft major terms: {summary['draft_major_terms']}")
    print(f"- Total major terms: {summary['major_terms']}")
    print(f"- Reviewed or stable major terms: {summary['reviewed_or_stable_major_terms']}")
    print()

    print("Draft Tag Clusters")
    if not tag_clusters:
        print("- None")
    else:
        for cluster in tag_clusters[:top_tags]:
            print(f"- {cluster['tag']}: {cluster['draft_terms']} draft term(s)")
        if len(tag_clusters) > top_tags:
            print(f"- ... {len(tag_clusters) - top_tags} more tag cluster(s)")
    print()

    print("Queue")
    if not queue:
        print("- None")
        return

    for entry in queue:
        tags = ", ".join(entry["tags"]) or "<none>"
        related = ", ".join(entry["related_terms"]) or "<none>"
        refs = ", ".join(entry["sutta_references"]) or "<none>"
        print(
            f"- {entry['normalized_term']} ({entry['term']}): {entry['preferred_translation']} | "
            f"tags {tags} | related {related} | refs {refs}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format.",
    )
    parser.add_argument(
        "--top-tags",
        type=int,
        default=10,
        help="Number of tag clusters to show in text mode.",
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
        print_text_report(report, top_tags=args.top_tags)
    return 0


if __name__ == "__main__":
    sys.exit(main())