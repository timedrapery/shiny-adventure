#!/usr/bin/env python3
"""Report likely translationese in the running English of translation surfaces.

This is the register counterpart to `check_translation_formula_consistency.py`.
That script catches formula-level lexical drift and gates the build. This one
catches plain-English readability problems and is advisory by default, because
several of its signals have legitimate exceptions and a crude gate would damage
good translations.

The standard it checks against is `docs/PLAIN_ENGLISH_STANDARD.md`.

Scope is the translated text only. Editorial Note blocks, reader "About this
text" introductions, notes files, and fenced code are apparatus rather than
translation, and are skipped.

The script reports two different kinds of thing.

`findings` are point signals: a specific span on a specific line that reads as
translationese. They are what `--strict` gates on.

The `spoken register profile` is distributional. It does not claim any line is
wrong; it measures four properties of the running English that only matter when
the text is said out loud, and that no per-line regex can see:

- how often dialogue leaves a negation uncontracted where a speaker would
  contract it
- where vocatives sit in the sentence
- the longest stretch a reader must get through on one breath
- which repeated units carry the most weight, so the unit that a reader hears
  twenty times gets edited first

These are read-aloud pressures, reported so a reviewer can aim a read-aloud
pass. See `docs/PLAIN_ENGLISH_STANDARD.md`, the read-aloud test and rule 4.
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
        rf"(?<!\b[Nn]o )\bone\s+(?!{GENERIC_ONE_STOP}\b)"
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


# ---------------------------------------------------------------------------
# Spoken register profile
#
# Everything below measures the running English as speech rather than as text.
# It is deliberately kept out of `findings`: these are distributional pressures
# with legitimate exceptions on any given line, so gating on them would be
# exactly the crude gate this script's docstring warns against.
# ---------------------------------------------------------------------------

# Negations an English speaker normally contracts when talking. Emphatic and
# formal negation is real ("I do not say that a person is reborn"), so this is
# reported as a rate rather than as a per-line error.
CONTRACTIBLE_NEGATION = re.compile(
    r"\b(?:do|does|did|is|are|was|were|will|would|should|could|have|has|had)\s+not\b"
    r"|\bcannot\b",
    re.IGNORECASE,
)

SPOKEN_CONTRACTION = re.compile(r"\b\w+n't\b", re.IGNORECASE)

# The corpus's forms of address. Restricted to the governed address terms
# rather than any capitalised name, because a comma-flanked name is far more
# often an ordinary appositive than a vocative.
VOCATIVES = (
    "bhikkhus",
    "bhikkhu",
    "bhante",
    "ayye",
    "friends",
    "friend",
)
_VOC = r"(?:%s)" % "|".join(VOCATIVES)

# A vocative opening the sentence or the quoted speech: `"Bhikkhus, ...`.
VOCATIVE_INITIAL = re.compile(
    rf'(?:^|(?<=[.?!])\s|(?<=")|(?<=“))\s*{_VOC},', re.IGNORECASE | re.MULTILINE
)
# A vocative closing the sentence: `..., bhikkhus.`
VOCATIVE_FINAL = re.compile(rf',\s*{_VOC}\s*(?=[.?!]|"|”|$)', re.IGNORECASE | re.MULTILINE)
# A vocative wedged inside the clause: `And what, bhikkhus, is right view?`
VOCATIVE_MEDIAL = re.compile(rf'\w\s*,\s*{_VOC}\s*,\s*\w', re.IGNORECASE)

# A reader has to get from one full stop to the next without a landing point.
# 45 words is roughly twice the corpus median sentence and well past what most
# people can deliver on one breath.
BREATH_LIMIT = 45

# A repeated unit shorter than this is a refrain, not a sentence under strain.
REPEAT_MIN_WORDS = 6
REPEAT_MIN_COUNT = 3


LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+\.)\s+")


def split_paragraphs(body: str) -> list[tuple[int, str]]:
    """Split stripped body text into (start line number, paragraph) pairs.

    Surfaces are hard-wrapped, so a paragraph is a run of non-blank lines. The
    line number is carried so a reported paragraph can be found in the file.

    A list item starts its own block even without a blank line before it. A
    reader delivers a bulleted list one item at a time, so gluing the items
    together would invent breath spans that nobody has to say in one go -- the
    enumerated lists in DN 2 and MN 118 are the corpus's longest by far, and
    every one of them is read item by item.
    """
    paragraphs: list[tuple[int, str]] = []
    current: list[str] = []
    start = 0

    def flush() -> None:
        nonlocal current
        if current:
            paragraphs.append((start, " ".join(current)))
            current = []

    for index, line in enumerate(body.splitlines(), start=1):
        if not line.strip():
            flush()
            continue
        if LIST_ITEM.match(line):
            flush()
            start = index
            current.append(LIST_ITEM.sub("", line.strip()))
            continue
        if not current:
            start = index
        current.append(line.strip())
    flush()
    return paragraphs


def iter_speech_paragraphs(body: str) -> list[tuple[int, str]]:
    """Return the paragraphs that are somebody speaking.

    The corpus convention is that a speech opens with a double quote and runs
    across paragraphs until a paragraph ends on the closing quote; continuation
    paragraphs are not re-opened. A paragraph-local test would therefore miss
    most of the dialogue, so this tracks the open speech across the surface.

    It is deliberately conservative: unbalanced quotes close the block rather
    than swallowing the rest of the file.
    """
    speech: list[tuple[int, str]] = []
    inside = False
    for line_number, paragraph in split_paragraphs(body):
        opens = paragraph.startswith('"') or paragraph.startswith("“")
        if opens:
            inside = True
        if inside:
            speech.append((line_number, paragraph))
        if inside and re.search(r'["”][.,!?]?\s*$', paragraph):
            inside = False
    return speech


def split_sentences(paragraph: str) -> list[str]:
    """Split a paragraph into sentences on terminal punctuation.

    Splitting is paragraph-local on purpose. Joining paragraphs first makes a
    question-and-answer exchange look like one enormous sentence, which is an
    artifact of the measurement rather than a property of the text.
    """
    parts = re.split(r"(?<=[.?!])[\"”\']*\s+", paragraph)
    return [part.strip() for part in parts if part.strip()]


def normalize_unit(sentence: str) -> str:
    """Reduce a sentence to a comparison key for repeat counting."""
    lowered = sentence.casefold()
    lowered = re.sub(r"[\"“”\'‘’]", "", lowered)
    lowered = re.sub(r"[^\w\s]", " ", lowered)
    return re.sub(r"\s+", " ", lowered).strip()


def word_count(text: str) -> int:
    return len(text.split())


def profile_text(text: str, relative_path: str) -> dict[str, object]:
    """Measure the read-aloud properties of one surface."""
    body = strip_apparatus(text)
    paragraphs = split_paragraphs(body)
    speech = iter_speech_paragraphs(body)
    speech_text = " ".join(paragraph for _, paragraph in speech)

    contractible = len(CONTRACTIBLE_NEGATION.findall(speech_text))
    contracted = len(SPOKEN_CONTRACTION.findall(speech_text))

    vocatives = {
        "initial": len(VOCATIVE_INITIAL.findall(speech_text)),
        "medial": len(VOCATIVE_MEDIAL.findall(speech_text)),
        "final": len(VOCATIVE_FINAL.findall(speech_text)),
    }

    long_units: list[dict[str, object]] = []
    sentence_lengths: list[int] = []
    for line_number, paragraph in paragraphs:
        for sentence in split_sentences(paragraph):
            length = word_count(sentence)
            sentence_lengths.append(length)
            if length > BREATH_LIMIT:
                long_units.append(
                    {
                        "line": line_number,
                        "words": length,
                        "opening": " ".join(sentence.split()[:12]),
                    }
                )
    long_units.sort(key=lambda unit: int(unit["words"]), reverse=True)

    repeats: Counter[str] = Counter()
    examples: dict[str, str] = {}
    for _, paragraph in paragraphs:
        for sentence in split_sentences(paragraph):
            key = normalize_unit(sentence)
            if word_count(key) < REPEAT_MIN_WORDS:
                continue
            repeats[key] += 1
            examples.setdefault(key, sentence)

    repeated_units = [
        {
            "occurrences": count,
            "words": word_count(key),
            # What it costs a reader to leave this unit unpolished: every
            # repeat after the first is a re-hearing of the same sentence.
            "weight": word_count(key) * (count - 1),
            "text": examples[key],
        }
        for key, count in repeats.items()
        if count >= REPEAT_MIN_COUNT
    ]
    repeated_units.sort(key=lambda unit: int(unit["weight"]), reverse=True)

    return {
        "path": relative_path,
        "words": sum(sentence_lengths),
        "speech_words": word_count(speech_text),
        "dialogue": {
            "contractible_negations": contractible,
            "contractions": contracted,
        },
        "vocatives": vocatives,
        "longest_unit": int(long_units[0]["words"]) if long_units else 0,
        "over_breath_limit": len(long_units),
        "long_units": long_units[:5],
        "repeated_units": repeated_units[:5],
        # Every unit, not just the locally repeated ones: a formula said once
        # per sutta across eight suttas repeats for the reader even though no
        # single surface repeats it. Underscored because this is the whole
        # corpus keyed twice over -- it feeds aggregate_profiles and is dropped
        # before the report is returned, so it never reaches --format json.
        "_unit_counts": dict(repeats),
        "_unit_examples": examples,
    }


def aggregate_profiles(profiles: list[dict[str, object]]) -> dict[str, object]:
    """Roll per-surface profiles up into corpus-level pressures."""
    words = sum(int(p["words"]) for p in profiles)
    speech_words = sum(int(p["speech_words"]) for p in profiles)
    contractible = sum(int(p["dialogue"]["contractible_negations"]) for p in profiles)
    contracted = sum(int(p["dialogue"]["contractions"]) for p in profiles)
    vocatives = {
        position: sum(int(p["vocatives"][position]) for p in profiles)
        for position in ("initial", "medial", "final")
    }
    vocative_total = sum(vocatives.values())

    long_units = [
        dict(unit, path=p["path"]) for p in profiles for unit in p["long_units"]
    ]
    long_units.sort(key=lambda unit: int(unit["words"]), reverse=True)

    repeated_units = [
        dict(unit, path=p["path"]) for p in profiles for unit in p["repeated_units"]
    ]
    repeated_units.sort(key=lambda unit: int(unit["weight"]), reverse=True)

    # A unit that appears across several surfaces is the highest-leverage thing
    # in the corpus to get right: one edit improves every text that carries it,
    # and one awkward phrasing is heard in all of them.
    corpus_counts: Counter[str] = Counter()
    corpus_surfaces: dict[str, set[str]] = {}
    corpus_examples: dict[str, str] = {}
    for profile in profiles:
        for key, count in profile["_unit_counts"].items():
            corpus_counts[key] += count
            corpus_surfaces.setdefault(key, set()).add(str(profile["path"]))
            corpus_examples.setdefault(key, profile["_unit_examples"][key])

    shared_units = [
        {
            "surfaces": len(corpus_surfaces[key]),
            "occurrences": count,
            "words": word_count(key),
            "weight": word_count(key) * (count - 1),
            "text": corpus_examples[key],
        }
        for key, count in corpus_counts.items()
        if len(corpus_surfaces[key]) >= 2 and count >= REPEAT_MIN_COUNT
    ]
    shared_units.sort(key=lambda unit: int(unit["weight"]), reverse=True)

    return {
        "words": words,
        "speech_words": speech_words,
        "dialogue": {
            "contractible_negations": contractible,
            "contractions": contracted,
            "contraction_rate": (
                round(contracted / (contracted + contractible), 3)
                if (contracted + contractible)
                else None
            ),
        },
        "vocatives": dict(
            vocatives,
            medial_share=(
                round(vocatives["medial"] / vocative_total, 3) if vocative_total else None
            ),
        ),
        "over_breath_limit": sum(int(p["over_breath_limit"]) for p in profiles),
        "breath_limit": BREATH_LIMIT,
        "longest_units": long_units[:20],
        "repeated_units": repeated_units[:20],
        "shared_units": shared_units[:20],
    }


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
    profiles: list[dict[str, object]] = []
    for path in files:
        try:
            relative = path.relative_to(repo_root).as_posix()
        except ValueError:
            relative = path.as_posix()
        text = path.read_text(encoding="utf-8")
        findings.extend(scan_text(text, relative, governed))
        profiles.append(profile_text(text, relative))

    spoken_register = aggregate_profiles(profiles)
    # The per-unit tables exist only to build the cross-surface rollup above.
    # Left in place they would put every sentence of the corpus, keyed twice,
    # into `--format json`.
    for profile in profiles:
        profile.pop("_unit_counts", None)
        profile.pop("_unit_examples", None)

    label_counts: Counter[str] = Counter(str(f["label"]) for f in findings)
    file_counts: Counter[str] = Counter(str(f["path"]) for f in findings)
    return {
        "summary": {"files_scanned": len(files), "matches": len(findings)},
        "label_counts": dict(sorted(label_counts.items())),
        "top_files": [
            {"path": path, "matches": count} for path, count in file_counts.most_common(20)
        ],
        "findings": findings,
        # Distributional, not gated. See the module docstring.
        "spoken_register": spoken_register,
        "surface_profiles": profiles,
    }


def render_spoken_register(report: dict[str, object], top: int) -> list[str]:
    """Render the distributional read-aloud section.

    Nothing here is an error. Each block names a pressure and where it is
    heaviest, so a read-aloud pass can be aimed rather than guessed at.
    """
    spoken = report.get("spoken_register")
    if not spoken:
        return []

    dialogue = spoken["dialogue"]
    vocatives = spoken["vocatives"]
    contractible = dialogue["contractible_negations"]
    contracted = dialogue["contractions"]
    rate = dialogue["contraction_rate"]

    lines = [
        "",
        "Spoken register profile",
        "-----------------------",
        f"Translated words: {spoken['words']}  (in dialogue: {spoken['speech_words']})",
        "",
        "Dialogue negation:",
        f"- contracted: {contracted}",
        f"- left uncontracted: {contractible}",
    ]
    if rate is not None:
        lines.append(f"- contraction rate: {rate:.1%}")
    lines.append(
        "    The standard allows neutral contractions. Emphatic negation is real,"
    )
    lines.append(
        "    so this is a rate to judge, not a list of lines to change."
    )

    medial_share = vocatives["medial_share"]
    lines.extend(
        [
            "",
            "Vocative position:",
            f"- opening the sentence: {vocatives['initial']}",
            f"- wedged mid-clause: {vocatives['medial']}",
            f"- closing the sentence: {vocatives['final']}",
        ]
    )
    if medial_share is not None:
        lines.append(f"- mid-clause share: {medial_share:.1%}")
    lines.append(
        "    Mid-clause address is the stiffest position for a speaking voice."
    )

    lines.extend(
        [
            "",
            f"Sentences over {spoken['breath_limit']} words: {spoken['over_breath_limit']}",
        ]
    )
    for unit in spoken["longest_units"][:top]:
        lines.append(f"- {unit['path']}:{unit['line']} ({unit['words']}w) {unit['opening']} ...")
    if spoken["over_breath_limit"]:
        lines.extend(
            [
                "    Measured between full stops. Semicolons and dashes do give a",
                "    reader somewhere to breathe, and a deliberately piled-up",
                "    sentence can be the point, so read the long ones before cutting.",
            ]
        )

    lines.extend(["", "Repeated units carrying the most weight, within one surface:"])
    if not spoken["repeated_units"]:
        lines.append("- none above the reporting threshold.")
    for unit in spoken["repeated_units"][:top]:
        lines.append(
            f"- {unit['path']} x{unit['occurrences']} ({unit['words']}w,"
            f" weight {unit['weight']}): {unit['text']}"
        )

    lines.extend(["", "Repeated units shared across surfaces:"])
    if not spoken["shared_units"]:
        lines.append("- none above the reporting threshold.")
    for unit in spoken["shared_units"][:top]:
        lines.append(
            f"- {unit['surfaces']} surfaces, x{unit['occurrences']}"
            f" ({unit['words']}w, weight {unit['weight']}): {unit['text']}"
        )
    lines.append(
        "    Perfect the unit before it repeats. See PLAIN_ENGLISH_STANDARD rule 4."
    )
    lines.append(
        "    A shared unit is the highest-leverage edit in the corpus: fixing it"
    )
    lines.append("    once improves every surface that carries it.")
    return lines


def render_text(report: dict[str, object], top: int, spoken: bool = False) -> str:
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
        if spoken:
            lines.extend(render_spoken_register(report, top))
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

    if spoken:
        lines.extend(render_spoken_register(report, top))

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
    parser.add_argument(
        "--spoken",
        action="store_true",
        help=(
            "Also show the spoken register profile: dialogue contraction rate, "
            "vocative position, breath spans, and repeated-unit weight. Always "
            "advisory; --strict never gates on it."
        ),
    )
    args = parser.parse_args()

    report = build_report(REPO_ROOT, paths=args.path)
    if args.format == "json":
        write_output(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    else:
        write_output(render_text(report, max(args.top, 1), spoken=args.spoken) + "\n")

    if args.strict and report["summary"]["matches"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
