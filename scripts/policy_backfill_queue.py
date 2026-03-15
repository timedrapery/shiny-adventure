#!/usr/bin/env python3
"""Rank major terms that should be prioritized for metadata backfill."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from scripts.text_utils import safe_text
    from scripts.term_store import iter_term_files
except ModuleNotFoundError:
    from text_utils import safe_text
    from term_store import iter_term_files


REPO_ROOT = Path(__file__).resolve().parent.parent
TERMS_DIR = REPO_ROOT / "terms"
PRIORITY_TAG_WEIGHTS = {
    "core-doctrine": 7,
    "core-practice": 6,
    "translation-sensitive": 5,
    "dependent-origination": 4,
    "four-noble-truths": 4,
}
STATUS_WEIGHTS = {
    "stable": 10,
    "reviewed": 6,
    "draft": 2,
}


@dataclass(frozen=True)
class QueueItem:
    term: str
    score: int
    missing_fields: tuple[str, ...]
    refinement_fields: tuple[str, ...]
    status: str
    tags: tuple[str, ...]


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


def build_queue(terms: dict[str, dict[str, object]]) -> list[QueueItem]:
    queue: list[QueueItem] = []
    for stem, data in sorted(terms.items()):
        if data.get("entry_type") != "major":
            continue

        missing_fields = []
        if not data.get("authority_basis"):
            missing_fields.append("authority_basis")
        if not data.get("translation_policy"):
            missing_fields.append("translation_policy")
        refinement_fields = []
        authority_basis = data.get("authority_basis")
        if isinstance(authority_basis, list):
            for item in authority_basis:
                if isinstance(item, dict) and item.get("source") == "Repository editorial record":
                    refinement_fields.append("authority_basis_source")
                    break

        if not missing_fields and not refinement_fields:
            continue

        score = STATUS_WEIGHTS.get(str(data.get("status")), 0)
        tags = tuple(tag for tag in data.get("tags", []) if isinstance(tag, str))
        for tag in tags:
            score += PRIORITY_TAG_WEIGHTS.get(tag, 0)
        if data.get("untranslated_preferred") is True:
            score += 3
        if len(missing_fields) == 2:
            score += 2
        if refinement_fields:
            score += 1

        queue.append(
            QueueItem(
                term=stem,
                score=score,
                missing_fields=tuple(missing_fields),
                refinement_fields=tuple(refinement_fields),
                status=str(data.get("status", "")),
                tags=tags,
            )
        )

    queue.sort(key=lambda item: (-item.score, item.term))
    return queue


def print_text(queue: list[QueueItem], *, top: int) -> None:
    print("Policy Backfill Queue")
    if not queue:
        print("- None")
        return

    for item in queue[:top]:
        missing = ", ".join(item.missing_fields) if item.missing_fields else "-"
        refine = ", ".join(item.refinement_fields) if item.refinement_fields else "-"
        tags = ", ".join(item.tags) if item.tags else "-"
        print(
            f"- {safe_text(item.term)}: score {item.score}; missing {missing}; refine {refine}; status {item.status}; tags {safe_text(tags)}"
        )
    if len(queue) > top:
        print(f"- ... {len(queue) - top} more term(s)")


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
        default=25,
        help="Number of rows to show in text mode.",
    )
    args = parser.parse_args()

    if not TERMS_DIR.exists():
        print(f"ERROR: Terms directory not found: {TERMS_DIR}")
        return 1

    terms = load_terms()
    if not terms:
        print("WARNING: No term files found in terms/")
        return 0

    queue = build_queue(terms)
    if args.format == "json":
        json.dump([item.__dict__ for item in queue], sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        print_text(queue, top=args.top)
    return 0


if __name__ == "__main__":
    sys.exit(main())
