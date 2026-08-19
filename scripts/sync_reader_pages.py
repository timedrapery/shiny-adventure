#!/usr/bin/env python3
"""Keep reader pages in step with the governed translation surfaces.

Each file in `reader-src/suttas/` is a presentation layer over the matching
surface in `docs/translations/`: it keeps its own title and "About this text"
introduction, and then reproduces the governed translation body.

Nothing enforced that agreement before this script existed, so the body could
drift from the surface silently. It has been resynced by hand several times.

Comparison is on content, not bytes. Reader pages legitimately differ in
presentation: heading levels are demoted one step so the page keeps a single
H1, and a page may italicise the closing colophon or add a horizontal rule.
Those differences are normalised away before comparing, so `--check` only fails
on a real content divergence.
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
TRANSLATIONS_DIR = REPO_ROOT / "docs" / "translations"
READER_DIR = REPO_ROOT / "reader-src" / "suttas"

BODY_MARKER = "## Translation"
INTRO_HEADING = "about this text"


def surface_body(text: str) -> str:
    """The governed translation body, with headings demoted one level."""
    if BODY_MARKER not in text:
        raise ValueError(f"surface has no `{BODY_MARKER}` section")
    body = text.split(BODY_MARKER, 1)[1].strip()
    return re.sub(r"^### ", "## ", body, flags=re.M)


def reader_head(text: str) -> str:
    """The reader page's own title and introduction, up to the first body heading."""
    lines = text.splitlines()
    seen_intro = False
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("## "):
            continue
        heading = stripped[3:].strip().casefold()
        if heading == INTRO_HEADING:
            seen_intro = True
            continue
        if seen_intro or index > 0:
            return "\n".join(lines[:index]).rstrip()
    return text.rstrip()


def reader_body(text: str) -> str:
    head = reader_head(text)
    return text[len(head):].strip()


def normalize(body: str) -> str:
    """Reduce a body to comparable content.

    Drops emphasis markers, horizontal rules, and all whitespace differences,
    so presentation-only edits on a reader page do not read as drift.
    """
    out = re.sub(r"^\s*(?:---+|\*\*\*+|___+)\s*$", "", body, flags=re.M)
    out = out.replace("*", "").replace("_", "")
    out = re.sub(r"^#+\s*", "", out, flags=re.M)
    out = re.sub(r"\s+", " ", out)
    return out.strip().casefold()


def pairs(reader_dir: Path, translations_dir: Path) -> list[tuple[Path, Path]]:
    found: list[tuple[Path, Path]] = []
    if not reader_dir.exists():
        return found
    for reader_path in sorted(reader_dir.glob("*.md")):
        surface_path = translations_dir / reader_path.name
        if surface_path.exists():
            found.append((reader_path, surface_path))
    return found


def build_report(
    repo_root: Path = REPO_ROOT,
    reader_dir: Path | None = None,
    translations_dir: Path | None = None,
) -> dict[str, object]:
    reader_dir = reader_dir or READER_DIR
    translations_dir = translations_dir or TRANSLATIONS_DIR

    checked: list[str] = []
    diverged: list[dict[str, str]] = []
    orphans: list[str] = []

    for reader_path in sorted(reader_dir.glob("*.md")) if reader_dir.exists() else []:
        if not (translations_dir / reader_path.name).exists():
            orphans.append(reader_path.name)

    for reader_path, surface_path in pairs(reader_dir, translations_dir):
        try:
            relative = reader_path.relative_to(repo_root).as_posix()
        except ValueError:
            relative = reader_path.as_posix()
        checked.append(relative)

        want = surface_body(surface_path.read_text(encoding="utf-8"))
        have = reader_body(reader_path.read_text(encoding="utf-8"))
        if normalize(want) != normalize(have):
            diff = difflib.unified_diff(
                normalize(have).split(" "),
                normalize(want).split(" "),
                lineterm="",
                n=6,
            )
            diverged.append({"path": relative, "diff": " ".join(list(diff)[:120])})

    return {
        "summary": {"checked": len(checked), "diverged": len(diverged), "orphans": len(orphans)},
        "diverged": diverged,
        "orphans": orphans,
    }


def write_pages(
    repo_root: Path = REPO_ROOT,
    reader_dir: Path | None = None,
    translations_dir: Path | None = None,
) -> list[str]:
    reader_dir = reader_dir or READER_DIR
    translations_dir = translations_dir or TRANSLATIONS_DIR
    written: list[str] = []

    for reader_path, surface_path in pairs(reader_dir, translations_dir):
        text = reader_path.read_text(encoding="utf-8")
        want = surface_body(surface_path.read_text(encoding="utf-8"))
        have = reader_body(text)
        if normalize(want) == normalize(have):
            continue
        head = reader_head(text)
        reader_path.write_text(f"{head}\n\n{want}\n", encoding="utf-8", newline="\n")
        try:
            written.append(reader_path.relative_to(repo_root).as_posix())
        except ValueError:
            written.append(reader_path.as_posix())
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if any reader page has drifted.")
    parser.add_argument("--write", action="store_true", help="Rewrite reader bodies from their surfaces.")
    args = parser.parse_args()

    if args.write:
        written = write_pages()
        if written:
            for path in written:
                print(f"resynced {path}")
        else:
            print("Reader pages already match their surfaces.")
        return 0

    report = build_report()
    summary = report["summary"]

    if report["orphans"]:
        for name in report["orphans"]:
            print(f"- {name}: no matching surface in docs/translations/")

    if not report["diverged"]:
        print(f"Reader pages match their surfaces ({summary['checked']} checked).")
        return 1 if (args.check and report["orphans"]) else 0

    print(f"Reader pages out of sync ({summary['diverged']} of {summary['checked']}):")
    for entry in report["diverged"]:
        print(f"- {entry['path']}")
    print("")
    print("Run `python scripts/sync_reader_pages.py --write` to rebuild them")
    print("from the governed surfaces.")
    return 1 if args.check else 0


if __name__ == "__main__":
    sys.exit(main())
