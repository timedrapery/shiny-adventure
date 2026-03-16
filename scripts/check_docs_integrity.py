#!/usr/bin/env python3
"""Validate internal Markdown links and repository-surface metadata files."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlparse


REPO_ROOT = Path(__file__).resolve().parent.parent
REQUIRED_PATHS = (
    "README.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "LICENSE",
    "CITATION.cff",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/config.yml",
)

FENCED_CODE_RE = re.compile(r"```.*?```", re.DOTALL)
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
MARKDOWN_LINK_RE = re.compile(r"(?<!!)(?:\[[^\]]+\])\(([^)]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)


def iter_markdown_files(repo_root: Path = REPO_ROOT) -> list[Path]:
    return sorted(
        path
        for path in repo_root.rglob("*.md")
        if ".git" not in path.parts and "__pycache__" not in path.parts
    )


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_ignored_regions(text: str) -> str:
    text = FENCED_CODE_RE.sub("", text)
    text = HTML_COMMENT_RE.sub("", text)
    return text


def is_external_target(target: str) -> bool:
    parsed = urlparse(target)
    return parsed.scheme in {"http", "https", "mailto", "tel"}


def split_link_target(target: str) -> tuple[str, str]:
    cleaned = target.strip()
    if cleaned.startswith("<") and cleaned.endswith(">"):
        cleaned = cleaned[1:-1].strip()
    cleaned = cleaned.split()[0]
    path_part, _, fragment = cleaned.partition("#")
    return unquote(path_part), unquote(fragment)


def extract_markdown_links(text: str) -> list[str]:
    return [match.group(1) for match in MARKDOWN_LINK_RE.finditer(strip_ignored_regions(text))]


def clean_heading_text(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", text)
    text = text.replace("`", "")
    text = re.sub(r"[*_~]", "", text)
    return text.strip()


def slugify_heading(text: str) -> str:
    text = clean_heading_text(text).casefold()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "-", text.strip())
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def collect_heading_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    counts: Counter[str] = Counter()
    for match in HEADING_RE.finditer(read_text(path)):
        base = slugify_heading(match.group(2))
        if not base:
            continue
        suffix = counts[base]
        anchor = base if suffix == 0 else f"{base}-{suffix}"
        counts[base] += 1
        anchors.add(anchor)
    return anchors


def resolve_target(source_path: Path, target_path: str, repo_root: Path) -> Path:
    if not target_path:
        return source_path
    if target_path.startswith("/"):
        return repo_root / target_path.lstrip("/")
    return (source_path.parent / target_path).resolve()


def collect_markdown_failures(repo_root: Path = REPO_ROOT) -> list[str]:
    failures: list[str] = []
    markdown_files = iter_markdown_files(repo_root)
    for source_path in markdown_files:
        text = read_text(source_path)
        for raw_target in extract_markdown_links(text):
            if is_external_target(raw_target):
                continue
            target_path_raw, fragment = split_link_target(raw_target)
            resolved = resolve_target(source_path, target_path_raw, repo_root)
            if not resolved.exists():
                failures.append(
                    f"{source_path.relative_to(repo_root)}: broken link target '{raw_target}'"
                )
                continue
            if fragment and resolved.suffix.lower() == ".md":
                anchors = collect_heading_anchors(resolved)
                if fragment not in anchors:
                    failures.append(
                        f"{source_path.relative_to(repo_root)}: missing anchor '#{fragment}' in {resolved.relative_to(repo_root)}"
                    )
    return failures


def collect_metadata_failures(repo_root: Path = REPO_ROOT) -> list[str]:
    failures: list[str] = []
    for relative_path in REQUIRED_PATHS:
        path = repo_root / relative_path
        if not path.exists():
            failures.append(f"Missing required repository file: {relative_path}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()

    failures = [
        *collect_metadata_failures(REPO_ROOT),
        *collect_markdown_failures(REPO_ROOT),
    ]
    if failures:
        print("Documentation integrity check failed:\n")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Documentation integrity check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())