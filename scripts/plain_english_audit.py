#!/usr/bin/env python3
"""Report likely translationese in the running English of translation surfaces.

This is the register counterpart to `check_translation_formula_consistency.py`.
That script catches formula-level lexical drift and gates the build. This one
catches spoken-English register problems and is advisory by default, because
several of its signals have legitimate exceptions and a crude gate would damage
good translations.

The standard it checks against is `docs/PLAIN_ENGLISH_STANDARD.md`.

Scope is the translated text only. Editorial Note blocks, reader "About this
text" introductions, notes files, and fenced code are apparatus rather than
translation, and are skipped.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
TRANSLATIONS_DIR = REPO_ROOT / "docs" / "translations"
# Reader pages are generated from the governed surfaces by
# scripts/generate_reader.py and cannot drift from them -- that is enforced by
# `generate_reader.py --check`. Auditing them as well would double-count every
# finding, and would also flag the reader glossary blocks, which are reader
# apparatus in their own voice rather than translated text. The canonical
# surfaces are the thing to audit.
READER_DIR = None
SKIP_FILES = {"translation-documents.md"}

# Signals are grouped so a reviewer can tell a hard register error (an artifact
# of translation that Pali does not have) from a softer preference.
# Words after `one` that mark it as a numeral or noun rather than a pronoun
# standing in for a person.
GENERIC_ONE_STOP = (
    r"(?:of|or|and|another|who|whom|whose|kind|kinds|side|thing|things|day|days"
    r"|year|years|arrow|arrows|feeling|feelings|direction|hand|in|at|on|to|for"
    r"|by|with|from|was|were|among|alone)"
)


FLAGGED_PATTERNS: dict[str, re.Pattern[str]] = {
    # Structural rather than a verb list. An explicit list of verbs was tried
    # first and missed roughly half the corpus: it caught `one recognizes` but
    # not `one discerns`, `one cultivates`, `one fades`, or `one should`. The
    # reliable signal is `one` standing as grammatical subject, which in English
    # means it is followed by a third-person-singular verb or an auxiliary.
    #
    # GENERIC_ONE_STOP carries the legitimate uses, where `one` is a numeral or
    # a noun: `one of them`, `one another`, `one kind of feeling`, `one arrow`,
    # `one in the body`. The negative lookbehind keeps `no one takes a life`,
    # which is ordinary English rather than the generic-person artifact.
    "generic one as subject": re.compile(
        rf"(?<!\bno )\bone\s+(?!{GENERIC_ONE_STOP}\b)"
        r"(?:[a-z]+(?:s|es)\b|is\b|has\b|does\b|will\b|would\b|should\b|can\b|must\b)"
    ),
    "generic one possessive": re.compile(r"\bone's\b"),
    "generic oneself": re.compile(r"\boneself\b"),
    # MULTILINE matters: surfaces are hard-wrapped, so an absolutive very often
    # lands at the start of a continuation line rather than after punctuation.
    "having-participle opener": re.compile(
        r"(?:^|[.;:\"'—]\s*)Having [a-z]+(?:ed|n)\b", re.MULTILINE
    ),
    "blessed one epithet": re.compile(r"\bthe Blessed One\b"),
    "archaic connective": re.compile(
        r"\b(?:thus|therein|thereof|whereby|whilst|amongst|herein|hence forth)\b",
        re.IGNORECASE,
    ),
    "clause person label": re.compile(
        r"(?<!\bno )\b(?:one who|he who|that which|those which)\b", re.IGNORECASE
    ),
    "contemplative abides": re.compile(r"\b(?:abides|abiding)\b", re.IGNORECASE),
    "nominalization chain": re.compile(
        r"\b\w+(?:tion|ment|ance|ence|ness|ity) of (?:the )?\w+(?:tion|ment|ance|ence|ness|ity)\b",
        re.IGNORECASE,
    ),
    "legacy doctrinal vocabulary": re.compile(
        r"\b(?:aggregates|volitional formations|fabrications|sense bases|defilements"
        r"|suchness|conditioned phenomena)\b",
        re.IGNORECASE,
    ),
}

PATTERN_GUIDANCE: dict[str, str] = {
    "generic one as subject": (
        "Pali has no generic `one`. Use `you`, `they`, `a person`, or name the "
        "type of person being described. See PLAIN_ENGLISH_STANDARD rule 1."
    ),
    "generic one possessive": (
        "Replace `one's` with `their`, `his`, or `your` to match the subject. "
        "See PLAIN_ENGLISH_STANDARD rule 1."
    ),
    "generic oneself": (
        "Replace `oneself` with `themselves`, `himself`, or `yourself` to match "
        "the subject. See PLAIN_ENGLISH_STANDARD rule 1."
    ),
    "having-participle opener": (
        "The Pali absolutive is an ordinary connector. Use two sentences or "
        "`Once he has ...`. See PLAIN_ENGLISH_STANDARD rule 2."
    ),
    "blessed one epithet": (
        "Use `the Buddha` for `bhagava`, as governed by terms/major/bhagava.json. "
        "See PLAIN_ENGLISH_STANDARD rule 3."
    ),
    "archaic connective": (
        "Drop the connective or use ordinary modern wording. See "
        "PLAIN_ENGLISH_STANDARD, words to be suspicious of."
    ),
    "clause person label": (
        "Use `someone who`, `a person who`, or `what`. See "
        "PLAIN_ENGLISH_STANDARD, words to be suspicious of."
    ),
    "contemplative abides": (
        "Use `stays`, `lives`, or `remains` unless the entry records a reason to "
        "keep contemplative diction."
    ),
    "nominalization chain": (
        "Two stacked abstract nouns usually means the sentence has not been "
        "written yet. Prefer verbs. See PLAIN_ENGLISH_STANDARD rule 6."
    ),
    "legacy doctrinal vocabulary": (
        "The lexicon already governs these away (heap not aggregate, "
        "putting-together not formations). Follow the lexicon."
    ),
}


TERMS_DIR = REPO_ROOT / "terms"

# Labels whose matches should be suppressed when the matched span is itself a
# governed rendering. A stacked-noun phrase that the lexicon has deliberately
# chosen is an editorial decision, not accidental translationese.
LEXICON_AWARE_LABELS = {
    "nominalization chain",
    "legacy doctrinal vocabulary",
    "archaic connective",
}


def load_governed_renderings(terms_dir: Path = TERMS_DIR) -> set[str]:
    """Collect every rendering the lexicon has explicitly chosen or allowed."""
    renderings: set[str] = set()
    if not terms_dir.exists():
        return renderings
    for path in terms_dir.rglob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if not isinstance(data, dict):
            continue
        for field in ("preferred_translation", "alternative_translations"):
            value = data.get(field)
            if isinstance(value, str):
                renderings.add(value.casefold())
            elif isinstance(value, list):
                renderings.update(v.casefold() for v in value if isinstance(v, str))
        for rule in data.get("context_rules") or []:
            if isinstance(rule, dict) and isinstance(rule.get("rendering"), str):
                renderings.add(rule["rendering"].casefold())
    return renderings


def is_governed(span: str, renderings: set[str], window: str = "") -> bool:
    """True when this span is part of a rendering the lexicon already chose.

    When a window of surrounding text is supplied, the governed rendering must
    actually appear in that window. That matters for short spans: the token
    `thus` is a substring of the governed rendering `'thus it was said' texts`,
    so a bare containment test would suppress every `thus` in the corpus. The
    window makes suppression apply only where the governed phrase is really
    present.
    """
    needle = span.casefold().strip()
    if not needle:
        return False
    if not window:
        return any(needle in rendering or rendering in needle for rendering in renderings)
    haystack = re.sub(r"\s+", " ", window).casefold()
    return any(
        needle in rendering and rendering in haystack for rendering in renderings
    )


def is_compositional(span: str, renderings: set[str]) -> bool:
    """True when an `X of Y` phrase is built entirely from governed renderings.

    The repository's doctrinal vocabulary legitimately stacks nouns:
    `recognition of impermanence` is `sanna` plus `anicca`, both governed, and
    `cessation of dissatisfaction` is a recorded four-noble-truths context rule
    for `nirodha` plus the governed `dukkha`. Those are editorial decisions, not
    accidental nominalization, so they should not be reported.
    """
    parts = [p.strip() for p in re.split(r"\bof\b", span.casefold()) if p.strip()]
    if len(parts) < 2:
        return False
    cleaned = [re.sub(r"^(?:the|a|an)\s+", "", p) for p in parts]
    return all(part in renderings for part in cleaned)


def strip_apparatus(text: str) -> str:
    """Blank out everything that is apparatus rather than translated text.

    Lines are replaced with empty strings rather than removed so that reported
    line numbers still match the file on disk.
    """
    lines = text.splitlines()
    out: list[str] = []
    in_fence = False
    in_apparatus = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("```"):
            in_fence = not in_fence
            out.append("")
            continue

        if stripped.startswith("#"):
            heading = stripped.lstrip("#").strip().casefold()
            # Apparatus sections; everything until the next heading is skipped.
            in_apparatus = heading in {
                "editorial note",
                "about this text",
                "translation notes",
                "source",
                "source basis",
            }
            out.append("")
            continue

        out.append("" if (in_fence or in_apparatus) else line)

    return "\n".join(out)


def iter_target_files(
    translations_dir: Path = TRANSLATIONS_DIR,
    reader_dir: Path | None = READER_DIR,
) -> list[Path]:
    files: list[Path] = []
    for directory in (translations_dir, reader_dir):
        if directory is None or not directory.exists():
            continue
        files.extend(
            path
            for path in directory.glob("*.md")
            if path.is_file()
            and path.name not in SKIP_FILES
            and not path.name.endswith("-notes.md")
        )
    return sorted(files)


def scan_text(
    text: str,
    relative_path: str,
    governed: set[str] | None = None,
) -> list[dict[str, object]]:
    body = strip_apparatus(text)
    lines = body.splitlines()
    governed = governed or set()
    findings: list[dict[str, object]] = []
    for label, pattern in FLAGGED_PATTERNS.items():
        for match in pattern.finditer(body):
            if label in LEXICON_AWARE_LABELS:
                window = body[max(0, match.start() - 80): match.end() + 80]
                if is_governed(match.group(0), governed, window):
                    continue
                if label == "nominalization chain" and is_compositional(
                    match.group(0), governed
                ):
                    continue
            line_number = body.count("\n", 0, match.start()) + 1
            line = lines[line_number - 1].strip() if line_number <= len(lines) else ""
            findings.append(
                {
                    "path": relative_path,
                    "line": line_number,
                    "label": label,
                    "match": match.group(0).strip(),
                    "guidance": PATTERN_GUIDANCE[label],
                    "text": line,
                }
            )
    return findings


def build_report(
    repo_root: Path = REPO_ROOT,
    translations_dir: Path | None = None,
    reader_dir: Path | None = None,
    paths: list[Path] | None = None,
) -> dict[str, object]:
    if paths:
        files = sorted(p for p in paths if p.is_file())
    else:
        files = iter_target_files(translations_dir or TRANSLATIONS_DIR, reader_dir)

    governed = load_governed_renderings(repo_root / "terms")
    findings: list[dict[str, object]] = []
    for path in files:
        try:
            relative = path.relative_to(repo_root).as_posix()
        except ValueError:
            relative = path.as_posix()
        findings.extend(scan_text(path.read_text(encoding="utf-8"), relative, governed))

    label_counts: Counter[str] = Counter(str(f["label"]) for f in findings)
    file_counts: Counter[str] = Counter(str(f["path"]) for f in findings)
    return {
        "summary": {"files_scanned": len(files), "matches": len(findings)},
        "label_counts": dict(sorted(label_counts.items())),
        "top_files": [
            {"path": path, "matches": count} for path, count in file_counts.most_common(20)
        ],
        "findings": findings,
    }


def render_text(report: dict[str, object], top: int) -> str:
    summary = report["summary"]
    lines = [
        "Plain English audit",
        "",
        f"Files scanned: {summary['files_scanned']}",
        f"Register signals: {summary['matches']}",
    ]

    if not report["findings"]:
        lines.append("")
        lines.append("- No register signals found.")
        return "\n".join(lines)

    lines.extend(["", "Signals by pattern:"])
    for label, count in report["label_counts"].items():
        lines.append(f"- {label}: {count}")

    lines.extend(["", "Top files:"])
    for entry in report["top_files"][:top]:
        lines.append(f"- {entry['path']}: {entry['matches']}")

    lines.extend(["", "Sample findings:"])
    for finding in report["findings"][:top]:
        lines.append(f"- {finding['path']}:{finding['line']} [{finding['label']}] {finding['match']}")
        lines.append(f"    {finding['guidance']}")

    lines.extend(
        [
            "",
            "This audit is advisory. A flagged line is a prompt to reread the",
            "sentence aloud, not proof that it must change. See",
            "docs/PLAIN_ENGLISH_STANDARD.md.",
        ]
    )
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
    parser.add_argument("--top", type=int, default=15, help="Number of sample findings to show.")
    parser.add_argument(
        "--path",
        type=Path,
        action="append",
        help="Scan only these files. Repeatable. Useful while revising one surface.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero when any register signal is found.",
    )
    args = parser.parse_args()

    report = build_report(REPO_ROOT, paths=args.path)
    if args.format == "json":
        write_output(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    else:
        write_output(render_text(report, max(args.top, 1)) + "\n")

    if args.strict and report["summary"]["matches"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
