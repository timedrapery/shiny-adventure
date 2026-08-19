#!/usr/bin/env python3
"""Detect Markdown list structure destroyed by paragraph rewriting.

A paragraph-aware rewriter treats everything between blank lines as one
paragraph and re-wraps it. Where a bulleted list has no blank line between its
items, that flattens the list into running prose and leaves the bullet markers
stranded mid-line:

    say. - The same pattern holds for water, fire, air, ...

This actually happened: MN 118's breath-training lists were flattened in commit
7819ad5 and survived three further commits, because nothing in the suite looked
at list structure. This check exists so that cannot happen twice.

It is intentionally narrow. It looks for a bullet marker appearing mid-line
after sentence-ending punctuation, which is the signature of the damage, rather
than trying to validate Markdown generally.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ROOTS = ("docs/translations", "reader-src")

# A bullet marker stranded inside a line, directly after the end of a sentence
# or a closing quote. Requiring sentence-ending punctuation before the marker
# is what separates real damage -- `say. - The same pattern` and
# `long.' - Breathing in short` -- from a hyphen used as ordinary punctuation,
# as in `regard self in this way - 'My self ...'`, which is not damage.
#
# Numbered lists are deliberately not checked: a sentence ending in a numeral
# (`... in perception 7. The distinction ...`) is common in the notes files and
# indistinguishable from a flattened ordered list without more context than
# this check should carry.
STRANDED_MARKER = re.compile(r"[.!?'\"”’)] +[-*] +[A-Z“\"']")


def iter_markdown(roots: tuple[str, ...], repo_root: Path = REPO_ROOT) -> list[Path]:
    files: list[Path] = []
    for name in roots:
        base = repo_root / name
        if base.is_file():
            files.append(base)
        elif base.is_dir():
            files.extend(sorted(base.rglob("*.md")))
    return files


def scan_text(text: str, relative: str) -> list[str]:
    problems: list[str] = []
    in_fence = False
    for number, line in enumerate(text.splitlines(), start=1):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if STRANDED_MARKER.search(line):
            problems.append(f"{relative}:{number}: {line.strip()[:88]}")
    return problems


def collect(roots: tuple[str, ...] = DEFAULT_ROOTS,
            repo_root: Path = REPO_ROOT) -> list[str]:
    problems: list[str] = []
    for path in iter_markdown(roots, repo_root):
        try:
            relative = path.relative_to(repo_root).as_posix()
        except ValueError:
            relative = path.as_posix()
        problems.extend(scan_text(path.read_text(encoding="utf-8"), relative))
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", action="append", dest="roots",
                        help="Directory or file to scan. Repeatable.")
    args = parser.parse_args()
    roots = tuple(args.roots) if args.roots else DEFAULT_ROOTS

    problems = collect(roots)
    if not problems:
        print("Markdown list structure is intact.")
        return 0
    print("Markdown list structure looks damaged:")
    for problem in problems:
        print(f"- {problem}")
    print("")
    print("A bullet marker mid-line usually means a list was flattened by a")
    print("paragraph rewriter. Restore the line breaks before the list items.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
