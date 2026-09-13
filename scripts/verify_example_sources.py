#!/usr/bin/env python3
"""Check that each example_phrase's cited source really contains its Pali.

`lint_terms.py` already checks that a reviewed or stable major entry *has*
example sources. Nothing checked that a cited source actually contains the
quoted Pali, and on 2026-08-19 several records were found citing suttas for
text that is not in them -- including two records left with no verified
citation at all.

This script closes that gap. It fetches the Bilara root text for each cited
sutta and reports, per example, whether the quoted Pali can be found there.

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
    unsupported  the collection is not addressable by this script (see below)
    source-changed  the fetched source no longer matches its recorded pin

Matching is on whole words. Plain substring containment, which this script used
at first, let a short quotation be "verified" by a longer unrelated word: `sati`
is inside `satipaṭṭhānā` and `paṭṭhāna` is inside `satipaṭṭhānasutta`.

`--strict` fails on every failed citation, and on every unresolved one that is
not explicitly waived in `reviews/source-verification-waivers.json` with a
reason. Unresolved rows used to exit zero, so an unreachable source read as
success.

Source texts are fetched from a moving upstream branch, so the digest of each
one is recorded in `reviews/source-pins.json`. A citation whose source has
changed since is reported rather than re-verified against different bytes.

The Khuddaka collections use several directory shapes. Dhp is bundled by verse
range; Iti, Snp, and Ud sit in vagga directories; Thag and Thig use direct text
files. The resolver handles each layout. Only a bare `KN` citation remains
unsupported because it does not identify a collection.

Two caveats before acting on a report:

1. AN numbering is not stable across editions. SuttaCentral's AN 3.134 is
   Parisasutta, and other schemes number the same discourses differently. An
   `absent` verdict on an AN citation may mean the citation follows a
   different numbering rather than that it is wrong. Check the fetched sutta's
   title before concluding anything.
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
import urllib.error
import urllib.request
import hashlib
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
TERMS_DIR = REPO_ROOT / "terms"
BILARA_ROOT = (
    "https://raw.githubusercontent.com/suttacentral/sc-data/main/"
    "sc_bilara_data/root/pli/ms/sutta"
)
PINS_PATH = REPO_ROOT / "reviews" / "source-pins.json"
WAIVERS_PATH = REPO_ROOT / "reviews" / "source-verification-waivers.json"

VERIFIED = ("exact",)
QUALIFIED = ("compound", "inflected")
FAILED = ("partial", "absent")
UNRESOLVED = ("inconclusive", "unfetched", "unsupported", "source-changed")
VERDICTS = VERIFIED + QUALIFIED + FAILED + UNRESOLVED

CITE_RE = re.compile(r"^(MN|DN|SN|AN|KN|Ud|Iti|Snp|Dhp|Thag|Thig)\s+(\d+)(?:\.(\d+))?$")
UNSUPPORTED = {"KN"}
ELLIPSIS = re.compile(r"\.{2,}|…+|\bpe\b")


def source_url(citation: str) -> str | None:
    """Map a citation such as `SN 12.11` to its Bilara root-text URL."""
    match = CITE_RE.match(citation.strip())
    if not match:
        return None
    collection, major, minor = match.group(1), match.group(2), match.group(3)
    if collection in UNSUPPORTED or collection == "Dhp":
        return None
    low = collection.lower()
    if collection in {"MN", "DN"}:
        return f"{BILARA_ROOT}/{low}/{low}{major}_root-pli-ms.json"
    if collection in {"SN", "AN"} and minor:
        return f"{BILARA_ROOT}/{low}/{low}{major}/{low}{major}.{minor}_root-pli-ms.json"
    if collection in {"Snp", "Ud"} and minor:
        return f"{BILARA_ROOT}/kn/{low}/vagga{major}/{low}{major}.{minor}_root-pli-ms.json"
    if collection in {"Thag", "Thig"} and minor:
        return f"{BILARA_ROOT}/kn/{low}/{low}{major}.{minor}_root-pli-ms.json"
    if collection == "Iti" and minor is None:
        vagga = (int(major) - 1) // 10 + 1
        return f"{BILARA_ROOT}/kn/iti/vagga{vagga}/iti{major}_root-pli-ms.json"
    return None


def citation_supported(citation: str) -> bool:
    """Whether a citation identifies a collection this resolver understands."""
    match = CITE_RE.match(citation.strip())
    return bool(match and match.group(1) not in UNSUPPORTED)


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


def fetch(url: str, cache_dir: Path, timeout: int = 60) -> str | None:
    cache_dir.mkdir(parents=True, exist_ok=True)
    cached = cache_dir / (url.rsplit("/", 1)[-1])
    if cached.exists():
        return cached.read_text(encoding="utf-8")
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            body = response.read().decode("utf-8")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError):
        return None
    cached.write_text(body, encoding="utf-8")
    return body


GITHUB_CONTENTS_API = (
    "https://api.github.com/repos/suttacentral/sc-data/contents/"
    "sc_bilara_data/root/pli/ms/sutta"
)
RANGE_FILE_RE = re.compile(r"^([a-z]+\d+)\.(\d+)-(\d+)_root-pli-ms\.json$")
DHP_RANGE_FILE_RE = re.compile(r"^dhp(\d+)-(\d+)_root-pli-ms\.json$")


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
            "sha256 of each cited source text as fetched from the upstream Bilara root. "
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


def range_candidates(citation: str) -> tuple[str, int] | None:
    """Split a citation into its directory stem and sutta number.

    Returns None for collections that are not bundled this way.
    """
    match = CITE_RE.match(citation.strip())
    if not match:
        return None
    collection, major, minor = match.group(1), match.group(2), match.group(3)
    if collection not in {"SN", "AN"} or not minor:
        return None
    low = collection.lower()
    return f"{low}{major}", int(minor)


def list_directory(stem: str, cache_dir: Path, timeout: int = 60) -> list[str]:
    """Filenames in a vagga directory, cached on disk.

    Uses the GitHub contents API because raw.githubusercontent serves files
    but not listings. One request per directory, cached, and a failure here
    degrades to the previous behaviour rather than raising.
    """
    collection = stem.rstrip("0123456789")
    cache_dir.mkdir(parents=True, exist_ok=True)
    cached = cache_dir / f"_listing_{stem}.json"
    if cached.exists():
        try:
            return json.loads(cached.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    url = f"{GITHUB_CONTENTS_API}/{collection}/{stem}"
    request = urllib.request.Request(url, headers={"User-Agent": "shiny-adventure"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError,
            json.JSONDecodeError):
        return []
    names = [str(entry.get("name", "")) for entry in payload]
    cached.write_text(json.dumps(names, ensure_ascii=False), encoding="utf-8")
    return names


def list_directory_path(directory: str, cache_dir: Path, timeout: int = 60) -> list[str]:
    """List a nested Bilara directory such as `kn/dhp`, with disk caching."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_key = directory.replace("/", "_")
    cached = cache_dir / f"_listing_{cache_key}.json"
    if cached.exists():
        try:
            return json.loads(cached.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    request = urllib.request.Request(
        f"{GITHUB_CONTENTS_API}/{directory}",
        headers={"User-Agent": "shiny-adventure"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError,
            json.JSONDecodeError):
        return []
    names = [str(entry.get("name", "")) for entry in payload]
    cached.write_text(json.dumps(names, ensure_ascii=False), encoding="utf-8")
    return names


def find_dhp_range_file(names: list[str], verse: int) -> str | None:
    """The Dhammapada bundle containing a verse number."""
    for name in names:
        match = DHP_RANGE_FILE_RE.match(name)
        if match and int(match.group(1)) <= verse <= int(match.group(2)):
            return name
    return None


def find_range_file(names: list[str], stem: str, number: int) -> str | None:
    """The bundled filename whose range covers `number`, if any.

    SuttaCentral bundles peyyala vaggas as e.g. sn50.1-12_root-pli-ms.json,
    so SN 50.1 has no file of its own and a per-sutta URL 404s.
    """
    for name in names:
        match = RANGE_FILE_RE.match(name)
        if not match:
            continue
        if match.group(1) != stem:
            continue
        if int(match.group(2)) <= number <= int(match.group(3)):
            return name
    return None


def resolve_source(citation: str, cache_dir: Path) -> str | None:
    """Fetch a citation's root text, falling back to its range bundle.

    Returns the body, or None when the text cannot be reached at all.
    """
    url = source_url(citation)
    if url is not None:
        body = fetch(url, cache_dir)
        if body is not None:
            return body

    match = CITE_RE.match(citation.strip())
    if match and match.group(1) == "Dhp":
        name = find_dhp_range_file(
            list_directory_path("kn/dhp", cache_dir), int(match.group(2))
        )
        return fetch(f"{BILARA_ROOT}/kn/dhp/{name}", cache_dir) if name else None

    split = range_candidates(citation)
    if split is None:
        return None
    stem, number = split
    name = find_range_file(list_directory(stem, cache_dir), stem, number)
    if name is None:
        return None
    collection = stem.rstrip("0123456789")
    return fetch(f"{BILARA_ROOT}/{collection}/{stem}/{name}", cache_dir)


def source_text(body: str) -> tuple[str, bool]:
    """Return the normalized root text and whether it uses peyyala elision."""
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return "", False
    if not isinstance(data, dict):
        return "", False
    raw = " ".join(str(v) for v in data.values())
    return normalize(raw), is_abridged(raw)


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
    cache_dir = cache_dir or (REPO_ROOT / ".bilara-cache")
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
            "Before treating one as wrong, check the fetched sutta's title: AN",
            "numbering differs between editions, so an AN citation may simply",
            "follow a different scheme.",
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
        "--cache-dir", type=Path, default=REPO_ROOT / ".bilara-cache",
        help="Where fetched root texts are cached.",
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
