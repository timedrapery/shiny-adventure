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
    """One row of the queue, in the order it is worked.

    `position` is display text only. `published` is the fact the tests check,
    so a row cannot drift out of step with the corpus by being relabelled.
    """

    position: str
    sutta: str
    pali_title: str
    pali_words: int
    orphan_anchor: str
    value: str
    published: bool = False


# Wave 11, as committed in docs/wave-11-execution-plan.md. Keep the two in step.
# Wave 10's completed items stay listed: the table is the corpus's queue
# history, and dropping finished rows would hide what each wave actually cost.
QUEUE: tuple[QueueItem, ...] = (
    QueueItem(
        "wave 10", "AN 11.12", "Dutiyamahānāma", 367, "—",
        "published 2026-08-25; six verified recollection anchors for daily life",
        published=True,
    ),
    QueueItem(
        "wave 10", "SN 12.20", "Paccaya", 355, "—",
        "published 2026-08-27; anchored four of five ranked orphan signals, not five",
        published=True,
    ),
    QueueItem(
        "wave 10", "AN 8.39", "Abhisanda", 268, "—",
        "published 2026-09-13; both ranked orphan signals anchored, plus `dāna`, `saraṇa`, `saṅgha`",
        published=True,
    ),
    QueueItem(
        "wave 10", "SN 46.1", "Himavanta", 125, "—",
        "published 2026-09-13; closed Wave 10; its one ranked orphan signal was a phrase the discourse does not contain",
        published=True,
    ),
    QueueItem(
        "next", "Dhp 21-32", "Appamādavagga", 124, "`appamāda`",
        "twelve verses in one upstream file; the repository's first verse surface, so settle verse handling in the packet",
    ),
    QueueItem(
        "wave 11", "Ud 8.3", "Tatiyanibbānapaṭisaṁyutta", 84, "—",
        "published 2026-09-13; anchors `asaṅkhata-dhātu`, and settles the Udāna framing formula",
        published=True,
    ),
    QueueItem(
        "3", "SN 22.22", "Bhāra", 108, "—",
        "anchors the burden formula; note that `puggalo tissa vacanīyaṁ` is a crux the translation must not settle",
    ),
    QueueItem(
        "4", "SN 22.26", "Assāda", 223, "—",
        "anchors the gratification, danger, and escape formula for the five heaps, exactly",
    ),
    QueueItem(
        "5", "MN 122", "Mahāsuññata", 1547, "—",
        "anchors `appicchatā` and `asaṁsagga`; the last multi-orphan text that is neither a stub nor a length deferral",
    ),
)

METHOD_NOTES: tuple[str, ...] = (
    "Every Wave 11 signal was checked against the cached root text before the "
    "item was given a position. The audit that produced this queue found and "
    "repaired eight false or mis-cased citations in the records it was ranking.",
    "SN 50.1 is permanently off the queue: upstream has no `sn50.1` file at "
    "all. The text lives in `sn50.1-12`, a Ganges-repetition series covering "
    "twelve discourses, so there is no discrete boundary to translate.",
    "SN 35.204, AN 4.27, AN 7.49, MN 13, and MN 108 ranked only on citations "
    "that turned out to be false, and carry no leverage now that those are "
    "repaired.",
    "MN 77's ten orphans are all kasiṇa records. That is a formula sheet, not "
    "a translation.",
    "The emptiness / signless / wishless cluster reports eleven of thirteen "
    "terms dark, but ten of those are uncited rather than orphaned. No "
    "translation can anchor them until they have verified sources.",
    "Longer one-anchor candidates such as DN 1, DN 21, DN 33, and DN 16 remain "
    "deferred on length.",
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
        "Use the [Wave 11 execution plan](../wave-11-execution-plan.md) for the",
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
    lines.append("")
    if any(item.position == "next" for item in QUEUE):
        lines += [
            "After the last queue item, run a fresh audit rather than extending",
            "this ranking. Every wave so far has found leverage signals that were",
            "wrong until they were checked against the source.",
        ]
    else:
        lines += [
            "**Every item in this queue is published, and there is no next item.**",
            "The next translation task is to run a fresh audit and build a new",
            "queue from it. Do not extend this ranking: it was computed against a",
            "61-surface corpus, and every wave so far has found leverage signals",
            "that were wrong until they were checked against the source.",
        ]
    lines.append("")
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
