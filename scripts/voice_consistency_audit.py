#!/usr/bin/env python3
"""Report likely voice-template drift across the live repository surface."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SCAN_ROOTS = (
    "README.md",
    "CONTRIBUTING.md",
    "STYLE_GUIDE.md",
    "TERMINOLOGY_PRINCIPLES.md",
    "docs",
    "terms",
    "scripts",
)
DEFAULT_SKIP_PATHS = {
    "docs/ARCHAIC_DICTION_SWEEP.md",
    "docs/MODERN_ENGLISH_AUDIT.md",
    "docs/MODERN_ENGLISH_POLICY.md",
    "docs/VOICE_CONSISTENCY_AUDIT.md",
    "docs/VOICE_STANDARD.md",
    "scripts/voice_consistency_audit.py",
}
TEXT_SUFFIXES = {".json", ".md", ".py", ".txt"}

FLAGGED_PATTERNS: dict[str, dict[str, re.Pattern[str]]] = {
    "stock_rule_templates": {
        "project preference is": re.compile(r"Project preference is"),
        "default project rendering": re.compile(r"Default project rendering\."),
        "default rendering": re.compile(r"Default rendering\."),
        "acceptable alternate": re.compile(r"Acceptable alternate\."),
        "use sparingly fragment": re.compile(r"Use sparingly\."),
    },
    "fragmentary_example_notes": {
        "simple note fragment": re.compile(r'"notes": "Simple [^"]+\."'),
        "useful note fragment": re.compile(r'"notes": "Useful [^"]+\."'),
    },
    "filler_instructional_framing": {
        "it should be understood that": re.compile(r"\bit should be understood that\b", re.IGNORECASE),
        "it is to be noted that": re.compile(r"\bit is to be noted that\b", re.IGNORECASE),
        "one may observe": re.compile(r"\bone may observe\b", re.IGNORECASE),
        "is to be translated as": re.compile(r"\bis to be translated as\b", re.IGNORECASE),
    },
}


def should_skip_path(path: Path, repo_root: Path = REPO_ROOT, include_generated: bool = False) -> bool:
    relative = path.relative_to(repo_root).as_posix()
    if relative in DEFAULT_SKIP_PATHS:
        return True
    if ".git" in path.parts or "__pycache__" in path.parts:
        return True
    if not include_generated and relative.startswith("docs/generated/"):
        return True
    return False


def iter_candidate_files(repo_root: Path = REPO_ROOT, include_generated: bool = False) -> list[Path]:
    files: list[Path] = []
    for root_name in DEFAULT_SCAN_ROOTS:
        root = repo_root / root_name
        if not root.exists():
            continue
        if root.is_file():
            if root.suffix.lower() in TEXT_SUFFIXES and not should_skip_path(root, repo_root, include_generated):
                files.append(root)
            continue
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            if should_skip_path(path, repo_root, include_generated):
                continue
            files.append(path)
    return sorted(files)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def scan_text(text: str, relative_path: str) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for category, patterns in FLAGGED_PATTERNS.items():
            for label, pattern in patterns.items():
                if pattern.search(line):
                    findings.append(
                        {
                            "path": relative_path,
                            "line": line_number,
                            "category": category,
                            "label": label,
                            "text": line.strip(),
                        }
                    )
    return findings


def build_report(repo_root: Path = REPO_ROOT, include_generated: bool = False) -> dict[str, object]:
    findings: list[dict[str, object]] = []
    files = iter_candidate_files(repo_root, include_generated=include_generated)
    for path in files:
        findings.extend(scan_text(read_text(path), path.relative_to(repo_root).as_posix()))

    category_counts: Counter[str] = Counter()
    label_counts: Counter[str] = Counter()
    file_counts: Counter[str] = Counter()
    for finding in findings:
        category_counts[str(finding["category"])] += 1
        label_counts[str(finding["label"])] += 1
        file_counts[str(finding["path"])] += 1

    return {
        "summary": {
            "files_scanned": len(files),
            "matches": len(findings),
            "include_generated": include_generated,
        },
        "category_counts": dict(sorted(category_counts.items())),
        "label_counts": dict(sorted(label_counts.items())),
        "top_files": [
            {"path": path, "matches": count}
            for path, count in file_counts.most_common(15)
        ],
        "findings": findings,
    }


def render_text(report: dict[str, object], top: int) -> str:
    summary = report["summary"]
    category_counts = report["category_counts"]
    label_counts = report["label_counts"]
    top_files = report["top_files"]
    findings = report["findings"]

    lines = [
        "Voice consistency audit report",
        "",
        f"Files scanned: {summary['files_scanned']}",
        f"Matches: {summary['matches']}",
        f"Include generated docs: {summary['include_generated']}",
        "",
        "Matches by category:",
    ]
    for category, count in category_counts.items():
        lines.append(f"- {category}: {count}")

    lines.append("")
    lines.append("Matches by pattern:")
    for label, count in label_counts.items():
        lines.append(f"- {label}: {count}")

    lines.append("")
    lines.append("Top files:")
    for entry in top_files[:top]:
        lines.append(f"- {entry['path']}: {entry['matches']}")

    lines.append("")
    lines.append("Sample findings:")
    for finding in findings[:top]:
        lines.append(
            f"- {finding['path']}:{finding['line']} [{finding['category']}] {finding['label']} -> {finding['text']}"
        )

    if not findings:
        lines.append("- No flagged voice-template drift found in the scanned surface.")

    return "\n".join(lines)


def write_output(text: str) -> None:
    if not hasattr(sys.stdout, "buffer"):
        sys.stdout.write(text)
        return
    encoding = sys.stdout.encoding or "utf-8"
    sys.stdout.buffer.write(text.encode(encoding, errors="replace"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--include-generated", action="store_true")
    parser.add_argument("--top", type=int, default=10, help="number of top files and sample findings to show")
    args = parser.parse_args()

    report = build_report(REPO_ROOT, include_generated=args.include_generated)
    if args.format == "json":
        write_output(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    elif report["summary"]["matches"]:
        write_output(render_text(report, max(args.top, 1)) + "\n")
    else:
        write_output("Voice consistency audit passed.\n")
    return 0 if report["summary"]["matches"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

