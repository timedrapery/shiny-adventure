#!/usr/bin/env python3
"""Report support-text sentences that break docs/support-text-standard.md.

Support text is what a reader meets around a translation: reader
introductions, "Before you read" guides, and glossary definitions. The
translations themselves are out of scope; `plain_english_audit.py` covers them.

The audit checks the rules a script can check reliably:

- sentence length: at most 20 words for a question or reading cue, at most 25
  for description and explanation (quoted text does not count)
- likely passive voice
- paragraph length: at most six sentences in an introduction paragraph, at
  most three in one guide field

It is advisory. A finding is a prompt to look again, not a verdict, and the
passive check is a heuristic. `--strict` exits 1 on any finding.

    python scripts/support_text_audit.py
    python scripts/support_text_audit.py --path includes/newcomer-guides/an2_9.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INTROS_DIR = REPO_ROOT / "includes" / "reader-intros"
GUIDES_DIR = REPO_ROOT / "includes" / "newcomer-guides"
GLOSSARY = REPO_ROOT / "includes" / "glossary.md"

INSTRUCTION_LIMIT = 20
DESCRIPTION_LIMIT = 25
INTRO_PARAGRAPH_LIMIT = 6
GUIDE_FIELD_LIMIT = 3

# Guide fields that ask the reader something or tell them what to do.
INSTRUCTION_FIELDS = {"question", "reading_cue"}
# Guide fields that are prose for the reader; the rest are keys and lists.
GUIDE_TEXT_FIELDS = ("scene", "question", "main_point", "reading_cue", "not_saying")

QUOTED = re.compile(r"“[^”]*”|\"[^\"]*\"")
# A capital may carry a Pali diacritic (Ānanda, Ñāṇa, Ṭhāna).
SENTENCE_END = re.compile(r"(?:(?<=[.!?])|(?<=[.!?][\"”’']))\s+(?=[\"“‘'(]?[A-ZĀĪŪṬḌṆÑṄṂḶṢŚ])")
PASSIVE = re.compile(
    r"\b(?:is|are|was|were|be|been|being)\s+(?:not\s+)?(?:\w+ly\s+)?"
    r"(?:\w+ed|known|seen|given|taken|done|made|said|told|born|shown|held|kept|"
    r"left|found|heard|taught|written|spoken|understood|meant|bound|led)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Finding:
    path: str
    location: str
    rule: str
    detail: str
    text: str


def split_sentences(text: str) -> list[str]:
    flat = " ".join(text.split())
    return [s.strip() for s in SENTENCE_END.split(flat) if s.strip()]


def counted_words(sentence: str) -> int:
    """Words in the sentence, not counting quoted text."""
    return len(QUOTED.sub(" ", sentence).split())


def is_passive(sentence: str) -> bool:
    return bool(PASSIVE.search(QUOTED.sub(" ", sentence)))


def check_block(path: str, location: str, text: str, limit: int, max_sentences: int) -> list[Finding]:
    findings: list[Finding] = []
    sentences = split_sentences(text)
    for sentence in sentences:
        words = counted_words(sentence)
        if words > limit:
            findings.append(Finding(path, location, "long sentence", f"{words} words (limit {limit})", sentence))
        if is_passive(sentence):
            findings.append(Finding(path, location, "passive voice", "likely passive", sentence))
    if len(sentences) > max_sentences:
        findings.append(
            Finding(path, location, "long paragraph", f"{len(sentences)} sentences (limit {max_sentences})",
                    sentences[0])
        )
    return findings


def relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+\.)\s+")


def prose_blocks(text: str) -> list[tuple[str, str]]:
    """(location, text) for each prose paragraph and list item in Markdown.

    Comments, fenced code, indented code, headings, tables, and HTML are not
    prose and are skipped. Each list item is checked on its own.
    """
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"^(```|~~~).*?^\1[^\n]*$", "", text, flags=re.S | re.M)
    blocks: list[tuple[str, str]] = []
    for number, paragraph in enumerate((p for p in re.split(r"\n\s*\n", text) if p.strip()), start=1):
        first = paragraph.lstrip()
        if first.startswith(("#", "|", "<", "    ")) or paragraph.startswith(("    ", "\t")):
            continue
        if LIST_ITEM.match(paragraph):
            items = re.split(r"\n(?=\s*(?:[-*+]|\d+\.)\s+)", paragraph)
            for index, item in enumerate(items, start=1):
                blocks.append((f"paragraph {number}, item {index}", LIST_ITEM.sub("", item, count=1)))
            continue
        blocks.append((f"paragraph {number}", re.sub(r"^>\s?", "", paragraph, flags=re.M)))
    return blocks


def audit_intro(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    for location, block in prose_blocks(path.read_text(encoding="utf-8")):
        findings += check_block(relative(path), location, block, DESCRIPTION_LIMIT, INTRO_PARAGRAPH_LIMIT)
    return findings


def audit_guide(path: Path) -> list[Finding]:
    data = json.loads(path.read_text(encoding="utf-8"))
    findings: list[Finding] = []
    for field in GUIDE_TEXT_FIELDS:
        value = data.get(field)
        if not isinstance(value, str):
            continue
        limit = INSTRUCTION_LIMIT if field in INSTRUCTION_FIELDS else DESCRIPTION_LIMIT
        findings += check_block(relative(path), field, value, limit, GUIDE_FIELD_LIMIT)
    return findings


def audit_glossary(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    for match in re.finditer(r"^\*\[([^\]]+)\]:\s*(.+)$", path.read_text(encoding="utf-8"), flags=re.M):
        term, definition = match.group(1), match.group(2)
        findings += check_block(relative(path), f"glossary: {term}", definition,
                                DESCRIPTION_LIMIT, INTRO_PARAGRAPH_LIMIT)
    return findings


def default_targets() -> list[Path]:
    return sorted(INTROS_DIR.glob("*.md")) + sorted(GUIDES_DIR.glob("*.json")) + [GLOSSARY]


def audit(paths: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    for path in paths:
        if path.suffix == ".json":
            findings += audit_guide(path)
        elif path.name == "glossary.md":
            findings += audit_glossary(path)
        else:
            findings += audit_intro(path)
    return findings


def render(findings: list[Finding], top: int) -> str:
    lines = ["Support text audit (docs/support-text-standard.md)", ""]
    if not findings:
        lines.append("No findings.")
        return "\n".join(lines)
    by_rule = Counter(f.rule for f in findings)
    lines.append("Findings by rule:")
    lines += [f"- {rule}: {count}" for rule, count in by_rule.most_common()]
    by_file = Counter(f.path for f in findings)
    lines += ["", "Files with the most findings:"]
    lines += [f"- {path}: {count}" for path, count in by_file.most_common(top)]
    lines += ["", f"First {min(top, len(findings))} findings:"]
    for finding in findings[:top]:
        lines.append(f"- {finding.path} ({finding.location}) {finding.rule}, {finding.detail}:")
        lines.append(f"    {finding.text}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--path", type=Path, action="append", help="audit only this file (repeatable)")
    parser.add_argument("--top", type=int, default=10, help="how many findings and files to list")
    parser.add_argument("--json", action="store_true", help="print findings as JSON")
    parser.add_argument("--strict", action="store_true", help="exit 1 on any finding")
    args = parser.parse_args(argv)
    findings = audit(args.path or default_targets())
    if args.json:
        print(json.dumps([asdict(f) for f in findings], indent=2, ensure_ascii=False))
    else:
        print(render(findings, args.top))
    return 1 if args.strict and findings else 0


if __name__ == "__main__":
    sys.exit(main())
