#!/usr/bin/env python3
"""Generate the next-sutta priority table from the live corpus.

`docs/generated/next-sutta-priority-table.md` used to be written by hand into
`docs/generated/`, where nothing regenerated it. It went stale the moment the
corpus moved: by 2026-09-13 it still reported 61 surfaces and 101 orphans
against an actual 64 and 91, and still listed a finished text as queue item 1.

Everything numeric here is now derived from `terms/` and the surface registry,
so `scripts/check_generated_docs.py` fails when the committed file drifts. The
queue itself is editorial and stays in `QUEUE` below, next to the reader
metadata it belongs with.

The Pali word counts in `QUEUE` are recorded rather than computed. Word counts
come from `.bilara-cache`, which is gitignored, so computing them here would
make the generated file differ between a machine that has fetched the root
texts and one that has not.
"""

from __future__ import annotations

import argparse
import textwrap
from dataclasses import dataclass
from pathlib import Path

try:
    from scripts.audit_surface_leverage import (
        build_leverage,
        load_entries,
        translated_suttas,
    )
except ModuleNotFoundError:
    from audit_surface_leverage import (
        build_leverage,
        load_entries,
        translated_suttas,
    )


REPO_ROOT = Path(__file__).resolve().parent.parent
TERMS_DIR = REPO_ROOT / "terms"
OUTPUT_DIR = REPO_ROOT / "docs" / "generated"


@dataclass(frozen=True)
class QueueItem:
    """One row of the Wave 10 queue, in the order it is worked."""

    position: str
    sutta: str
    pali_title: str
    pali_words: int
    orphan_anchor: str
    value: str


# Wave 10, as committed in docs/wave-10-execution-plan.md. Keep the two in step.
QUEUE: tuple[QueueItem, ...] = (
    QueueItem(
        "complete", "SN 45.8", "Vibhaṅga", 300, "`ariya`",
        "published 2026-08-25; path-factor cluster now has no dark governed terms",
    ),
    QueueItem(
        "complete", "SN 12.44", "Loka", 182, "`loka`",
        "published 2026-08-25; connects lived sensory experience to dependent arising",
    ),
    QueueItem(
        "complete", "AN 3.88", "Tatiyasikkhā", 230, "`adhicitta`",
        "published 2026-08-25; threefold training; replaces the false AN 4.41 leverage signal",
    ),
    QueueItem(
        "complete", "Iti 49", "Diṭṭhigata", 173, "`pariyuṭṭhāna`",
        "published 2026-08-25; active takeover by views; abandonment-sequence cluster",
    ),
    QueueItem(
        "complete", "AN 11.12", "Dutiyamahānāma", 367, "—",
        "published 2026-08-25; six verified recollection anchors for daily life",
    ),
    QueueItem(
        "complete", "SN 12.20", "Paccaya", 355, "—",
        "published 2026-08-27; anchored four of five ranked orphan signals, not five",
    ),
    QueueItem(
        "complete", "AN 8.39", "Abhisanda", 268, "—",
        "published 2026-09-13; both ranked orphan signals anchored, plus `dāna`, `saraṇa`, `saṅgha`",
    ),
    QueueItem(
        "next", "SN 46.1", "Himavanta", 125, "—",
        "one orphan anchor (`bojjhaṅga-bhāvanā`) and a compact awakening-factor practice",
    ),
)

METHOD_NOTES: tuple[str, ...] = (
    "Direct inspection found that SN 55.30 contains `ariyasāvaka` and an "
    "abbreviated Saṅgha formula, not `ariyapuggala`; it is not a priority anchor.",
    "AN 11.12 contains six of its seven credited recollection terms, not "
    "`upasamānussati`; that term belongs to the AN 1.296-305 list.",
    "AN 8.39 does not contain `veramaṇī` in any form, so the "
    "`kāmesu-micchācāra` citation that quoted it was repaired to the "
    "discourse's own `pahāya … paṭivirato hoti` wording.",
    "SN 50.1 and the other enumeration or peyyāla stubs remain formula or "
    "cluster-sheet work rather than reader translations.",
    "Longer one-anchor candidates such as DN 21 and DN 1 remain deferred.",
)


def load_terms() -> list[dict[str, object]]:
    """The term records this report is derived from.

    Named `load_terms` because `scripts/check_generated_docs.py` requires a
    generator to expose `OUTPUT_DIR`, `load_terms()`, and `write_outputs()`.
    """
    return load_entries(TERMS_DIR)


def build_report(terms: list[dict[str, object]]) -> dict[str, int]:
    """Corpus-wide counts, computed the same way the leverage audit computes them."""
    translated = translated_suttas()
    cited = [entry for entry in terms if entry["refs"]]
    orphans = [
        entry for entry in cited if not (set(entry["refs"]) & translated)
    ]
    leverage = build_leverage(terms, translated)
    orphan_majors = {
        name
        for row in leverage.values()
        for name in row.orphan_majors
    }
    return {
        "surfaces": len(translated),
        "records": len(terms),
        "cited": len(cited),
        "anchored": len(cited) - len(orphans),
        "orphans": len(orphans),
        "orphan_majors": len(orphan_majors),
    }


def render_table(report: dict[str, int]) -> str:
    lines = [
        "# Next Sutta Priority Table",
        "",
        "Generated by `scripts/next_sutta_priority_report.py`. Do not edit this",
        "file by hand; change the script or the live term data instead.",
        "",
    ]
    lines += textwrap.wrap(
        f"The corpus has {report['records']:,} term records and "
        f"{report['surfaces']} translation surfaces. Of {report['cited']} cited "
        f"records, {report['anchored']} are anchored by a translated surface and "
        f"{report['orphans']} are orphaned; {report['orphan_majors']} of those "
        "orphans are major terms.",
        width=78,
        break_long_words=False,
        break_on_hyphens=False,
    )
    lines += [
        "",
        "Use the [Wave 10 execution plan](../wave-10-execution-plan.md) for the",
        "active queue, validation, and handoff gates, and the",
        "[full roadmap](../next-suttas-roadmap.md) for historical method notes.",
        "",
        "| Queue | Sutta | Pali length | Orphan major | Reader and policy value |",
        "| ---: | --- | ---: | --- | --- |",
    ]
    for item in QUEUE:
        lines.append(
            f"| {item.position} | `{item.sutta}` {item.pali_title} "
            f"| {item.pali_words} words | {item.orphan_anchor} | {item.value} |"
        )
    lines += [
        "",
        "After the last queue item, run a fresh audit rather than extending this",
        "ranking. Every wave so far has found leverage signals that were wrong",
        "until they were checked against the source.",
        "",
    ]
    lines += [f"- {note}" for note in METHOD_NOTES]
    lines += [
        "",
        "Reproduce the numbers:",
        "",
        "```bash",
        "python scripts/audit_surface_leverage.py --top 20",
        "python scripts/verify_example_sources.py --strict --top 30",
        "```",
    ]
    return "\n".join(lines)


def write_outputs(terms: list[dict[str, object]]) -> list[Path]:
    """Render the table into OUTPUT_DIR.

    `scripts/check_generated_docs.py` calls this with OUTPUT_DIR pointed at a
    temporary directory and compares the result against the committed file, so
    everything written here has to be a pure function of repository content.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / "next-sutta-priority-table.md"
    content = render_table(build_report(terms))
    path.write_text(content + ("" if content.endswith("\n") else "\n"), encoding="utf-8")
    return [path]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write the generated table under docs/generated/ instead of printing it.",
    )
    args = parser.parse_args()

    terms = load_terms()
    if args.write:
        for path in write_outputs(terms):
            print(f"Wrote {path.relative_to(REPO_ROOT).as_posix()}")
        return 0
    print(render_table(build_report(terms)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
