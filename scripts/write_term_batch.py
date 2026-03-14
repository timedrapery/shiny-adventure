#!/usr/bin/env python3
"""Write term entry batches to terms/ using explicit UTF-8 output."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
TERMS_DIR = REPO_ROOT / "terms"
PROTECTED_TEXT_FIELDS = (
    "term",
    "preferred_translation",
    "literal_meaning",
    "definition",
    "gloss_on_first_occurrence",
)


def load_batch(path: Path) -> list[dict[str, object]]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError("Batch file must contain a JSON array of term records.")
    records: list[dict[str, object]] = []
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Record {index} is not a JSON object.")
        records.append(item)
    return records


def validate_record(record: dict[str, object], index: int) -> str:
    normalized_term = record.get("normalized_term")
    if not isinstance(normalized_term, str) or not normalized_term:
        raise ValueError(f"Record {index} is missing a string normalized_term.")
    if any(ch not in "abcdefghijklmnopqrstuvwxyz0123456789-_" for ch in normalized_term):
        raise ValueError(
            f"Record {index} has non-ASCII normalized_term '{normalized_term}'."
        )
    for field in PROTECTED_TEXT_FIELDS:
        value = record.get(field)
        if isinstance(value, str) and "?" in value:
            raise ValueError(
                f"Record {index} field '{field}' contains '?'; refusing to write likely corrupted text."
            )
    return normalized_term


def write_record(record: dict[str, object], destination: Path) -> None:
    with destination.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(record, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch_file", type=Path, help="Path to a JSON array of term records.")
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Validate the batch without writing any files.",
    )
    args = parser.parse_args()

    if not TERMS_DIR.exists():
        print(f"ERROR: Terms directory not found: {TERMS_DIR}")
        return 1

    try:
        records = load_batch(args.batch_file)
        planned_writes: list[tuple[dict[str, object], Path]] = []
        for index, record in enumerate(records, start=1):
            normalized_term = validate_record(record, index)
            planned_writes.append((record, TERMS_DIR / f"{normalized_term}.json"))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 1

    if args.check_only:
        print(f"Validated {len(planned_writes)} record(s) without writing files.")
        return 0

    for record, destination in planned_writes:
        write_record(record, destination)

    print(f"Wrote {len(planned_writes)} term file(s) to {TERMS_DIR}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
