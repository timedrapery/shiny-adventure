#!/usr/bin/env python3
"""Check and regenerate the registered translation-surface index."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from scripts.surface_registry import TRANSLATION_SURFACES, TranslationSurface, REPO_ROOT
except ModuleNotFoundError:
    from surface_registry import TRANSLATION_SURFACES, TranslationSurface, REPO_ROOT


TRANSLATIONS_DIR = REPO_ROOT / "docs" / "translations"
INDEX_PATH = TRANSLATIONS_DIR / "translation-documents.md"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def render_index(surfaces: tuple[TranslationSurface, ...] | None = None) -> str:
    effective_surfaces = surfaces or TRANSLATION_SURFACES
    lines = [
        "# Translation Documents",
        "",
        "This directory holds shareable, reader-facing translation documents produced",
        "from the repository's current term policy.",
        "",
        "The primary product format is Markdown:",
        "",
        "- readable directly on GitHub",
        "- easy to copy as plain text into email or chat",
        "- easy to convert later to PDF, print layout, or webpage presentation",
        "",
        "These files are the outward-facing translation surface.",
        "",
        "Supporting policy remains in `terms/`, while the documents here are meant to be",
        "read and shared as complete texts.",
        "",
        "This index is generated from `scripts/surface_registry.py` so translation",
        "pairs remain explicit and machine-checkable.",
        "",
    ]

    for surface in effective_surfaces:
        main_name = surface.main_name
        notes_name = surface.notes_name
        lines.extend(
            [
                f"Current {surface.label} surfaces:",
                "",
                f"- [{main_name}]({main_name}): main shareable translation text",
                f"- [{notes_name}]({notes_name}): companion translator notes and rationale",
                "",
            ]
        )

    return "\n".join(lines).rstrip() + "\n"


def collect_surface_failures(
    repo_root: Path | None = None,
    surfaces: tuple[TranslationSurface, ...] | None = None,
    *,
    index_path: Path | None = None,
) -> list[str]:
    effective_repo_root = repo_root or REPO_ROOT
    effective_surfaces = surfaces or TRANSLATION_SURFACES
    failures: list[str] = []
    effective_index_path = index_path or (
        effective_repo_root / "docs" / "translations" / "translation-documents.md"
    )

    for surface in effective_surfaces:
        main_path = effective_repo_root / surface.main_relpath
        notes_path = effective_repo_root / surface.notes_relpath

        if not main_path.exists():
            failures.append(f"Missing registered translation file: {surface.main_relpath}")
            continue
        if not notes_path.exists():
            failures.append(f"Missing registered translation notes file: {surface.notes_relpath}")
            continue

        main_text = read_text(main_path)
        notes_text = read_text(notes_path)

        if surface.notes_name not in main_text:
            failures.append(
                f"{surface.main_relpath}: main translation does not link to companion notes `{surface.notes_name}`"
            )
        if surface.main_name not in notes_text:
            failures.append(
                f"{surface.notes_relpath}: companion notes do not link back to main translation `{surface.main_name}`"
            )

    expected = render_index(effective_surfaces)
    if not effective_index_path.exists():
        failures.append(
            f"Missing translation surface index: {effective_index_path.relative_to(effective_repo_root).as_posix()}"
        )
    else:
        current = read_text(effective_index_path)
        if current != expected:
            failures.append(
                f"Stale translation surface index: {effective_index_path.relative_to(effective_repo_root).as_posix()}"
            )

    return failures


def write_index(
    surfaces: tuple[TranslationSurface, ...] | None = None,
    *,
    index_path: Path | None = None,
) -> None:
    effective_surfaces = surfaces or TRANSLATION_SURFACES
    effective_index_path = index_path or INDEX_PATH
    effective_index_path.parent.mkdir(parents=True, exist_ok=True)
    effective_index_path.write_text(render_index(effective_surfaces), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-docs", action="store_true", help="Rewrite the translation surface index from the registry.")
    parser.add_argument("--check", action="store_true", help="Fail if registered translation surfaces or the index are missing or stale.")
    args = parser.parse_args()

    if args.write_docs:
        write_index()

    if args.check:
        failures = collect_surface_failures()
        if failures:
            print("Translation surface check failed:\n")
            for failure in failures:
                print(f"- {failure}")
            return 1
        print(f"Translation surface check passed for {len(TRANSLATION_SURFACES)} translation set(s).")
        return 0

    if not args.write_docs:
        print(INDEX_PATH.relative_to(REPO_ROOT).as_posix())
    return 0


if __name__ == "__main__":
    sys.exit(main())
