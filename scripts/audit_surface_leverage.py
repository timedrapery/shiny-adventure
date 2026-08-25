#!/usr/bin/env python3
"""Rank untranslated suttas by how much governed vocabulary they would anchor.

This is the audit method described in docs/next-suttas-roadmap.md, made
reproducible. It exists because the ranking has now been wrong twice in the
same way, and each correction was recomputed by hand.

The measure is deliberately not raw citation count. An entry is an ORPHAN when
every sutta it cites is untranslated, so no existing surface shows its policy
in running text. Ranking by orphans rather than by citations was the Wave 6
correction.

The Wave 7 correction is that orphan count is not leverage either when the
anchoring text is a bare enumeration. A sutta whose whole body is "there are
four X; what four; A, B, C, D; these are the four" scores well per word while
demonstrating nothing a cluster sheet could not state. Those are reported
separately rather than silently ranked at the top.

Pali word counts come from .bilara-cache when the root text is present. Texts
that are not cached are reported as unverified rather than guessed.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

try:
    from scripts.surface_registry import TRANSLATION_SURFACES
    from scripts.term_store import iter_term_files
    from scripts.text_utils import safe_text
except ModuleNotFoundError:
    from surface_registry import TRANSLATION_SURFACES
    from term_store import iter_term_files
    from text_utils import safe_text


REPO_ROOT = Path(__file__).resolve().parent.parent
TERMS_DIR = REPO_ROOT / "terms"
BILARA_CACHE = REPO_ROOT / ".bilara-cache"

# Below this many Pali words a discourse is a bare enumeration rather than a
# text that shows its vocabulary in use. Calibrated against the SN 45 Oghavagga
# repetition suttas (30-35 words) and AN 7.11 (18 words), all of which are a
# title, a count, a list, and a restatement of the count.
ENUMERATION_STUB_MAX_WORDS = 80

# Length is a useful warning, not a definition. AN 2.9 is only 63 substantive
# Pali words, but it contains a counterfactual social argument and a simile --
# not merely a count, list, and restatement. Keep known short substantive texts
# out of the enumeration-only track.
SUBSTANTIVE_SHORT_TEXTS = frozenset({"AN 2.9"})


@dataclass
class SuttaLeverage:
    sutta: str
    orphan_majors: list[str] = field(default_factory=list)
    orphan_minors: list[str] = field(default_factory=list)
    citing_entries: int = 0
    pali_words: int | None = None

    @property
    def orphan_total(self) -> int:
        return len(self.orphan_majors) + len(self.orphan_minors)

    @property
    def is_enumeration_stub(self) -> bool:
        return (
            self.pali_words is not None
            and self.pali_words <= ENUMERATION_STUB_MAX_WORDS
            and self.sutta not in SUBSTANTIVE_SHORT_TEXTS
        )

    @property
    def length_note(self) -> str:
        if self.pali_words is None:
            return "unverified (not cached)"
        if self.is_enumeration_stub:
            return f"{self.pali_words}w enumeration stub"
        if self.pali_words < 250:
            return f"{self.pali_words}w short"
        return f"{self.pali_words}w full"


def translated_suttas() -> set[str]:
    return {surface.label.strip() for surface in TRANSLATION_SURFACES}


def cache_key(sutta: str) -> str:
    return sutta.lower().replace(" ", "") + "_root-pli-ms.json"


@lru_cache(maxsize=1)
def bundled_cache_index() -> dict[str, Path]:
    """Map every cached Bilara sutta UID to the file that contains it.

    Most root texts have one file per discourse. Some collections, especially
    AN 2, bundle several discourses into files such as
    ``an2.1-10_root-pli-ms.json``. Looking only for an exact filename made the
    audit call AN 2.9 uncached, and an earlier manual check then counted the
    entire bundle as though it were one discourse.
    """
    index: dict[str, Path] = {}
    for path in sorted(BILARA_CACHE.glob("*_root-pli-ms.json")):
        try:
            with path.open("r", encoding="utf-8") as handle:
                segments = json.load(handle)
        except (OSError, json.JSONDecodeError):
            continue
        for segment_id in segments:
            uid, separator, _ = str(segment_id).partition(":")
            if separator:
                index.setdefault(uid, path)
    return index


def cache_path(sutta: str) -> Path | None:
    """Return the exact or bundled cache path for a display reference."""
    exact = BILARA_CACHE / cache_key(sutta)
    if exact.exists():
        return exact
    uid = sutta.lower().replace(" ", "")
    return bundled_cache_index().get(uid)


def pali_word_count(sutta: str) -> int | None:
    """Body word count from the cached root text, or None when not cached.

    Front-matter counters beginning with `0.` and bundled-discourse title
    counters ending with `.0` are excluded so short texts are not inflated.
    """
    path = cache_path(sutta)
    if path is None:
        return None
    try:
        with path.open("r", encoding="utf-8") as handle:
            segments = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return None
    total = 0
    target_uid = sutta.lower().replace(" ", "")
    for segment_id, text in segments.items():
        uid, _, counter = segment_id.partition(":")
        if uid != target_uid:
            continue
        if counter.startswith("0.") or counter.endswith(".0"):
            continue
        total += len(str(text).split())
    return total


def load_entries(terms_dir: Path = TERMS_DIR) -> list[dict[str, object]]:
    entries = []
    for path in iter_term_files(terms_dir):
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        refs = [str(ref).strip() for ref in (data.get("sutta_references") or [])]
        entries.append(
            {
                "name": data.get("normalized_term") or data.get("term"),
                "kind": data.get("entry_type", "minor"),
                "refs": refs,
            }
        )
    return entries


def build_leverage(
    entries: list[dict[str, object]], translated: set[str]
) -> dict[str, SuttaLeverage]:
    leverage: dict[str, SuttaLeverage] = defaultdict(
        lambda: SuttaLeverage(sutta="")
    )
    for entry in entries:
        refs = entry["refs"]
        if not refs:
            continue
        is_orphan = not (set(refs) & translated)
        for ref in refs:
            if ref in translated:
                continue
            row = leverage[ref]
            row.sutta = ref
            row.citing_entries += 1
            if is_orphan:
                if entry["kind"] == "major":
                    row.orphan_majors.append(str(entry["name"]))
                else:
                    row.orphan_minors.append(str(entry["name"]))
    for sutta, row in leverage.items():
        row.pali_words = pali_word_count(sutta)
    return dict(leverage)


def summarize(entries: list[dict[str, object]], translated: set[str]) -> dict[str, int]:
    cited = [e for e in entries if e["refs"]]
    orphans = [e for e in cited if not (set(e["refs"]) & translated)]
    return {
        "surfaces": len(translated),
        "terms": len(entries),
        "cited": len(cited),
        "anchored": len(cited) - len(orphans),
        "orphans": len(orphans),
        "orphan_majors": len([e for e in orphans if e["kind"] == "major"]),
        "uncited": len(entries) - len(cited),
    }


def rank(rows: list[SuttaLeverage]) -> list[SuttaLeverage]:
    """Rank substantive candidates: pressure on policy-bearing majors first."""
    return sorted(
        rows,
        key=lambda r: (-len(r.orphan_majors), -r.orphan_total, -r.citing_entries, r.sutta),
    )


def rank_stubs(rows: list[SuttaLeverage]) -> list[SuttaLeverage]:
    """Rank enumeration stubs by sheer coverage.

    A bare list demonstrates nothing in context, so the major/minor split
    carries little weight here. What matters is how many governed records the
    list would take out of orphan state at all.
    """
    return sorted(rows, key=lambda r: (-r.orphan_total, r.sutta))


def print_report(
    summary: dict[str, int], leverage: dict[str, SuttaLeverage], top: int
) -> None:
    print("Surface Leverage Audit")
    print(f"- Translation surfaces: {summary['surfaces']}")
    print(f"- Term records: {summary['terms']}")
    print(f"- Cited: {summary['cited']} (anchored {summary['anchored']}, orphan {summary['orphans']})")
    print(f"- Orphan majors: {summary['orphan_majors']}")
    print(f"- Uncited: {summary['uncited']}")
    print()

    rows = [r for r in leverage.values() if r.orphan_total]
    substantive = rank([r for r in rows if not r.is_enumeration_stub])
    stubs = rank_stubs([r for r in rows if r.is_enumeration_stub])

    print("Ranked Candidates (substantive texts)")
    if not substantive:
        print("- None")
    for row in substantive[:top]:
        majors = ", ".join(safe_text(name) for name in sorted(row.orphan_majors))
        print(
            f"- {safe_text(row.sutta)}: {len(row.orphan_majors)} orphan major(s), "
            f"{row.orphan_total} orphan total, {row.length_note}"
            + (f"; majors: {majors}" if majors else "")
        )
    print()

    print("Enumeration Stubs (high orphan count, bare list text)")
    print("  Treat as formula or cluster-sheet work, not as translation surfaces.")
    if not stubs:
        print("- None")
    for row in stubs[:top]:
        print(
            f"- {safe_text(row.sutta)}: {row.orphan_total} orphan(s), {row.length_note}"
        )
    print()

    unverified = sorted(
        (r for r in rows if r.pali_words is None), key=lambda r: -r.orphan_total
    )
    print("Unverified Length (root text not in .bilara-cache)")
    if not unverified:
        print("- None")
    for row in unverified[:top]:
        print(f"- {safe_text(row.sutta)}: {row.orphan_total} orphan(s)")


@dataclass
class ClusterCoverage:
    label: str
    shown: int = 0
    orphan: int = 0
    uncited: int = 0
    anchors: dict[str, int] = field(default_factory=dict)

    @property
    def total(self) -> int:
        return self.shown + self.orphan + self.uncited

    enumeration_only: int = 0

    @property
    def dark(self) -> int:
        """Terms with no running-text demonstration anywhere.

        Orphan percentage alone understates this. An uncited term is not an
        orphan -- it has no anchors to be untranslated -- but it is equally
        invisible in running text, so both count as dark.

        Note that dark deliberately does NOT mean "unpublished". Every term a
        cluster declares is rendered in its generated glossary, so the policy
        is always reachable. Dark means the term has never been shown at work
        in a sentence, which is what a translation surface adds and a table
        cannot.
        """
        return self.orphan + self.uncited

    @property
    def dark_reachable(self) -> int:
        """Dark terms a substantive text could still rescue.

        The rest are anchored only to enumeration stubs, so no honest
        translation would ever demonstrate them in context. Separating the two
        keeps the ranking pointed at work that translation can actually do.
        """
        return self.dark - self.enumeration_only

    @property
    def dark_pct(self) -> float:
        return 100.0 * self.dark / self.total if self.total else 0.0


def cluster_members(cluster) -> list[str]:
    """Read a cluster report's declared term list without running the report."""
    import importlib

    dotted = cluster.script_relpath.replace("/", ".").removesuffix(".py")
    # Run as `python scripts/audit_surface_leverage.py`, sys.path[0] is scripts/
    # and the `scripts.` package prefix does not resolve; run as a module from
    # the repo root, the bare name does not. Try both rather than silently
    # reporting every cluster as empty.
    module = None
    for module_name in (dotted, dotted.rpartition(".")[2]):
        try:
            module = importlib.import_module(module_name)
            break
        except Exception:
            continue
    if module is None:
        return []
    members: list[str] = []
    for attr in (
        "HEADWORD_TERMS",
        "SUPPORTING_TERMS",
        "CLUSTER_TERMS",
        "TERMS",
        "CORE_TERMS",
        "HEADWORDS",
    ):
        value = getattr(module, attr, None)
        if isinstance(value, (list, tuple)):
            members += [item for item in value if isinstance(item, str)]
    return sorted(set(members))


def build_cluster_coverage(
    entries: list[dict[str, object]], translated: set[str]
) -> list[ClusterCoverage]:
    try:
        from scripts.cluster_registry import CLUSTER_SURFACES
    except ModuleNotFoundError:
        from cluster_registry import CLUSTER_SURFACES

    by_name = {entry["name"]: entry for entry in entries}
    rows = []
    for cluster in CLUSTER_SURFACES:
        members = cluster_members(cluster)
        if not members:
            continue
        row = ClusterCoverage(label=cluster.label)
        for member in members:
            entry = by_name.get(member)
            if entry is None:
                continue
            refs = entry["refs"]
            if not refs:
                row.uncited += 1
            elif set(refs) & translated:
                row.shown += 1
            else:
                row.orphan += 1
                untranslated = [r for r in refs if r not in translated]
                for ref in untranslated:
                    row.anchors[ref] = row.anchors.get(ref, 0) + 1
                # A term anchored only to enumeration stubs cannot be rescued
                # by any honest translation, so it is dark for good.
                if untranslated and all(
                    (w := pali_word_count(r)) is not None
                    and w <= ENUMERATION_STUB_MAX_WORDS
                    for r in untranslated
                ):
                    row.enumeration_only += 1
        if row.total:
            rows.append(row)
    rows.sort(key=lambda r: (-r.dark_pct, -r.dark, r.label))
    return rows


def print_cluster_coverage(rows: list[ClusterCoverage], top: int) -> None:
    print("Governed Cluster Coverage (factor 4: drift reduction)")
    print("  dark = governed terms with no running-text demonstration anywhere.")
    shown_any = False
    for row in rows[:top]:
        if not row.dark:
            continue
        shown_any = True
        anchors = sorted(row.anchors.items(), key=lambda kv: (-kv[1], kv[0]))[:3]
        anchor_text = ", ".join(f"{name}({count})" for name, count in anchors)
        stuck = (
            f", {row.enumeration_only} enumeration-only"
            if row.enumeration_only
            else ""
        )
        print(
            f"- {safe_text(row.label)}: {row.dark}/{row.total} dark "
            f"({row.dark_pct:.0f}%) -- {row.dark_reachable} reachable by a real "
            f"text{stuck}; orphan {row.orphan}, uncited {row.uncited}"
            + (f"; anchors: {anchor_text}" if anchor_text else "")
        )
    if not shown_any:
        print("- None")
    print()


def build_payload(
    summary: dict[str, int], leverage: dict[str, SuttaLeverage]
) -> dict[str, object]:
    rows = [r for r in leverage.values() if r.orphan_total]
    return {
        "summary": summary,
        "candidates": [
            {
                "sutta": r.sutta,
                "orphan_majors": sorted(r.orphan_majors),
                "orphan_minors": sorted(r.orphan_minors),
                "orphan_total": r.orphan_total,
                "citing_entries": r.citing_entries,
                "pali_words": r.pali_words,
                "enumeration_stub": r.is_enumeration_stub,
            }
            for r in rank(rows)
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--top",
        type=int,
        default=15,
        help="Number of candidates to show in each section.",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    if not TERMS_DIR.exists():
        print(f"ERROR: Terms directory not found: {TERMS_DIR}")
        return 1

    entries = load_entries()
    if not entries:
        print("WARNING: No term files found in terms/")
        return 0

    translated = translated_suttas()
    summary = summarize(entries, translated)
    leverage = build_leverage(entries, translated)

    clusters = build_cluster_coverage(entries, translated)

    if args.format == "json":
        payload = build_payload(summary, leverage)
        payload["clusters"] = [
            {
                "label": c.label,
                "shown": c.shown,
                "orphan": c.orphan,
                "uncited": c.uncited,
                "dark": c.dark,
                "dark_reachable": c.dark_reachable,
                "enumeration_only": c.enumeration_only,
                "dark_pct": round(c.dark_pct, 1),
                "anchors": c.anchors,
            }
            for c in clusters
        ]
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print_report(summary, leverage, args.top)
        print_cluster_coverage(clusters, args.top)
    return 0


if __name__ == "__main__":
    sys.exit(main())
