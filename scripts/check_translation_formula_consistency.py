#!/usr/bin/env python3
"""Detect formula-level drift in shareable translation surfaces."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
TRANSLATIONS_DIR = REPO_ROOT / "docs" / "translations"
SKIP_FILES = {"translation-documents.md"}
TEXT_SUFFIX = ".md"

FLAGGED_PATTERNS: dict[str, re.Pattern[str]] = {
    "venerable sir": re.compile(r"\bVenerable sir\b"),
    "the buddha said colon": re.compile(r"The Buddha said:"),
    "listen attend carefully": re.compile(r"Listen, attend carefully, I will speak\."),
    "eye and forms formula": re.compile(r"Dependent on eye and forms, eye-knowing arises\."),
    "eye forms designation": re.compile(r"\beye, forms, and eye-knowing\b"),
    "no eye no forms designation": re.compile(r"\bno eye, no forms, and no eye-knowing\b"),
    "forms knowable by the eye": re.compile(r"(?<!visible )forms knowable by the eye\b"),
    "right knowing": re.compile(r"\bright knowing\b"),
    "neutral feeling": re.compile(r"\bneutral feeling\b"),
    "observing feelings in relation to feelings": re.compile(
        r"observing\s+feelings\s+in\s+relation\s+to\s+feelings"
    ),
    "one kind of feeling": re.compile(r"\bone\s+kind\s+of\s+feeling\b"),
    "tanha formula desire wording": re.compile(
        r"\bthat desire that (?:leads to renewed becoming|causes rebirth)\b",
        re.IGNORECASE,
    ),
    "tanha formula rebirth shorthand": re.compile(r"\bcauses rebirth\b"),
    "tanha formula craving collapse": re.compile(r"\baccompanied by craving\b"),
    "tanha formula pleasure collapse": re.compile(r"\baccompanied by pleasure\b"),
    "tanha formula this-and-that attachment": re.compile(r"\battached to this and that\b"),
    "tanha formula enjoying everything": re.compile(r"\benjoying everything\b"),
}

PATTERN_GUIDANCE: dict[str, str] = {
    "venerable sir": "Use `bhante` in governed dialogue-address formulas.",
    "the buddha said colon": "Use `The Buddha said this:` in stock opening formulas.",
    "listen attend carefully": "Use `Listen carefully, attend well, and I will speak.` in stock teaching-introduction formulas.",
    "eye and forms formula": "Use `Dependent on eye and visible forms, eye-knowing arises.` in eye-door sense-field formulas.",
    "eye forms designation": "Keep the eye-door designation line aligned with `visible forms`.",
    "no eye no forms designation": "Keep the negative eye-door designation line aligned with `visible forms`.",
    "forms knowable by the eye": "Use `visible forms knowable by the eye` in eye-door sequence explanation.",
    "right knowing": "Use `right knowledge` for `sammā-ñāṇa` in translation surfaces.",
    "neutral feeling": "Use `mixed feeling`, not `neutral feeling`, for the third vedanā register.",
    "observing feelings in relation to feelings": "Use `observing felt experience in relation to felt experience` in satipaṭṭhāna formulas.",
    "one kind of feeling": "Use `one kind of felt experience` in the satipaṭṭhāna fulfillment formula.",
    "tanha formula desire wording": "Use `that ignorant wanting that leads to renewed becoming` in the SN 56.11 taṇhā-definition line.",
    "tanha formula rebirth shorthand": "Keep `ponobbhavikā` in renewed-becoming language in the governed taṇhā-definition formula; do not flatten it to `causes rebirth`.",
    "tanha formula craving collapse": "Keep `nandī` and `rāga` distinct as `relishing and passion` in the governed taṇhā-definition formula.",
    "tanha formula pleasure collapse": "Keep `nandī` and `rāga` distinct as `relishing and passion` in the governed taṇhā-definition formula.",
    "tanha formula this-and-that attachment": "Use `delighting here and there` or the recorded controlled alternate, not `attached to this and that`, in the governed taṇhā-definition formula.",
    "tanha formula enjoying everything": "Use `delighting here and there` or the recorded controlled alternate in the governed taṇhā-definition formula.",
}


def iter_translation_files(translations_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in translations_dir.glob(f"*{TEXT_SUFFIX}")
        if path.is_file()
        and path.name not in SKIP_FILES
        and not path.name.endswith("-notes.md")
    )


def scan_text(text: str, relative_path: str) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    lines = text.splitlines()
    for label, pattern in FLAGGED_PATTERNS.items():
        for match in pattern.finditer(text):
            line_number = text.count("\n", 0, match.start()) + 1
            line = lines[line_number - 1].strip() if lines else ""
            findings.append(
                {
                    "path": relative_path,
                    "line": line_number,
                    "label": label,
                    "guidance": PATTERN_GUIDANCE[label],
                    "text": line,
                }
            )
    return findings


def build_report(repo_root: Path = REPO_ROOT, translations_dir: Path | None = None) -> dict[str, object]:
    target_dir = translations_dir or (repo_root / "docs" / "translations")
    files = iter_translation_files(target_dir)
    findings: list[dict[str, object]] = []
    for path in files:
        findings.extend(
            scan_text(path.read_text(encoding="utf-8"), path.relative_to(repo_root).as_posix())
        )

    label_counts: Counter[str] = Counter(str(finding["label"]) for finding in findings)
    file_counts: Counter[str] = Counter(str(finding["path"]) for finding in findings)
    return {
        "summary": {
            "files_scanned": len(files),
            "matches": len(findings),
        },
        "label_counts": dict(sorted(label_counts.items())),
        "top_files": [
            {"path": path, "matches": count}
            for path, count in file_counts.most_common(20)
        ],
        "findings": findings,
    }


def render_text(report: dict[str, object], top: int) -> str:
    lines = [
        "Translation formula consistency report",
        "",
        f"Files scanned: {report['summary']['files_scanned']}",
        f"Matches: {report['summary']['matches']}",
        "",
        "Matches by pattern:",
    ]
    for label, count in report["label_counts"].items():
        lines.append(f"- {label}: {count}")

    lines.append("")
    lines.append("Top files:")
    for entry in report["top_files"][:top]:
        lines.append(f"- {entry['path']}: {entry['matches']}")

    lines.append("")
    lines.append("Sample findings:")
    for finding in report["findings"][:top]:
        lines.append(
            f"- {finding['path']}:{finding['line']} [{finding['label']}] {finding['guidance']} -> {finding['text']}"
        )

    if not report["findings"]:
        lines.append("- No translation-surface formula drift found.")
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
    parser.add_argument(
        "--translations-dir",
        type=Path,
        default=TRANSLATIONS_DIR,
        help="directory containing shareable translation markdown files",
    )
    parser.add_argument("--top", type=int, default=10, help="Number of sample findings to show.")
    args = parser.parse_args()

    report = build_report(REPO_ROOT, args.translations_dir)
    if args.format == "json":
        write_output(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    elif report["summary"]["matches"]:
        write_output(render_text(report, max(args.top, 1)) + "\n")
    else:
        write_output("Translation formula consistency passed.\n")
    return 0 if report["summary"]["matches"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
