#!/usr/bin/env python3
"""Replay git history to record weekly schema and lint failure counts.

CI reports whether the checks pass right now; it keeps no trend. This script
reconstructs one by checking out the last commit of each ISO week into a
temporary worktree and running the two record-level checks against it.

The output is `reviews/check-history.jsonl`, one line per week, which
`scripts/health_dashboard.py` reads. Rewriting the whole file every run keeps
it idempotent: the same repository always produces the same history, so a
re-run after new commits simply extends it.

Counts are failing *records*, not failing runs — a week where one entry broke
the schema and a week where forty did are different facts, and the exit code
alone cannot tell them apart.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from collections import OrderedDict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HISTORY_PATH = REPO_ROOT / "reviews" / "check-history.jsonl"

# Both checkers print one repair block per finding, opening with `- Rule
# violated:` and naming the offending file on the next line. Counting those
# blocks gives findings rather than runs, which is the number worth trending:
# one broken entry and forty broken entries are different weeks.
DIAGNOSTIC_BLOCK = re.compile(r"^\s*[-*]\s+Rule violated:", re.M)
# Older commits predate the repair-diagnostic format and printed a bare
# `- path/to/file.json: message` line per finding instead.
LEGACY_DIAGNOSTIC = re.compile(r"^\s*[-*]\s+\S+\.json\b", re.M)

CHECKS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("schema_failures", ("scripts/validate_terms.py", "--strict")),
    ("lint_failures", ("scripts/lint_terms.py", "--strict")),
)


def git(args: list[str], cwd: Path) -> str:
    result = subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True, check=True
    )
    return result.stdout


def weekly_commits(repo_root: Path = REPO_ROOT) -> "OrderedDict[str, list[tuple[str, str]]]":
    """Group every commit by the ISO week it landed in, oldest first.

    Every commit is measured, not just each week's last one. Sampling only the
    week's tip would miss the most interesting case there is: a failure
    introduced on Tuesday and repaired on Thursday, which is exactly the event
    a failure trend exists to show.

    Weeks with no commits are absent rather than zero-filled. Nothing was
    checked in, so there is no failure count to report.
    """
    # `%x09` is not expanded inside `--date=format:`, it goes to strftime, so
    # the week comes from the configurable `%ad` and the plain date from `%as`.
    log = git(
        ["log", "--reverse", "--format=%H%x09%ad%x09%as", "--date=format:%G-W%V"],
        repo_root,
    )
    weeks: "OrderedDict[str, list[tuple[str, str]]]" = OrderedDict()
    for line in log.splitlines():
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        commit, week, day = parts
        weeks.setdefault(week, []).append((commit, day))
    return weeks


def count_failures(output: str) -> int:
    """Read a finding count out of a checker's output."""
    for pattern in (DIAGNOSTIC_BLOCK, LEGACY_DIAGNOSTIC):
        found = len(pattern.findall(output))
        if found:
            return found
    # A non-zero exit with nothing parseable still means at least one failure.
    # A missing dependency lands here, which is why the replay installs the
    # dev requirements before it starts.
    return 1


def measure_commit(commit: str, worktree: Path, repo_root: Path) -> dict[str, int]:
    git(["checkout", "--quiet", "--detach", commit], worktree)
    counts: dict[str, int] = {}
    for label, command in CHECKS:
        script = worktree / command[0]
        if not script.exists():
            # The check had not been written yet at this point in history.
            counts[label] = 0
            continue
        result = subprocess.run(
            [sys.executable, *command],
            cwd=worktree,
            capture_output=True,
            text=True,
            check=False,
        )
        counts[label] = 0 if result.returncode == 0 else count_failures(result.stdout + result.stderr)
    return counts


def build_history(repo_root: Path = REPO_ROOT, *, limit: int | None = None) -> list[dict[str, object]]:
    weeks = weekly_commits(repo_root)
    if limit is not None:
        weeks = OrderedDict(list(weeks.items())[-limit:])

    rows: list[dict[str, object]] = []
    with tempfile.TemporaryDirectory() as tmpdir:
        worktree = Path(tmpdir) / "replay"
        git(["worktree", "add", "--quiet", "--detach", str(worktree), "HEAD"], repo_root)
        try:
            for week, commits in weeks.items():
                schema = 0
                lint = 0
                broken: list[str] = []
                for commit, _day in commits:
                    counts = measure_commit(commit, worktree, repo_root)
                    # The week's number is its worst commit, not the sum. A
                    # failure that survives five commits is one problem, and
                    # adding it up five times would report it as five.
                    schema = max(schema, counts["schema_failures"])
                    lint = max(lint, counts["lint_failures"])
                    if counts["schema_failures"] or counts["lint_failures"]:
                        broken.append(commit[:12])
                rows.append(
                    {
                        "week": week,
                        "date": commits[-1][1],
                        "commit": commits[-1][0][:12],
                        "commits_checked": len(commits),
                        "commits_failing": len(broken),
                        "schema_failures": schema,
                        "lint_failures": lint,
                        "source": "replay",
                    }
                )
        finally:
            git(["worktree", "remove", "--force", str(worktree)], repo_root)
    return rows


def write_history(rows: list[dict[str, object]], path: Path = HISTORY_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows)
    path.write_text(body, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Replay only the most recent N weeks.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=HISTORY_PATH,
        help="Destination JSONL file.",
    )
    args = parser.parse_args()

    try:
        rows = build_history(limit=args.limit)
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: git failed: {exc.stderr.strip() or exc}")
        return 1

    if not rows:
        print("WARNING: no commits found to replay")
        return 0

    write_history(rows, args.output)
    failing = sum(
        1 for row in rows if row["schema_failures"] or row["lint_failures"]
    )
    print(
        f"Wrote {len(rows)} week(s) to {args.output.relative_to(REPO_ROOT).as_posix()} "
        f"({failing} with a failure)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
