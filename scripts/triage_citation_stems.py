#!/usr/bin/env python3
"""Triage the `inflected` and `inconclusive` citation verdicts.

`verify_example_sources.py` reports six verdicts. Two of them are not
assertions that a citation is good, but they read like it: the script prints
`Every verifiable citation checks out` while both are outstanding.

- `inconclusive` means the root text uses peyyala somewhere, so a phrase that
  did not match might have been elided rather than absent.
- `inflected` means a word stem matched, not that the cited phrase is present.
  A citation can quote a different word built on the same root and pass.

On 2026-08-21 both buckets were found to contain genuinely wrong citations --
`bhagava` citing MN 1 for an opening formula sited at Savatthi when MN 1 opens
at Ukkattha, `adhicitta` citing an MN 44 that contains no `adhicitta`, and
others. This script narrows those buckets to a reviewable list.

The test it applies is the one that worked on the `partial` bucket: a citation
is suspect when a whole word in it has no stem anywhere in the cited sutta. A
word that is genuinely present in another inflection still shares its stem; a
word from a different lemma does not.

**The output is a list of suspects, not a list of errors.** The screen
over-flags compounds and sandhi, where a word that is present appears only
inside a longer form. `cover` reports how much of the missing word the sutta
can account for as a contiguous substring, which sorts the likely-wrong ahead
of the likely-compound, but every row still needs a human check against the
source before it is called wrong.

Needs network access on first run for any sutta not already in
`.bilara-cache`, so it is deliberately not part of `run_checks.py`, for the
same reason `verify_example_sources.py` is not.

    python scripts/triage_citation_stems.py
    python scripts/triage_citation_stems.py --band A
    python scripts/triage_citation_stems.py --format json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import verify_example_sources as ves  # noqa: E402


MIN_WORD = 4
STEM = 5
TRIAGED_VERDICTS = ("inflected", "inconclusive")


def band_for(cover: float) -> str:
    """A over B over C, by how little of the missing word the sutta explains."""
    if cover <= 0.40:
        return "A"
    if cover <= 0.60:
        return "B"
    return "C"


def longest_shared_run(word: str, haystack: str) -> int:
    """Length of the longest contiguous slice of `word` present in `haystack`."""
    for size in range(len(word), 3, -1):
        for start in range(0, len(word) - size + 1):
            if word[start:start + size] in haystack:
                return size
    return 0


def triage(findings: list[dict], cache_dir: Path) -> list[dict]:
    texts: dict[str, str] = {}
    rows: list[dict] = []
    for finding in findings:
        if finding.get("verdict") not in TRIAGED_VERDICTS:
            continue
        source = finding.get("source")
        if source not in texts:
            resolved = ves.resolve_source(source, cache_dir)
            texts[source] = ves.normalize(resolved or "")
        haystack = texts[source]
        if not haystack:
            continue
        words = [w for w in ves.normalize(finding["pali"]).split() if len(w) > MIN_WORD - 1]
        missing = [w for w in words if w[:STEM] not in haystack]
        if not missing:
            continue
        detail = []
        for word in missing:
            run = longest_shared_run(word, haystack)
            detail.append({"word": word, "explained": run, "of": len(word),
                           "cover": round(run / len(word), 2)})
        cover = min(d["cover"] for d in detail)
        rows.append({
            "record": finding["record"],
            "source": source,
            "verdict": finding.get("verdict"),
            "pali": finding["pali"],
            "missing": detail,
            "cover": cover,
            "band": band_for(cover),
        })
    rows.sort(key=lambda r: (r["cover"], r["record"]))
    return rows


def render_text(rows: list[dict], band: str | None) -> str:
    shown = [r for r in rows if band is None or r["band"] == band]
    counts = {b: sum(1 for r in rows if r["band"] == b) for b in ("A", "B", "C")}
    lines = [
        "Citation stem triage",
        "",
        f"Suspects: {len(rows)}"
        f"   A (likely wrong) {counts['A']}"
        f"   B {counts['B']}"
        f"   C (likely compound) {counts['C']}",
        "",
        "A suspect is a citation with a whole word whose stem is absent from the",
        "cited sutta. This is a review list, not an error list: the screen",
        "over-flags compounds and sandhi. Check each against the source.",
        "",
    ]
    for row in shown:
        lines.append(
            f"[{row['band']}] {row['record']} <- {row['source']} ({row['verdict']})"
        )
        lines.append(f"      quotes: {row['pali'][:88]}")
        for d in row["missing"]:
            lines.append(
                f"      missing {d['word']} -- sutta explains {d['explained']}/{d['of']}"
            )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--band", choices=("A", "B", "C"))
    parser.add_argument("--cache-dir", default=str(REPO_ROOT / ".bilara-cache"))
    args = parser.parse_args(argv)

    cache_dir = Path(args.cache_dir)
    report = ves.build_report(cache_dir=cache_dir)
    rows = triage(report["findings"], cache_dir)

    # Not `print`: the report is full of Pali diacritics, and on Windows a
    # redirected stdout defaults to cp1252, which raises rather than degrades.
    # `ves.write_output` encodes with errors="replace", so piping the report to
    # a file works the same way it does for verify_example_sources.py.
    if args.format == "json":
        payload = [r for r in rows if args.band is None or r["band"] == args.band]
        ves.write_output(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    else:
        ves.write_output(render_text(rows, args.band) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
