#!/usr/bin/env python3
"""Check that each example_phrase's cited source really contains its Pali.

`lint_terms.py` already checks that a reviewed or stable major entry *has*
example sources. Nothing checked that a cited source actually contains the
quoted Pali, and on 2026-08-19 several records were found citing suttas for
text that is not in them -- including two records left with no verified
citation at all.

This script closes that gap. It reads each cited sutta from the Vipassana
Research Institute's Chaṭṭha Saṅgāyana Tipiṭaka (`scripts/vri_source.py`) and
reports, per example, whether the quoted Pali can be found there.

It used to read SuttaCentral's Mahāsaṅgīti root text. That text's publication
record asks that it not be used in AI-derived work, and this project is drafted
with AI assistance, so on 2026-11-10 the owner stopped all use of SuttaCentral
content; see `docs/source-text-policy.md`.

It is deliberately NOT part of `run_checks.py`: it needs network access, and a
check that fails when GitHub is unreachable would be worse than no check. Run
it deliberately, and after any pass that adds or edits example_phrases.

Verdicts, grouped by what they actually establish:

  verified
    exact        the quoted words are in the text, as whole words, in order

  qualified -- a real relationship, but not the quoted words
    compound     the quoted word appears inside a longer word, as `sati` does
                 inside `satipaṭṭhāna`. Ordinary lexicographic practice, and
                 weaker evidence than the word itself being present
    inflected    not found, but every word's stem is -- usually a lemma cited
                 for an inflected passage

  failed
    partial      some words of the phrase are present but not all; usually the
                 right sutta quoted with the wrong wording
    absent       no word of the phrase appears; the citation points at the
                 wrong sutta

  unresolved -- the check could not settle it either way
    inconclusive the root text elides passages with peyyala, so absence proves
                 nothing
    unfetched    the source could not be retrieved
    unsupported  the collection is not addressable by this script
    source-changed  the fetched source no longer matches its recorded pin

Matching is on whole words. Plain substring containment, which this script used
at first, let a short quotation be "verified" by a longer unrelated word: `sati`
is inside `satipaṭṭhānā` and `paṭṭhāna` is inside `satipaṭṭhānasutta`.

`--strict` fails on every failed citation, and on every unresolved one that is
not explicitly waived in `reviews/source-verification-waivers.json` with a
reason. Unresolved rows used to exit zero, so an unreachable source read as
success.

VRI corrects its files from time to time, so the digest of each cited passage
as read is recorded in `reviews/source-pins.json`. A citation whose passage
has changed since is reported rather than re-verified against different text.

DN, MN, SN, AN, Dhp, Ud, Iti, and Snp citations are resolved. Thag, Thig, and a
bare `KN` are reported as unsupported.

Two caveats before acting on a report:

1. Numbering is not stable across editions. Citations keep the familiar
   numbering and `vri_source.py` maps it onto VRI's divisions; where VRI
   splits a discourse differently the shift is recorded there. An `absent`
   verdict may mean the mapping landed on a neighbouring discourse rather
   than that the citation is wrong. Check the passage heading (`--format json`)
   before concluding anything.
2. `inflected` is usually not an error. Records often cite a lemma or stem
   form rather than the exact inflected string in the text, which is ordinary
   lexicographic practice.

Treat this as a triage tool that tells you where to look, not as an oracle.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import hashlib
from collections import Counter
from pathlib import Path

try:
    from scripts import vri_source
except ModuleNotFoundError:
    import vri_source  # type: ignore[no-redef]


REPO_ROOT = Path(__file__).resolve().parent.parent
TERMS_DIR = REPO_ROOT / "terms"
PINS_PATH = REPO_ROOT / "reviews" / "source-pins.json"
WAIVERS_PATH = REPO_ROOT / "reviews" / "source-verification-waivers.json"

VERIFIED = ("exact",)
QUALIFIED = ("compound", "inflected")
FAILED = ("partial", "absent")
UNRESOLVED = ("inconclusive", "unfetched", "unsupported", "source-changed")
VERDICTS = VERIFIED + QUALIFIED + FAILED + UNRESOLVED

CITE_RE = re.compile(r"^(MN|DN|SN|AN|KN|Ud|Iti|Snp|Dhp|Thag|Thig)\s+(\d+)(?:\.(\d+))?$")
UNSUPPORTED = {"KN", "Thag", "Thig"}
ELLIPSIS = re.compile(r"\.{2,}|…+|\bpe\b")


def citation_supported(citation: str) -> bool:
    """Whether a citation identifies a collection the VRI resolver understands."""
    match = CITE_RE.match(citation.strip())
    return bool(match and match.group(1) not in UNSUPPORTED and vri_source.supported(citation))


DIACRITICS = str.maketrans({
    "ā": "a", "ī": "i", "ū": "u", "ṁ": "m", "ṃ": "m", "ṅ": "n", "ñ": "n",
    "ṇ": "n", "ṭ": "t", "ḍ": "d", "ḷ": "l", "ṣ": "s", "ś": "s", "ṛ": "r",
    "ṝ": "r", "ḥ": "h", "ĩ": "i", "õ": "o", "ū": "u",
})


def normalize(text: str) -> str:
    """Fold a Pali string to a comparable, edition-insensitive form."""
    out = text.casefold().translate(DIACRITICS)
    # Punctuation must go, not just quotes: records quote phrases without the
    # commas the root text uses, so `cetanahan bhikkhave` would otherwise fail
    # against `Cetanāhaṁ, bhikkhave,`.
    out = re.sub(r"[“”\"'‘’\[\](),.;:!?—–-]", " ", out)
    out = re.sub(r"\s+", " ", out)
    return out.strip()


def source_digest(body: str) -> str:
    """A stable digest of a fetched source file."""
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def load_pins(path: Path = PINS_PATH) -> dict[str, str]:
    """Recorded digests of the source texts these verdicts were reached against.

    The upstream root texts are fetched from a moving branch, so a verdict is
    only reproducible if the bytes it was reached against are identified. A
    citation whose source no longer matches its pin is reported as
    `source-changed` rather than quietly re-verified against different text.
    """
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    pins = data.get("sources") if isinstance(data, dict) else None
    if not isinstance(pins, dict):
        return {}
    return {str(k): str(v) for k, v in pins.items()}


def write_pins(pins: dict[str, str], path: Path = PINS_PATH) -> None:
    payload = {
        "_comment": (
            "sha256 of each cited passage as read from the VRI Chattha Sangayana XML. "
            "`scripts/verify_example_sources.py` reports `source-changed` when a fetched "
            "source no longer matches its pin, so a verdict cannot silently come from "
            "different text than the one it was reached against. Refresh deliberately with "
            "--update-pins after reading what changed."
        ),
        "sources": dict(sorted(pins.items())),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_waivers(path: Path = WAIVERS_PATH) -> dict[tuple[str, int], str]:
    """Explicitly accepted unresolved examples, keyed by (record, index).

    An unresolved example is one the checker could not settle: the collection is
    not addressable, the source could not be fetched, or the root text elides
    the passage. Strict mode fails on those unless a waiver says, in words, why
    it is accepted. Silence used to count as success.
    """
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    entries = data.get("waivers") if isinstance(data, dict) else None
    result: dict[tuple[str, int], str] = {}
    if not isinstance(entries, list):
        return result
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        record = entry.get("record")
        index = entry.get("index")
        reason = entry.get("reason")
        if not isinstance(record, str) or not isinstance(index, int) or not isinstance(reason, str) or not reason.strip():
            raise ValueError(f"source-verification waiver needs record, index, and a reason: {entry!r}")
        key = (record, index)
        if key in result:
            raise ValueError(f"duplicate waiver for {record} example[{index}]")
        result[key] = reason.strip()
    return result


def resolve_source(citation: str, cache_dir: Path) -> str | None:
    """The cited passage's plain text from the VRI edition, or None.

    None covers both a book that could not be read and a citation that could
    not be placed; either way nothing was checked, and the row is reported as
    unresolved rather than failed.
    """
    try:
        located = vri_source.locate(citation, cache_dir=cache_dir)
    except vri_source.SourceUnavailable:
        return None
    if located is None or not located.text.strip():
        return None
    return located.text


def source_text(body: str) -> tuple[str, bool]:
    """Return the normalized passage text and whether it uses peyyala elision."""
    return normalize(body), is_abridged(body)


def stems_of(phrase: str) -> list[str]:
    """Conservative stems for every substantive word in the phrase.

    Every word is stemmed, not just the longest one. Taking only the longest
    word makes `kammassa phalaṁ` look merely inflected in a text that contains
    `kamma` but no `phala` at all, which hides the real error.
    """
    # normalize() has already folded diacritics away, so plain a-z suffices.
    # Trailing vowels are stripped as well as the ending, because Pali case
    # endings change the final vowel: `phassassa` and `phasso` share only
    # `phass`, and a stem of `phassa` would miss the match.
    words = [w for w in re.split(r"[^a-z]+", normalize(phrase)) if len(w) >= 5]
    stems = [w[: max(4, len(w) - 3)].rstrip("aeiou") for w in words]
    return [s for s in stems if len(s) >= 3]


PEYYALA = re.compile(r"…pe…|\bpe\b|\.{3}pe\.{3}")


def is_abridged(raw_text: str) -> bool:
    """True when the root text elides passages with peyyala markers.

    This matters for the verdict. SN 12.2 abbreviates its quenching chain after
    two links, so a citation quoting `namarupanirodha salayatananirodho` is
    quoting a line that really belongs to the passage but is not spelled out in
    the root file. Calling that `absent` would be wrong.
    """
    return bool(PEYYALA.search(raw_text))


def word_tokens(text: str) -> list[str]:
    """The normalized text as whole words."""
    return [w for w in re.split(r"[^a-z0-9]+", text) if w]


def contains_words(tokens: list[str], phrase: str) -> bool:
    """Whether the phrase appears as consecutive whole words.

    Substring containment was the original test, and it let a short quotation
    be "verified" by a longer unrelated word: `sati` is inside `satipaṭṭhānā`,
    and `paṭṭhāna` is inside `satipaṭṭhānasutta`. Neither is an occurrence of
    the quoted word, so neither should count as finding it.
    """
    wanted = word_tokens(phrase)
    if not wanted:
        return False
    for start in range(len(tokens) - len(wanted) + 1):
        if tokens[start : start + len(wanted)] == wanted:
            return True
    return False


def contains_as_compound_member(tokens: list[str], phrase: str) -> bool:
    """Whether the quoted words appear inside a single longer word.

    Two real relationships land here. A record cites `sati` for a passage that
    has `satipaṭṭhāna`; and a record quotes `oghaṃ atariṃ` where SN 1.1 has the
    sandhi-joined `oghamatarī`. Both are ordinary lexicographic practice and
    weaker evidence than the words being present as quoted, so they get their
    own verdict rather than passing as `exact` -- or, for the sandhi case,
    being called a failure.
    """
    wanted = word_tokens(phrase)
    if not wanted:
        return False
    joined = "".join(wanted)
    if len(joined) < 4:
        return False
    return any(token != joined and joined in token for token in tokens)


def stem_presence(tokens: list[str], stem: str) -> bool:
    """Whether a stem appears inside some word.

    Deliberately loose, and only ever reached after the whole-word tests have
    failed. A stem can sit in the middle of a word legitimately: SN 1.1 has the
    sandhi-joined `oghamatarī` for a record quoting `oghaṃ atariṃ`, and
    anchoring the stem to a word start reported that real citation as a
    failure. The strict tests above are what stop a loose match from being
    called verified.
    """
    return any(stem in token for token in tokens)


def check_phrase(pali: str, haystack: str, abridged: bool = False) -> str:
    """Classify how well the cited source supports one quoted phrase.

    Returns `exact`, `compound`, `inflected`, `partial`, `inconclusive`, or
    `absent`. Only `exact` means the quoted words are in the text as quoted.
    """
    tokens = word_tokens(haystack)
    # Split on the ellipsis BEFORE normalizing: normalize() strips periods, so
    # a `...` would already be gone by the time this ran.
    chunks = [normalize(c) for c in ELLIPSIS.split(pali)]
    chunks = [c for c in chunks if len(c) >= 4]
    if not chunks:
        chunks = [normalize(pali)]
    if all(contains_words(tokens, chunk) for chunk in chunks):
        return "exact"
    if all(contains_words(tokens, c) or contains_as_compound_member(tokens, c) for c in chunks):
        return "compound"
    stems = stems_of(pali)
    # Only call it an inflection problem when every substantive word is present
    # in some form. If any word is missing outright, the citation is suspect.
    if stems and all(stem_presence(tokens, stem) for stem in stems):
        return "inflected"
    if abridged:
        return "inconclusive"
    # Distinguish a wrong source from a right source quoted badly. MN 11 really
    # does discuss kamupadana, and only the exact phrase `catasso upadana` is
    # not in it; AN 3.86 contains no `anagam` at all. Calling both `absent`
    # overstates the first and understates the second.
    if stems and any(stem_presence(tokens, stem) for stem in stems):
        return "partial"
    return "absent"


def collect_examples(terms_dir: Path = TERMS_DIR) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path in sorted(terms_dir.rglob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if not isinstance(data, dict):
            continue
        for index, example in enumerate(data.get("example_phrases") or []):
            if not isinstance(example, dict):
                continue
            pali = example.get("pali")
            source = example.get("source")
            if not isinstance(pali, str) or not isinstance(source, str):
                continue
            rows.append(
                {
                    "record": path.stem,
                    "index": index,
                    "source": source.strip(),
                    "pali": pali.strip(),
                }
            )
    return rows


def build_report(
    terms_dir: Path = TERMS_DIR,
    cache_dir: Path | None = None,
    only: str | None = None,
    pins: dict[str, str] | None = None,
    waivers: dict[tuple[str, int], str] | None = None,
) -> dict[str, object]:
    cache_dir = cache_dir or vri_source.DEFAULT_CACHE_DIR
    pins = {} if pins is None else pins
    waivers = {} if waivers is None else waivers
    rows = collect_examples(terms_dir)
    if only:
        rows = [r for r in rows if r["record"] == only]

    texts: dict[str, tuple[str, bool] | None] = {}
    digests: dict[str, str] = {}
    changed_sources: set[str] = set()
    findings: list[dict[str, object]] = []

    for row in rows:
        citation = str(row["source"])
        if not citation_supported(citation):
            row["verdict"] = "unsupported"
            findings.append(row)
            continue
        if citation not in texts:
            body = resolve_source(citation, cache_dir)
            if body is None:
                texts[citation] = None
            else:
                digest = source_digest(body)
                digests[citation] = digest
                pinned = pins.get(citation)
                if pinned is not None and pinned != digest:
                    changed_sources.add(citation)
                texts[citation] = source_text(body)
        entry = texts[citation]
        if entry is None:
            row["verdict"] = "unfetched"
        elif citation in changed_sources:
            # The text upstream is not the text this citation was checked
            # against. Re-verifying against the new bytes would quietly change
            # what the recorded verdict means.
            row["verdict"] = "source-changed"
        else:
            haystack, abridged = entry
            row["verdict"] = check_phrase(str(row["pali"]), haystack, abridged)
        findings.append(row)

    # Attached in one pass so every unresolved verdict is covered, including
    # the unsupported-collection branch that returns before the checks above.
    for row in findings:
        if row["verdict"] in UNRESOLVED:
            waiver = waivers.get((str(row["record"]), int(row["index"])))
            if waiver:
                row["waiver"] = waiver

    counts = Counter(str(f["verdict"]) for f in findings)
    unresolved = [f for f in findings if f["verdict"] in UNRESOLVED]
    return {
        "summary": {
            "examples": len(findings),
            "sources": len(texts),
            "verified": sum(counts.get(k, 0) for k in VERIFIED),
            "qualified": sum(counts.get(k, 0) for k in QUALIFIED),
            "failed": sum(counts.get(k, 0) for k in FAILED),
            "unresolved": len(unresolved),
            "unresolved_waived": sum(1 for f in unresolved if f.get("waiver")),
            "pinned_sources": sum(1 for c in texts if c in pins),
            **{k: counts.get(k, 0) for k in VERDICTS},
        },
        "digests": dict(sorted(digests.items())),
        "findings": findings,
    }


def render_text(report: dict[str, object], top: int) -> str:
    s = report["summary"]
    lines = [
        "Example source verification",
        "",
        f"Examples checked: {s['examples']}   Sources fetched: {s['sources']}"
        f"   Pinned: {s['pinned_sources']}",
        "",
        f"Verified (quoted words present as quoted): {s['verified']}",
        f"  exact        {s['exact']}",
        f"Qualified (related but not the quoted words): {s['qualified']}",
        f"  compound     {s['compound']}   the word appears inside a longer word",
        f"  inflected    {s['inflected']}   the stems are present in another form",
        f"Failed: {s['failed']}",
        f"  partial      {s['partial']}   some words of the phrase appear, not all",
        f"  absent       {s['absent']}   no word of the phrase appears",
        f"Unresolved: {s['unresolved']} ({s['unresolved_waived']} waived)",
        f"  inconclusive {s['inconclusive']}   the root text elides the passage",
        f"  unfetched    {s['unfetched']}   the source could not be retrieved",
        f"  unsupported  {s['unsupported']}   the collection is not addressable",
        f"  source-changed {s['source-changed']}   upstream no longer matches its pin",
    ]
    problems = [f for f in report["findings"] if f["verdict"] in FAILED]
    if problems:
        lines.extend(["", "Citations needing review:"])
        for f in sorted(problems, key=lambda x: (x["verdict"], x["record"]))[:top]:
            lines.append(
                f"- [{f['verdict']}] {f['record']} example[{f['index']}] "
                f"cites {f['source']}: {str(f['pali'])[:70]}"
            )
        if len(problems) > top:
            lines.append(f"  ... and {len(problems) - top} more")
        lines.extend([
            "",
            "`partial` means only some words of the quoted phrase appear;",
            "`absent` means no word of the phrase appears in the cited sutta.",
            "Before treating one as wrong, check the passage heading: numbering",
            "differs between editions, so the mapping may have landed on a",
            "neighbouring discourse.",
        ])
    else:
        lines.extend(["", "- No failed citation matches."])

    unwaived = [
        f for f in report["findings"]
        if f["verdict"] in UNRESOLVED and not f.get("waiver")
    ]
    if unwaived:
        lines.extend(["", f"Unresolved and not waived ({len(unwaived)}):"])
        for f in sorted(unwaived, key=lambda x: (x["verdict"], x["record"]))[:top]:
            lines.append(
                f"- [{f['verdict']}] {f['record']} example[{f['index']}] cites {f['source']}"
            )
        if len(unwaived) > top:
            lines.append(f"  ... and {len(unwaived) - top} more")
        lines.append(
            "These prove nothing either way. Accept one on purpose in "
            "reviews/source-verification-waivers.json, with a reason."
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
    parser.add_argument("--top", type=int, default=40)
    parser.add_argument("--record", help="Check only this record stem.")
    parser.add_argument(
        "--cache-dir", type=Path, default=vri_source.DEFAULT_CACHE_DIR,
        help="Where fetched VRI books are cached. Set VRI_TIPITAKA_DIR to read a local clone instead.",
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="Exit non-zero on any failed citation, and on any unresolved one "
             "that is not explicitly waived.",
    )
    parser.add_argument(
        "--update-pins", action="store_true",
        help="Record the digest of every source fetched in this run, so later "
             "runs can tell when upstream text has changed.",
    )
    args = parser.parse_args()

    try:
        waivers = load_waivers()
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}")
        return 1

    pins = load_pins()
    report = build_report(TERMS_DIR, args.cache_dir, args.record, pins=pins, waivers=waivers)

    if args.update_pins:
        digests = report["digests"]
        assert isinstance(digests, dict)
        if args.record:
            print("ERROR: --update-pins records the whole corpus; drop --record.")
            return 1
        merged = {**pins, **digests}
        write_pins(merged)
        print(
            f"Pinned {len(digests)} fetched source(s); {len(merged)} total in "
            f"{PINS_PATH.relative_to(REPO_ROOT).as_posix()}."
        )
        return 0

    if args.format == "json":
        write_output(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    else:
        write_output(render_text(report, max(args.top, 1)) + "\n")

    if args.strict:
        summary = report["summary"]
        assert isinstance(summary, dict)
        unwaived = int(summary["unresolved"]) - int(summary["unresolved_waived"])
        if int(summary["failed"]) or unwaived:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
