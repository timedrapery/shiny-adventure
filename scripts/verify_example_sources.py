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

Verdicts:

  ok         the quoted Pali was found
  inflected  not found, but the word stem is present -- usually a wrong case
             ending in the citation rather than a wrong source
  partial    some words of the phrase are present but not all; usually the
             right sutta quoted with the wrong wording
  inconclusive the root text elides passages with peyyala, so absence proves
             nothing
  absent     no word of the phrase appears; the citation points at the wrong
             sutta
  unfetched  the source could not be retrieved
  unsupported  the collection is not addressable by this script (see below)

Dhp, Iti, Snp, Thag, and Thig are chunked by verse range in Bilara rather than
by the numbers used in citations, so they are reported as unsupported rather
than guessed at.

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
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
TERMS_DIR = REPO_ROOT / "terms"
BILARA_ROOT = (
    "https://raw.githubusercontent.com/suttacentral/sc-data/main/"
    "sc_bilara_data/root/pli/ms/sutta"
)
CITE_RE = re.compile(r"^(MN|DN|SN|AN|KN|Ud|Iti|Snp|Dhp|Thag|Thig)\s+(\d+)(?:\.(\d+))?$")
UNSUPPORTED = {"Dhp", "Iti", "Snp", "Thag", "Thig", "KN", "Ud"}
ELLIPSIS = re.compile(r"\.{2,}|…+|\bpe\b")


def source_url(citation: str) -> str | None:
    """Map a citation such as `SN 12.11` to its Bilara root-text URL."""
    match = CITE_RE.match(citation.strip())
    if not match:
        return None
    collection, major, minor = match.group(1), match.group(2), match.group(3)
    if collection in UNSUPPORTED:
        return None
    low = collection.lower()
    if collection in {"MN", "DN"}:
        return f"{BILARA_ROOT}/{low}/{low}{major}_root-pli-ms.json"
    if collection in {"SN", "AN"} and minor:
        return f"{BILARA_ROOT}/{low}/{low}{major}/{low}{major}.{minor}_root-pli-ms.json"
    return None


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
    if url is None:
        return None
    body = fetch(url, cache_dir)
    if body is not None:
        return body

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


def check_phrase(pali: str, haystack: str, abridged: bool = False) -> str:
    """Return `ok`, `inflected`, `inconclusive`, or `absent` for one phrase."""
    # Split on the ellipsis BEFORE normalizing: normalize() strips periods, so
    # a `...` would already be gone by the time this ran.
    chunks = [normalize(c) for c in ELLIPSIS.split(pali)]
    chunks = [c for c in chunks if len(c) >= 4]
    if not chunks:
        chunks = [normalize(pali)]
    if all(chunk in haystack for chunk in chunks):
        return "ok"
    stems = stems_of(pali)
    # Only call it an inflection problem when every substantive word is present
    # in some form. If any word is missing outright, the citation is suspect.
    if stems and all(stem in haystack for stem in stems):
        return "inflected"
    if abridged:
        return "inconclusive"
    # Distinguish a wrong source from a right source quoted badly. MN 11 really
    # does discuss kamupadana, and only the exact phrase `catasso upadana` is
    # not in it; AN 3.86 contains no `anagam` at all. Calling both `absent`
    # overstates the first and understates the second.
    if stems and any(stem in haystack for stem in stems):
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
) -> dict[str, object]:
    cache_dir = cache_dir or (REPO_ROOT / ".bilara-cache")
    rows = collect_examples(terms_dir)
    if only:
        rows = [r for r in rows if r["record"] == only]

    texts: dict[str, tuple[str, bool] | None] = {}
    findings: list[dict[str, object]] = []

    for row in rows:
        citation = str(row["source"])
        url = source_url(citation)
        if url is None:
            row["verdict"] = "unsupported"
            findings.append(row)
            continue
        if citation not in texts:
            body = resolve_source(citation, cache_dir)
            texts[citation] = source_text(body) if body else None
        entry = texts[citation]
        if entry is None:
            row["verdict"] = "unfetched"
        else:
            haystack, abridged = entry
            row["verdict"] = check_phrase(str(row["pali"]), haystack, abridged)
        findings.append(row)

    counts = Counter(str(f["verdict"]) for f in findings)
    return {
        "summary": {
            "examples": len(findings),
            "sources": len(texts),
            **{k: counts.get(k, 0) for k in
               ("ok", "inflected", "inconclusive", "partial", "absent",
                "unfetched", "unsupported")},
        },
        "findings": findings,
    }


def render_text(report: dict[str, object], top: int) -> str:
    s = report["summary"]
    lines = [
        "Example source verification",
        "",
        f"Examples checked: {s['examples']}   Sources fetched: {s['sources']}",
        f"  ok          {s['ok']}",
        f"  inflected   {s['inflected']}",
        f"  inconclusive {s['inconclusive']}",
        f"  partial     {s['partial']}",
        f"  absent      {s['absent']}",
        f"  unfetched   {s['unfetched']}",
        f"  unsupported {s['unsupported']}",
    ]
    problems = [f for f in report["findings"] if f["verdict"] == "absent"]
    if problems:
        lines.extend(["", "Citations that do not check out:"])
        for f in sorted(problems, key=lambda x: (x["verdict"], x["record"]))[:top]:
            lines.append(
                f"- [{f['verdict']}] {f['record']} example[{f['index']}] "
                f"cites {f['source']}: {str(f['pali'])[:70]}"
            )
        if len(problems) > top:
            lines.append(f"  ... and {len(problems) - top} more")
        lines.extend([
            "",
            "`absent` means no word of the phrase appears in the cited sutta.",
            "Before treating one as wrong, check the fetched sutta's title: AN",
            "numbering differs between editions, so an AN citation may simply",
            "follow a different scheme. `inflected` and `inconclusive` are not",
            "listed here; neither is reliably an error.",
        ])
    else:
        lines.extend(["", "- Every verifiable citation checks out."])
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
        help="Exit non-zero if any citation is absent or inflected.",
    )
    args = parser.parse_args()

    report = build_report(TERMS_DIR, args.cache_dir, args.record)
    if args.format == "json":
        write_output(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    else:
        write_output(render_text(report, max(args.top, 1)) + "\n")

    if args.strict:
        s = report["summary"]
        if s["absent"]:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
