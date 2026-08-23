#!/usr/bin/env python3
"""Validate the reader's source-level accessibility contract.

This check deliberately inspects the Markdown/HTML planned by the reader
generator.  It is fast, needs no MkDocs installation, and catches structural
regressions before stale generated files are written or deployed.
"""

from __future__ import annotations

import json
import re
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

try:
    from scripts import generate_reader
    from scripts.surface_registry import ESSENTIAL_FIVE, TRANSLATION_SURFACES
except ModuleNotFoundError:  # invoked as a script from the repository root
    import generate_reader  # type: ignore[no-redef]
    from surface_registry import (  # type: ignore[no-redef]
        ESSENTIAL_FIVE,
        TRANSLATION_SURFACES,
    )


REPO_ROOT = Path(__file__).resolve().parent.parent
GUIDES_DIR = REPO_ROOT / "includes" / "newcomer-guides"

H1_RE = re.compile(r"^#(?!#)\s+\S", re.MULTILINE)
H2_RE = re.compile(r"^##(?!#)\s+(.+?)\s*$", re.MULTILINE)
H3_RE = re.compile(r"^###(?!#)\s+\S", re.MULTILINE)
READING_META_RE = re.compile(
    r"^(?=[^\n]*\b\d[\d,]*\s+words?\b)"
    r"(?=[^\n]*\b(?:about\s+)?\d+\s+min(?:ute)?s?\b)[^\n]+$",
    re.IGNORECASE | re.MULTILINE,
)
SKIP_LINK_RE = re.compile(
    r"(?:\[[^\]]+\]\(\s*#translation\s*\)|"
    r"<a\b[^>]*\bhref=[\"']#translation[\"'][^>]*>)",
    re.IGNORECASE,
)
MARKDOWN_TABLE_DIVIDER_RE = re.compile(
    r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$",
    re.MULTILINE,
)
RAW_HTML_MARKDOWN_LINK_RE = re.compile(
    r"<a\b[^>]*\bhref\s*=\s*[\"'][^\"']+\.md(?:#[^\"']*)?[\"']",
    re.IGNORECASE,
)

GUIDE_SECTIONS = {
    "scene": "What happens",
    "question": "Central question",
    "main_point": "Main point",
    "reading_cue": "Reading tip",
}


def _relative(path: Path, repo_root: Path = REPO_ROOT) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def _opening_tag_with_classes(text: str, tag: str, *classes: str) -> re.Match[str] | None:
    """Return an opening tag whose class attribute contains every token."""
    for match in re.finditer(rf"<{tag}\b[^>]*>", text, re.IGNORECASE | re.DOTALL):
        class_match = re.search(
            r"\bclass\s*=\s*[\"']([^\"']*)[\"']",
            match.group(0),
            re.IGNORECASE,
        )
        if class_match is None:
            continue
        tokens = class_match.group(1).casefold().split()
        if all(name.casefold() in tokens for name in classes):
            return match
    return None


def _nav_has_reading_order_label(text: str) -> bool:
    for match in re.finditer(r"<nav\b[^>]*>", text, re.IGNORECASE | re.DOTALL):
        tag = match.group(0)
        class_match = re.search(
            r"\bclass\s*=\s*[\"']([^\"']*)[\"']", tag, re.IGNORECASE
        )
        label_match = re.search(
            r"\baria-label\s*=\s*[\"']([^\"']*)[\"']", tag, re.IGNORECASE
        )
        if class_match is None or label_match is None:
            continue
        classes = class_match.group(1).casefold().split()
        if (
            "reading-order" in classes
            and label_match.group(1).strip().casefold() == "reading order"
        ):
            return True
    return False


def _section(text: str, heading: str) -> str | None:
    """Return one H2 section's body, stopping before the next H2."""
    matches = list(H2_RE.finditer(text))
    for index, match in enumerate(matches):
        if match.group(1).strip().casefold() != heading.casefold():
            continue
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        return text[match.end():end]
    return None


def load_guides(
    repo_root: Path = REPO_ROOT,
    essential_five: tuple[str, ...] = ESSENTIAL_FIVE,
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    """Load and minimally validate the Essential Five newcomer guides."""
    guides: dict[str, dict[str, Any]] = {}
    failures: list[str] = []
    guide_dir = repo_root / "includes" / "newcomer-guides"

    for key in essential_five:
        path = guide_dir / f"{key}.json"
        relative = _relative(path, repo_root)
        if not path.is_file():
            failures.append(f"{relative}: missing newcomer guide for `{key}`")
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            failures.append(f"{relative}: invalid JSON ({error})")
            continue
        if not isinstance(data, dict):
            failures.append(f"{relative}: guide must be a JSON object")
            continue

        if data.get("surface_key") != key:
            failures.append(f"{relative}: surface_key must be `{key}`")
        for field in GUIDE_SECTIONS:
            value = data.get(field)
            if not isinstance(value, str) or not value.strip():
                failures.append(f"{relative}: `{field}` must be a non-empty string")

        key_terms = data.get("key_terms")
        if (
            not isinstance(key_terms, list)
            or not key_terms
            or any(not isinstance(term, str) or not term.strip() for term in key_terms)
        ):
            failures.append(
                f"{relative}: `key_terms` must be a non-empty list of strings"
            )
        guides[key] = data

    return guides, failures


def sutta_page_failures(
    text: str,
    label: str,
    guide: Mapping[str, Any] | None = None,
) -> list[str]:
    """Validate one rendered sutta page and return actionable failures."""
    failures: list[str] = []

    h1_count = len(H1_RE.findall(text))
    if h1_count != 1:
        failures.append(f"{label}: expected exactly one H1; found {h1_count}")

    before_match = re.search(
        r"^##(?!#)\s+Before you read\s*$", text, re.IGNORECASE | re.MULTILINE
    )
    translation_matches = list(
        re.finditer(
            r"^##(?!#)\s+Translation\s*$", text, re.IGNORECASE | re.MULTILINE
        )
    )
    if before_match is None:
        failures.append(f"{label}: missing H2 `Before you read`")
    if len(translation_matches) != 1:
        failures.append(
            f"{label}: expected exactly one H2 `Translation`; "
            f"found {len(translation_matches)}"
        )

    pre_translation = (
        text[:translation_matches[0].start()] if translation_matches else text
    )
    if READING_META_RE.search(pre_translation) is None:
        failures.append(
            f"{label}: reading metadata must put a word count and minutes "
            "on the same line before the translation"
        )
    if SKIP_LINK_RE.search(pre_translation) is None:
        failures.append(f"{label}: missing skip link to `#translation`")

    translation = _section(text, "Translation")
    if translation is not None and H3_RE.search(translation) is None:
        failures.append(f"{label}: `Translation` must contain at least one H3")

    details_match = _opening_tag_with_classes(text, "details", "reader-terms")
    if details_match is None:
        failures.append(f"{label}: missing visible `details.reader-terms` glossary")
    else:
        close = re.search(r"</details\s*>", text[details_match.end():], re.IGNORECASE)
        details_body = (
            text[details_match.end():details_match.end() + close.start()]
            if close is not None
            else text[details_match.end():]
        )
        if close is None:
            failures.append(f"{label}: `details.reader-terms` is not closed")
        if re.search(
            r"<summary\b[^>]*>\s*\S.*?</summary\s*>",
            details_body,
            re.IGNORECASE | re.DOTALL,
        ) is None:
            failures.append(
                f"{label}: `details.reader-terms` needs a non-empty summary"
            )

    if not _nav_has_reading_order_label(text):
        failures.append(
            f'{label}: missing `nav.reading-order` with aria-label="Reading order"'
        )

    # MkDocs rewrites Markdown links, but not href values authored inside raw
    # HTML. A raw .md href therefore becomes a broken nested URL after build.
    if RAW_HTML_MARKDOWN_LINK_RE.search(text):
        failures.append(
            f"{label}: raw HTML links must not point to source `.md` files"
        )

    if guide is not None:
        before = _section(text, "Before you read")
        if before is None:
            return failures
        for field, heading in GUIDE_SECTIONS.items():
            if re.search(
                rf"^###(?!#)\s+{re.escape(heading)}\s*$",
                before,
                re.IGNORECASE | re.MULTILINE,
            ) is None:
                failures.append(f"{label}: newcomer guide is missing `{heading}`")
            value = guide.get(field)
            if isinstance(value, str) and value.strip():
                if value.strip().casefold() not in before.casefold():
                    failures.append(
                        f"{label}: newcomer guide does not show `{field}` content"
                    )

        terms = guide.get("key_terms")
        if isinstance(terms, list):
            for term in terms:
                if isinstance(term, str) and term.strip():
                    if term.strip().casefold() not in before.casefold():
                        failures.append(
                            f"{label}: newcomer guide does not show key term "
                            f"`{term.strip()}`"
                        )

    return failures


def markdown_table_failures(text: str, label: str) -> list[str]:
    if MARKDOWN_TABLE_DIVIDER_RE.search(text):
        return [f"{label}: Markdown tables are not allowed in this reader index"]
    return []


def accessibility_asset_failures(
    mkdocs_text: str,
    css_text: str,
    css_exists: bool = True,
) -> list[str]:
    """Check the small set of site-wide accessibility assets we depend on."""
    failures: list[str] = []
    if not css_exists:
        failures.append("reader-src/stylesheets/reader.css: missing")
    if "stylesheets/reader.css" not in mkdocs_text:
        failures.append("mkdocs.yml: reader stylesheet is not registered")
    if not re.search(r"^\s*font:\s*false\s*$", mkdocs_text, re.MULTILINE):
        failures.append("mkdocs.yml: external theme fonts must remain disabled")
    if "navigation.instant" in mkdocs_text:
        failures.append("mkdocs.yml: instant navigation conflicts with simple page loading")
    required_css = {
        ":focus-visible": "visible keyboard focus",
        "min-height: 44px": "touch target sizing",
        "prefers-reduced-motion": "reduced-motion support",
        "max-width: 70ch": "readable line length",
        "summary::before": "a visible disclosure indicator",
    }
    for token, purpose in required_css.items():
        if token not in css_text:
            failures.append(f"reader.css: missing {purpose} ({token})")
    return failures


def planned_reader_files() -> Mapping[Path, str]:
    """Return generator output while tolerating the established API name."""
    planner = getattr(generate_reader, "planned_pages", None)
    if planner is None:
        planner = generate_reader.planned_files
    return planner()


def collect_failures(
    repo_root: Path = REPO_ROOT,
    pages: Mapping[Path, str] | None = None,
) -> list[str]:
    """Validate all registered reader pages plus the two flowing indexes."""
    failures: list[str] = []
    planned = pages if pages is not None else planned_reader_files()
    guides, guide_failures = load_guides(repo_root)
    failures.extend(guide_failures)

    mkdocs_path = repo_root / "mkdocs.yml"
    css_path = repo_root / "reader-src" / "stylesheets" / "reader.css"
    mkdocs_text = (
        mkdocs_path.read_text(encoding="utf-8") if mkdocs_path.is_file() else ""
    )
    css_exists = css_path.is_file()
    css_text = css_path.read_text(encoding="utf-8") if css_exists else ""
    failures.extend(accessibility_asset_failures(mkdocs_text, css_text, css_exists))

    by_key = {surface.key: surface for surface in TRANSLATION_SURFACES}
    for key in ESSENTIAL_FIVE:
        if key not in by_key:
            failures.append(f"Essential Five key `{key}` is not a registered surface")

    sutta_dir = repo_root / "reader-src" / "suttas"
    for surface in TRANSLATION_SURFACES:
        path = sutta_dir / surface.main_name
        relative = _relative(path, repo_root)
        text = planned.get(path)
        if text is None:
            failures.append(f"{relative}: missing from planned reader output")
            continue
        failures.extend(sutta_page_failures(text, relative, guides.get(surface.key)))

    index_paths = (
        sutta_dir / "index.md",
        repo_root / "reader-src" / "glossary.md",
    )
    for path in index_paths:
        relative = _relative(path, repo_root)
        text = planned.get(path)
        if text is None:
            failures.append(f"{relative}: missing from planned reader output")
            continue
        failures.extend(markdown_table_failures(text, relative))

    return failures


def main() -> int:
    failures = collect_failures()
    if failures:
        print("Reader accessibility check failed:\n")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "Reader accessibility check passed "
        f"({len(TRANSLATION_SURFACES)} sutta pages)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
