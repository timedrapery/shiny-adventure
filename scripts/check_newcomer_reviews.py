#!/usr/bin/env python3
"""Validate the human newcomer-review ledger without pretending reviews exist."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    from scripts.surface_registry import TRANSLATION_SURFACES
except ModuleNotFoundError:
    from surface_registry import TRANSLATION_SURFACES  # type: ignore[no-redef]


REPO_ROOT = Path(__file__).resolve().parent.parent
LEDGER = REPO_ROOT / "reviews" / "newcomer-review-ledger.json"
ALLOWED_STATUS = {"recruiting", "in-review", "ready", "validated"}
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def load_ledger(path: Path = LEDGER) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("ledger must be a JSON object")
    return data


def collect_failures(data: dict[str, Any], repo_root: Path = REPO_ROOT) -> list[str]:
    failures: list[str] = []
    by_key = {surface.key: surface for surface in TRANSLATION_SURFACES}
    threshold = data.get("threshold")
    if not isinstance(threshold, dict):
        return ["threshold must be an object"]
    required = threshold.get("participants_required")
    passes_required = threshold.get("independent_passes_required")
    if not isinstance(required, int) or required < 1:
        failures.append("participants_required must be a positive integer")
    if not isinstance(passes_required, int) or not isinstance(required, int) or not 1 <= passes_required <= required:
        failures.append("independent_passes_required must be between 1 and participants_required")

    cohort = data.get("cohort")
    surfaces = data.get("surfaces")
    if not isinstance(cohort, list) or not cohort or any(not _nonempty(key) for key in cohort):
        return failures + ["cohort must be a non-empty list of surface keys"]
    if len(set(cohort)) != len(cohort):
        failures.append("cohort contains duplicate surface keys")
    if not isinstance(surfaces, dict):
        return failures + ["surfaces must be an object"]
    if set(surfaces) != set(cohort):
        failures.append("surfaces must cover the cohort exactly")

    for key in cohort:
        if key not in by_key:
            failures.append(f"{key}: not a registered translation surface")
            continue
        record = surfaces.get(key)
        if not isinstance(record, dict):
            failures.append(f"{key}: review record must be an object")
            continue
        status = record.get("status")
        if status not in ALLOWED_STATUS:
            failures.append(f"{key}: unsupported status {status!r}")

        fidelity = record.get("source_fidelity")
        if not isinstance(fidelity, dict) or fidelity.get("status") not in {"pending", "complete"}:
            failures.append(f"{key}: source_fidelity needs pending/complete status")
        elif fidelity.get("status") == "complete":
            evidence = fidelity.get("evidence")
            if not _nonempty(evidence) or not (repo_root / str(evidence)).is_file():
                failures.append(f"{key}: source-fidelity evidence file is missing")
            if not _nonempty(fidelity.get("completed_on")) or not DATE.match(str(fidelity.get("completed_on"))):
                failures.append(f"{key}: source-fidelity completion date is invalid")

        read_aloud = record.get("human_read_aloud")
        if not isinstance(read_aloud, dict) or read_aloud.get("status") not in {"pending", "complete"}:
            failures.append(f"{key}: human_read_aloud needs pending/complete status")
            read_aloud_complete = False
        else:
            reviewers = read_aloud.get("reviewers")
            if not isinstance(reviewers, list):
                failures.append(f"{key}: human_read_aloud.reviewers must be a list")
                reviewers = []
            read_aloud_complete = read_aloud.get("status") == "complete"
            if read_aloud_complete and not reviewers:
                failures.append(f"{key}: completed read-aloud gate needs evidence")

        reviews = record.get("newcomer_reviews")
        if not isinstance(reviews, list):
            failures.append(f"{key}: newcomer_reviews must be a list")
            reviews = []
        participants: set[str] = set()
        independent_passes = 0
        for index, review in enumerate(reviews, start=1):
            label = f"{key} review {index}"
            if not isinstance(review, dict):
                failures.append(f"{label}: must be an object")
                continue
            participant = review.get("participant")
            if not _nonempty(participant):
                failures.append(f"{label}: participant label is required")
            elif str(participant) in participants:
                failures.append(f"{key}: duplicate participant {participant}")
            else:
                participants.add(str(participant))
            for field in ("reviewed_on", "what_happened", "practical_point"):
                if not _nonempty(review.get(field)):
                    failures.append(f"{label}: {field} is required")
            if _nonempty(review.get("reviewed_on")) and not DATE.match(str(review["reviewed_on"])):
                failures.append(f"{label}: reviewed_on must be YYYY-MM-DD")
            if not isinstance(review.get("independent"), bool) or not isinstance(review.get("pass"), bool):
                failures.append(f"{label}: independent and pass must be booleans")
            if review.get("independent") is True and review.get("pass") is True:
                independent_passes += 1

        enough_reviews = isinstance(required, int) and len(reviews) >= required
        enough_passes = isinstance(passes_required, int) and independent_passes >= passes_required
        ready = fidelity.get("status") == "complete" and read_aloud_complete and enough_reviews and enough_passes
        registry_status = by_key[key].readability_review.status if by_key[key].readability_review else "unreviewed"
        if status in {"ready", "validated"} and not ready:
            failures.append(f"{key}: {status} requires all three evidence gates")
        if registry_status == "validated" and (status != "validated" or not ready):
            failures.append(f"{key}: registry says validated without completed ledger evidence")
        if status == "validated" and registry_status != "validated":
            failures.append(f"{key}: ledger says validated but registry does not")
    return failures


def main() -> int:
    try:
        data = load_ledger()
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Newcomer review ledger is invalid: {error}")
        return 1
    failures = collect_failures(data)
    if failures:
        print("Newcomer review ledger check failed:\n")
        for failure in failures:
            print(f"- {failure}")
        return 1
    completed = sum(len(record["newcomer_reviews"]) for record in data["surfaces"].values())
    print(f"Newcomer review ledger passed ({len(data['cohort'])} surfaces; {completed} participant reviews recorded).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
