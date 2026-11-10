#!/usr/bin/env python3
"""Bring every derived file back in step after a translation or term change.

Changing one translation body used to mean hand-editing a hash table, then
running some thirty generator commands in the right order, and nothing told
you which you had missed until the full suite failed one check at a time.
This script is that procedure, in one place:

    python scripts/refresh_derived.py            report stale body versions
    python scripts/refresh_derived.py --write    refresh everything derived

`--write` does, in order:

1. Body versions. Recompute each translation body's SHA-256 and, where it
   differs from `reviews/body-versions.json`, record the new hash and today's
   date together. The date is the day the text was last revised; it is never
   a claim that anyone reviewed it.
2. Passage identifiers, the reader's edition, every registered generated
   document, the term indexes, and the translation index.

What it deliberately does not touch: the newcomer review ledger. Human review
evidence is bound to the body hash it was gathered against, so a changed body
leaves that evidence pointing at a text that is no longer published. The
script names every surface in that position and stops there. Reopening a gate
is an editorial act that a person records, with a reason; see
`docs/newcomer-review-protocol.md`.

It does not run the verification suite either. Follow it with
`python scripts/run_checks.py`.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

try:
    from scripts.check_readability_reviews import translation_body_sha256
    from scripts.surface_registry import (
        BODY_VERSIONS_RELPATH,
        CLUSTER_SURFACES,
        NON_CLUSTER_GENERATED_SURFACES,
        REPO_ROOT,
        TRANSLATION_SURFACES,
        TranslationSurface,
    )
except ModuleNotFoundError:
    from check_readability_reviews import translation_body_sha256
    from surface_registry import (
        BODY_VERSIONS_RELPATH,
        CLUSTER_SURFACES,
        NON_CLUSTER_GENERATED_SURFACES,
        REPO_ROOT,
        TRANSLATION_SURFACES,
        TranslationSurface,
    )


LEDGER_RELPATH = "reviews/newcomer-review-ledger.json"

# The generators that are not registered report scripts. Order matters: the
# reader embeds the passage identifiers, so the maps are realigned first.
PRE_REPORT_COMMANDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("Passage identifiers", ("scripts/paragraph_ids.py", "--write")),
    ("Reader's edition", ("scripts/generate_reader.py", "--write")),
)
POST_REPORT_COMMANDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("Term indexes", ("scripts/term_directory_navigation.py", "--write-docs")),
    ("Translation index", ("scripts/translation_surface_index.py", "--write-docs")),
)
CLUSTER_WRITE_FLAG = "--write-docs"
NON_CLUSTER_WRITE_FLAG = "--write"


def stale_body_versions(
    surfaces: tuple[TranslationSurface, ...] = TRANSLATION_SURFACES,
    repo_root: Path = REPO_ROOT,
    versions_path: Path | None = None,
) -> dict[str, tuple[str | None, str]]:
    """Return {surface key: (recorded hash or None, actual hash)} where they differ."""

    path = versions_path or (repo_root / BODY_VERSIONS_RELPATH)
    recorded = json.loads(path.read_text(encoding="utf-8")).get("surfaces", {})
    stale: dict[str, tuple[str | None, str]] = {}
    for surface in surfaces:
        actual = translation_body_sha256(repo_root / surface.main_relpath)
        record = recorded.get(surface.key)
        old = record.get("body_sha256") if isinstance(record, dict) else None
        if old != actual:
            stale[surface.key] = (old, actual)
    return stale


def write_body_versions(
    stale: dict[str, tuple[str | None, str]],
    today: str,
    surfaces: tuple[TranslationSurface, ...] = TRANSLATION_SURFACES,
    repo_root: Path = REPO_ROOT,
    versions_path: Path | None = None,
) -> None:
    """Record each stale surface's new hash and revision date in one write.

    Surfaces whose body did not change keep their date. Records for surfaces
    that are no longer registered are dropped, and the file is written in
    registry order so a diff shows only what changed.
    """

    path = versions_path or (repo_root / BODY_VERSIONS_RELPATH)
    data = json.loads(path.read_text(encoding="utf-8"))
    recorded = data.get("surfaces", {})
    ordered: dict[str, dict[str, str]] = {}
    for surface in surfaces:
        if surface.key in stale:
            ordered[surface.key] = {
                "body_sha256": stale[surface.key][1],
                "revised_on": today,
            }
        else:
            ordered[surface.key] = recorded[surface.key]
    data["surfaces"] = ordered
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def orphaned_evidence(
    stale: dict[str, tuple[str | None, str]],
    repo_root: Path = REPO_ROOT,
    ledger_path: Path | None = None,
) -> list[str]:
    """Describe ledger evidence bound to a body that `stale` says has changed.

    This only reads the ledger. The evidence is not wrong, it is about an
    older text, and whether to reassess the changed lines or redo the review
    is not something a script can decide.
    """

    path = ledger_path or (repo_root / LEDGER_RELPATH)
    if not path.is_file():
        return []
    records = json.loads(path.read_text(encoding="utf-8")).get("surfaces", {})
    findings: list[str] = []
    for key, (old_hash, _new_hash) in stale.items():
        record = records.get(key)
        if not isinstance(record, dict) or old_hash is None:
            continue
        fidelity = record.get("source_fidelity", {})
        if fidelity.get("status") == "complete" and fidelity.get("body_sha256") == old_hash:
            findings.append(f"{key}: source-fidelity sign-off")
        read_aloud = record.get("human_read_aloud", {})
        if read_aloud.get("status") == "complete" and read_aloud.get("body_sha256") == old_hash:
            findings.append(f"{key}: read-aloud review")
        bound = [
            review
            for review in record.get("newcomer_reviews", [])
            if isinstance(review, dict) and review.get("body_sha256") == old_hash
        ]
        if bound:
            findings.append(f"{key}: {len(bound)} newcomer review(s)")
    return findings


def generator_commands() -> list[tuple[str, tuple[str, ...]]]:
    """Every generator, in the order it has to run."""

    commands = list(PRE_REPORT_COMMANDS)
    seen: set[str] = set()
    for cluster in CLUSTER_SURFACES:
        if cluster.script_relpath not in seen:
            seen.add(cluster.script_relpath)
            commands.append((cluster.label, (cluster.script_relpath, CLUSTER_WRITE_FLAG)))
    commands.extend(POST_REPORT_COMMANDS)
    # The dashboard and the priority table count the corpus, so they go last.
    for surface in NON_CLUSTER_GENERATED_SURFACES:
        commands.append((surface.label, (surface.script_relpath, NON_CLUSTER_WRITE_FLAG)))
    return commands


def run_generators(repo_root: Path = REPO_ROOT) -> list[str]:
    """Run every generator in a fresh interpreter. Return the labels that failed."""

    failed: list[str] = []
    for label, arguments in generator_commands():
        # A fresh process each time: the registry reads the body versions at
        # import, and this process imported it before they were rewritten.
        result = subprocess.run(
            [sys.executable, *arguments],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            failed.append(label)
            print(f"  FAILED  {label}: {' '.join(arguments)}")
            detail = (result.stderr or result.stdout).strip().splitlines()
            for line in detail[-6:]:
                print(f"          {line}")
        else:
            print(f"  ok      {label}")
    return failed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--write",
        action="store_true",
        help="Record changed body versions and regenerate every derived file.",
    )
    args = parser.parse_args()

    stale = stale_body_versions()
    if stale:
        print(f"Translation bodies changed since their version was recorded ({len(stale)}):")
        for key in stale:
            print(f"  {key}")
    else:
        print("Every recorded body version matches its translation.")

    orphans = orphaned_evidence(stale)
    if orphans:
        print(
            "\nHuman review evidence in the ledger is bound to the previous body of:"
        )
        for finding in orphans:
            print(f"  {finding}")
        print(
            "That evidence no longer covers the published text. This script does not\n"
            f"edit {LEDGER_RELPATH}. Either restore the reviewed wording, or reopen\n"
            "each gate by hand with a reason (docs/newcomer-review-protocol.md)."
        )

    if not args.write:
        if stale:
            print("\nRun `python scripts/refresh_derived.py --write` to refresh.")
            return 1
        return 0

    if stale:
        today = date.today().isoformat()
        write_body_versions(stale, today)
        print(f"\nRecorded {len(stale)} new body version(s), revised on {today}.")

    print("\nRegenerating derived files:")
    failed = run_generators()
    if failed:
        print(f"\n{len(failed)} generator(s) failed; fix them and run this again.")
        return 1
    print("\nDone. Now run `python scripts/run_checks.py`.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
