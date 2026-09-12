#!/usr/bin/env python3
"""Validate the human newcomer-review ledger without pretending reviews exist."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

try:
    from scripts.check_readability_reviews import translation_body_sha256
    from scripts.surface_registry import TRANSLATION_SURFACES
except ModuleNotFoundError:
    from check_readability_reviews import translation_body_sha256  # type: ignore[no-redef]
    from surface_registry import TRANSLATION_SURFACES  # type: ignore[no-redef]


REPO_ROOT = Path(__file__).resolve().parent.parent
LEDGER = REPO_ROOT / "reviews" / "newcomer-review-ledger.json"
ALLOWED_STATUS = {"recruiting", "in-review", "ready", "validated"}
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def load_ledger(path: Path = LEDGER) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("ledger must be a JSON object")
    return data


def current_body_hash(surface: Any, repo_root: Path) -> str | None:
    """The hash of the body a reader would be given today, or None if unreadable."""
    main_path = repo_root / surface.main_relpath
    if not main_path.is_file():
        return None
    try:
        return translation_body_sha256(main_path)
    except (OSError, ValueError):
        return None


def count_newcomer_evidence(
    key: str,
    reviews: list[Any],
    body_hash: str | None,
    failures: list[str],
) -> tuple[int, int]:
    """Validate one surface's newcomer reviews and count what still holds.

    Returns (participants who reviewed the current body, independent passes
    among them).

    A review is evidence about one version of one text, so the identity that
    must be unique is the pair (participant, body). Checking the participant
    label alone across the whole history blocked the workflow the protocol
    asks for -- keep the old record, repeat the affected review -- because the
    returning reader collided with their own earlier entry.

    A returning reader still counts as one of the required participants: they
    did read this body. They cannot count toward the independent passes,
    because someone who has already read an earlier draft is no longer giving
    a first unprompted account of it. That is recorded as `follow_up` rather
    than inferred silently, so the ledger says what kind of session it was.
    """
    entries: list[dict[str, Any]] = []
    for index, review in enumerate(reviews, start=1):
        label = f"{key} review {index}"
        if not isinstance(review, dict):
            failures.append(f"{label}: must be an object")
            continue
        participant = review.get("participant")
        if not _nonempty(participant):
            failures.append(f"{label}: participant label is required")
        for field in ("reviewed_on", "what_happened", "practical_point"):
            if not _nonempty(review.get(field)):
                failures.append(f"{label}: {field} is required")
        if _nonempty(review.get("reviewed_on")) and not DATE.match(str(review["reviewed_on"])):
            failures.append(f"{label}: reviewed_on must be YYYY-MM-DD")
        if not isinstance(review.get("independent"), bool) or not isinstance(review.get("pass"), bool):
            failures.append(f"{label}: independent and pass must be booleans")
        follow_up = review.get("follow_up", False)
        if not isinstance(follow_up, bool):
            failures.append(f"{label}: follow_up must be a boolean when present")
            follow_up = False

        # Which body this reader actually read. Recording it is required;
        # matching today's body is what makes the review count. A review of an
        # earlier draft stays in the file as history and simply stops paying
        # toward the threshold.
        recorded = review.get("body_sha256")
        if not _nonempty(recorded) or not SHA256.match(str(recorded)):
            failures.append(f"{label}: body_sha256 of the reviewed text is required")
            continue
        if not _nonempty(participant):
            continue
        entries.append(
            {
                "label": label,
                "order": (str(review.get("reviewed_on") or ""), index),
                "participant": str(participant),
                "body": str(recorded),
                "independent": review.get("independent") is True,
                "passed": review.get("pass") is True,
                "follow_up": follow_up,
            }
        )

    seen: Counter[tuple[str, str]] = Counter()
    for entry in entries:
        seen[(entry["participant"], entry["body"])] += 1
    for (participant, _body), count in sorted(seen.items()):
        if count > 1:
            failures.append(
                f"{key}: duplicate participant {participant} for one body version"
            )

    # Only a *later* session is a follow-up. Asking whether the participant
    # appears anywhere else would flag the original review too, which is the
    # record the protocol asks contributors to keep.
    earlier_bodies: dict[str, set[str]] = defaultdict(set)
    returning_labels: set[str] = set()
    for entry in sorted(entries, key=lambda item: item["order"]):
        if earlier_bodies[entry["participant"]] - {entry["body"]}:
            returning_labels.add(entry["label"])
        earlier_bodies[entry["participant"]].add(entry["body"])

    participants: set[str] = set()
    independent_passes = 0
    for entry in entries:
        returning = entry["label"] in returning_labels
        if returning and not entry["follow_up"]:
            failures.append(
                f"{entry['label']}: {entry['participant']} reviewed another body of this "
                "text; record follow_up: true"
            )
        if not returning and entry["follow_up"]:
            failures.append(
                f"{entry['label']}: follow_up is recorded but this participant has no "
                "review of an earlier body"
            )
        if returning and entry["independent"]:
            failures.append(
                f"{entry['label']}: a returning reader cannot give a first unprompted "
                "reading; record independent: false on a follow-up"
            )
        if body_hash is None or entry["body"] != body_hash:
            continue
        participants.add(entry["participant"])
        if entry["independent"] and entry["passed"] and not returning:
            independent_passes += 1
    return len(participants), independent_passes


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

        # Human evidence is evidence about a *particular text*. The body it
        # was gathered against is recorded with it, so an edit to the
        # translation cannot silently inherit approval from readers who never
        # saw it. Stale evidence is kept as history and simply stops counting.
        body_hash = current_body_hash(by_key[key], repo_root)

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
            if read_aloud_complete:
                recorded = read_aloud.get("body_sha256")
                if not _nonempty(recorded) or not SHA256.match(str(recorded)):
                    failures.append(f"{key}: completed read-aloud needs the body_sha256 it reviewed")
                    read_aloud_complete = False
                elif body_hash is not None and recorded != body_hash:
                    failures.append(
                        f"{key}: read-aloud evidence is for an older body; re-review or reopen the gate"
                    )
                    read_aloud_complete = False

        reviews = record.get("newcomer_reviews")
        if not isinstance(reviews, list):
            failures.append(f"{key}: newcomer_reviews must be a list")
            reviews = []
        current_reviews, independent_passes = count_newcomer_evidence(
            key, reviews, body_hash, failures
        )

        enough_reviews = isinstance(required, int) and current_reviews >= required
        enough_passes = isinstance(passes_required, int) and independent_passes >= passes_required
        ready = fidelity.get("status") == "complete" and read_aloud_complete and enough_reviews and enough_passes
        registry_status = by_key[key].readability_review.status if by_key[key].readability_review else "unreviewed"
        if status in {"ready", "validated"} and not ready:
            failures.append(f"{key}: {status} requires all three evidence gates")
        if registry_status == "validated" and (status != "validated" or not ready):
            failures.append(f"{key}: registry says validated without completed ledger evidence")
        if status == "validated" and registry_status != "validated":
            failures.append(f"{key}: ledger says validated but registry does not")

    # Enforcement used to iterate the cohort alone, so a surface promoted to
    # `validated` in the registry but never added to the cohort escaped the
    # evidence requirement entirely -- the one way to claim validation
    # without any. The registry is where promotion is recorded, so the
    # registry decides who owes evidence, not the list the ledger happens
    # to name.
    for surface in TRANSLATION_SURFACES:
        review = surface.readability_review
        if review is not None and review.status == "validated" and surface.key not in surfaces:
            failures.append(
                f"{surface.key}: registry says validated but the ledger has no record for it"
            )
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
