#!/usr/bin/env python3
"""Generate navigation indexes for the flat terms/major and terms/minor directories."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

try:
    from scripts.term_store import iter_term_files
except ModuleNotFoundError:
    from term_store import iter_term_files


REPO_ROOT = Path(__file__).resolve().parent.parent
TERMS_DIR = REPO_ROOT / "terms"
OUTPUT_DIR = REPO_ROOT / "docs" / "generated"
OUTPUTS = {
    "major": OUTPUT_DIR / "major-term-index.md",
    "minor": OUTPUT_DIR / "minor-term-index.md",
}


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def load_json(path: Path) -> dict[str, object]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Term file is not a JSON object: {path}")
    return data


def collect_records(entry_type: str) -> list[dict[str, object]]:
    directory = TERMS_DIR / entry_type
    records: list[dict[str, object]] = []
    for path in sorted(directory.glob("*.json")):
        data = load_json(path)
        records.append(
            {
                "stem": path.stem,
                "path": path.relative_to(REPO_ROOT).as_posix(),
                "term": data.get("term", path.stem),
                "preferred_translation": data.get("preferred_translation", ""),
                "status": data.get("status", ""),
                "tags": ", ".join(data.get("tags", [])) if isinstance(data.get("tags"), list) else "",
            }
        )
    return records


def render_index(entry_type: str, records: list[dict[str, object]]) -> str:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for record in records:
        stem = str(record["stem"])
        grouped[stem[0].upper()].append(record)

    lines = [
        f"# {entry_type.title()} Term Index",
        "",
        f"Generated navigation index for the flat `terms/{entry_type}/` directory.",
        "",
        f"- Entries: {len(records)}",
        "- Structure decision: keep the on-disk directory flat and rely on generated navigation for human browsing.",
        "",
    ]

    for letter in sorted(grouped):
        lines.append(f"## {letter}")
        lines.append("")
        lines.append("| Stem | Pali | Preferred | Status | Tags |")
        lines.append("| --- | --- | --- | --- | --- |")
        for record in grouped[letter]:
            lines.append(
                "| "
                f"[{record['stem']}](../../{record['path']}) | "
                f"{record['term']} | "
                f"{record['preferred_translation'] or '-'} | "
                f"{record['status'] or '-'} | "
                f"{record['tags'] or '-'} |"
            )
        lines.append("")
    return "\n".join(lines)


def build_outputs() -> dict[Path, str]:
    major_records = collect_records("major")
    minor_records = collect_records("minor")
    return {
        OUTPUTS["major"]: render_index("major", major_records),
        OUTPUTS["minor"]: render_index("minor", minor_records),
    }


def write_outputs(outputs: dict[Path, str]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for path, content in outputs.items():
        path.write_text(content + "\n", encoding="utf-8")


def check_outputs(outputs: dict[Path, str]) -> list[str]:
    failures: list[str] = []
    for path, content in outputs.items():
        expected = content + "\n"
        if not path.exists():
            failures.append(f"Missing generated navigation file: {display_path(path)}")
            continue
        current = path.read_text(encoding="utf-8")
        if current != expected:
            failures.append(f"Stale generated navigation file: {display_path(path)}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-docs", action="store_true", help="Write generated navigation indexes.")
    parser.add_argument("--check", action="store_true", help="Fail if generated navigation indexes are missing or stale.")
    args = parser.parse_args()

    outputs = build_outputs()

    if args.write_docs:
        write_outputs(outputs)

    if args.check:
        failures = check_outputs(outputs)
        if failures:
            print("Term directory navigation check failed:\n")
            for failure in failures:
                print(f"- {failure}")
            return 1

    if not args.check:
        for path in outputs:
            print(display_path(path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
