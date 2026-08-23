#!/usr/bin/env python3
"""Validate neutral readability review metadata for translation surfaces."""

from __future__ import annotations

import hashlib
import re
import sys
from datetime import date
from pathlib import Path

try:
    from scripts.surface_registry import TRANSLATION_SURFACES, TranslationSurface
except ModuleNotFoundError:
    from surface_registry import TRANSLATION_SURFACES, TranslationSurface


REPO_ROOT = Path(__file__).resolve().parent.parent
STANDARD = "plain-english-v1"
BODY_MARKER = "## Translation"
REVIEW_HEADING = "## Readability Review"

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
REVIEW_STATUSES = {"provisional", "validated"}


def is_iso_date(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def normalized_translation_body(text: str) -> str:
    if BODY_MARKER not in text:
        raise ValueError(f"surface has no `{BODY_MARKER}` section")
    body = text.split(BODY_MARKER, 1)[1]
    return body.replace("\r\n", "\n").replace("\r", "\n").strip() + "\n"


def translation_body_sha256(path: Path) -> str:
    body = normalized_translation_body(path.read_text(encoding="utf-8"))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def review_failures(
    surfaces: tuple[TranslationSurface, ...],
    repo_root: Path,
) -> list[str]:
    failures: list[str] = []
    for surface in surfaces:
        review = surface.readability_review
        if review is None:
            failures.append(f"{surface.label}: missing readability_review")
            continue

        prefix = surface.label
        if review.standard != STANDARD:
            failures.append(f"{prefix}: readability standard must be `{STANDARD}`")
        if review.status not in REVIEW_STATUSES:
            failures.append(
                f"{prefix}: unknown readability review status `{review.status}`"
            )
        if not is_iso_date(review.reviewed_on):
            failures.append(f"{prefix}: reviewed_on must be an ISO date")

        main_path = repo_root / surface.main_relpath
        notes_path = repo_root / surface.notes_relpath
        if not main_path.is_file():
            failures.append(f"{prefix}: translation surface is missing")
            continue
        if not SHA256_RE.fullmatch(review.body_sha256):
            failures.append(f"{prefix}: body_sha256 must be lowercase SHA-256")
        else:
            actual_hash = translation_body_sha256(main_path)
            if actual_hash != review.body_sha256:
                failures.append(
                    f"{prefix}: reviewed body hash is stale; expected {actual_hash}"
                )

        if not notes_path.is_file():
            failures.append(f"{prefix}: companion notes are missing")
            continue
        notes = notes_path.read_text(encoding="utf-8")
        if REVIEW_HEADING not in notes:
            failures.append(f"{prefix}: notes need `{REVIEW_HEADING}`")
        if f"- Standard: `{review.standard}`" not in notes:
            failures.append(f"{prefix}: notes do not record the readability standard")
        if f"- Status: `{review.status}`" not in notes:
            failures.append(f"{prefix}: notes do not record the readability status")

        if review.status == "validated":
            required_completions = (
                "source-fidelity review: complete",
                "human read-aloud usability review: complete",
                "newcomer comprehension review: complete",
            )
            folded_notes = notes.casefold()
            for requirement in required_completions:
                if requirement not in folded_notes:
                    failures.append(
                        f"{prefix}: validated status needs `{requirement}`"
                    )
    return failures


def collect_failures(
    repo_root: Path = REPO_ROOT,
    surfaces: tuple[TranslationSurface, ...] = TRANSLATION_SURFACES,
) -> list[str]:
    return review_failures(surfaces, repo_root)


def main() -> int:
    failures = collect_failures()
    if failures:
        print("Readability review check failed:\n")
        for failure in failures:
            print(f"- {failure}")
        return 1
    reviewed = sum(
        1 for surface in TRANSLATION_SURFACES if surface.readability_review is not None
    )
    print(f"Readability review check passed ({reviewed} reviewed surface(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
