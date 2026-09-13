#!/usr/bin/env python3
"""Stage a reviewed formal-session export into the newcomer review ledger.

The feedback service exports one formal session as ledger-shaped records
(`python -m feedback_service export-session`). This script is the checked
path from that file into `reviews/newcomer-review-ledger.json`:

- it refuses anything that is not a formal-session export;
- it checks every record's fields against the ledger contract;
- it says which records will count toward the threshold (those whose body
  hash is the current translation body) and which are staged as history;
- it keeps a returning reader's ledger identity and stages them as a
  follow-up (`independent: false`), which the checker counts as a
  participant and never as an independent pass;
- it leaves responses to draft question sets out unless an editor accepts
  them explicitly, and records that acceptance;
- with `--write`, it appends the records and re-runs the ledger check before
  saving, so a file that would fail `check_newcomer_reviews.py` is never
  written.

It never changes a surface's readability status. Promotion to `validated`
stays the two-key operation described in docs/newcomer-review-protocol.md.

    python scripts/stage_feedback_evidence.py --export session.json
    python scripts/stage_feedback_evidence.py --export session.json --write
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    from scripts.check_newcomer_reviews import LEDGER, collect_failures, load_ledger
    from scripts.check_readability_reviews import translation_body_sha256
    from scripts.surface_registry import REPO_ROOT, TRANSLATION_SURFACES
except ModuleNotFoundError:  # invoked as a script from the repo root
    from check_newcomer_reviews import LEDGER, collect_failures, load_ledger  # type: ignore[no-redef]
    from check_readability_reviews import translation_body_sha256  # type: ignore[no-redef]
    from surface_registry import REPO_ROOT, TRANSLATION_SURFACES  # type: ignore[no-redef]


SHA256 = re.compile(r"^[0-9a-f]{64}$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LEDGER_FIELDS = (
    "participant", "reviewed_on", "independent", "what_happened", "practical_point",
    "confusing_words", "pass", "body_sha256",
)


class StagingError(ValueError):
    pass


def load_export(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("export_kind") != "formal-session-review":
        raise StagingError("not a formal-session export (public feedback is never staged as evidence)")
    if data.get("export_format") != 1:
        raise StagingError("unsupported export format")
    if not isinstance(data.get("session"), dict) or not isinstance(data.get("records"), list):
        raise StagingError("export is missing its session or records")
    return data


def stage(
    export_data: dict[str, Any],
    ledger: dict[str, Any],
    *,
    accept_draft_questions: bool = False,
) -> tuple[list[dict[str, Any]], list[str]]:
    """Return ledger records to append and human-readable notes.

    Participant identity is preserved across sessions: a returning reader is
    staged under the label of their earlier ledger record with `follow_up:
    true` and `independent: false`, which is what the ledger checker counts
    as one participant and never as an independent pass. A fresh reader may
    not reuse a label already in the ledger.

    Responses to a question set still marked `draft` are exploratory. They
    are left out unless an editor accepts them with `accept_draft_questions`,
    and the acceptance is recorded on the staged record.
    """
    session = export_data["session"]
    key = session.get("surface_key")
    by_key = {surface.key: surface for surface in TRANSLATION_SURFACES}
    if key not in by_key:
        raise StagingError(f"{key!r} is not a registered translation surface")
    surfaces = ledger.get("surfaces", {})
    if key not in surfaces:
        raise StagingError(f"{key} is not in the ledger cohort; add it there first")
    current_hash = translation_body_sha256(by_key[key].main_path)
    existing = [r for r in surfaces[key].get("newcomer_reviews", []) if isinstance(r, dict)]
    known_labels = {str(r.get("participant")) for r in existing}
    staged_ids = {
        r.get("evidence_source", {}).get("submission_id")
        for r in existing if isinstance(r.get("evidence_source"), dict)
    }
    notes: list[str] = []
    records: list[dict[str, Any]] = []
    for index, item in enumerate(export_data["records"], start=1):
        label = f"record {index}"
        if not isinstance(item, dict):
            raise StagingError(f"{label}: must be an object")
        for field in ("participant", "reviewed_on", "what_happened", "practical_point", "body_sha256"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                raise StagingError(f"{label}: {field} is required")
        if not DATE.match(item["reviewed_on"]):
            raise StagingError(f"{label}: reviewed_on must be YYYY-MM-DD")
        if not SHA256.match(item["body_sha256"]):
            raise StagingError(f"{label}: body_sha256 must be a lowercase SHA-256")
        if not isinstance(item.get("independent"), bool) or not isinstance(item.get("pass"), bool):
            raise StagingError(f"{label}: independent and pass must be booleans")
        if item.get("assessment") not in {"pass", "fail", "unclear"}:
            raise StagingError(f"{label}: only assessed responses can be staged")
        if item.get("submission_id") in staged_ids:
            notes.append(f"{label}: submission {item['submission_id']} is already in the ledger; skipped")
            continue
        confusing = item.get("confusing_words", [])
        if not isinstance(confusing, list) or any(not isinstance(c, str) for c in confusing):
            raise StagingError(f"{label}: confusing_words must be a list of strings")

        status = item.get("question_editorial_status")
        if status != "approved" and not accept_draft_questions:
            notes.append(
                f"{item['participant']}: answered a {status or 'unreviewed'} question set "
                f"(v{item.get('question_version')}); kept as exploratory evidence in the "
                "service, not staged. Re-run with --accept-draft-questions once an editor "
                "has decided those questions can carry formal weight."
            )
            continue

        kind = item.get("participant_kind", "fresh")
        returning = item.get("returning_from") or {}
        if kind == "returning":
            name = str(returning.get("participant") or item["participant"])
            if name not in known_labels:
                raise StagingError(
                    f"{label}: returning reader {name} has no earlier record in the ledger "
                    "for this text; stage the earlier session first or mark them fresh"
                )
            independent = False
            follow_up = True
            if item["independent"]:
                notes.append(f"{name}: export marked a returning reader independent; staged as independent: false")
        else:
            name = item["participant"]
            if name in known_labels:
                raise StagingError(
                    f"{label}: label {name} already exists in the ledger for this text; "
                    "mark the participant as returning or use a new label"
                )
            independent = item["independent"]
            follow_up = False
        known_labels.add(name)

        record = {
            "participant": name,
            "reviewed_on": item["reviewed_on"],
            "independent": independent,
            "follow_up": follow_up,
            "what_happened": item["what_happened"],
            "practical_point": item["practical_point"],
            "confusing_words": confusing,
            "pass": item["pass"],
            "body_sha256": item["body_sha256"],
            "evidence_source": {
                "kind": "reader-feedback-session",
                "session": session["code"],
                "submission_id": item.get("submission_id"),
                "session_label": item["participant"],
                "participant_kind": kind,
                "returning_from": item.get("returning_from"),
                "familiarity": item.get("familiarity"),
                "question_version": item.get("question_version"),
                "question_set_sha256": item.get("question_set_sha256"),
                "question_editorial_status": status,
                "draft_questions_accepted_by_editor": status != "approved",
                "assessment": item.get("assessment"),
            },
        }
        counts = item["body_sha256"] == current_hash
        role = "follow-up (counts as a participant, never as an independent pass)" if follow_up else "fresh"
        version = "current body" if counts else "older body; history only, does not count"
        notes.append(f"{name}: {role}, pass={item['pass']}, {version}")
        if status != "approved":
            notes.append(f"{name}: staged from a DRAFT question set on editor acceptance; recorded on the record")
        records.append(record)
    if export_data.get("excluded"):
        notes.append(f"{len(export_data['excluded'])} response(s) were excluded by the service export "
                     "(not assessed, duplicates, or independence not recorded); see the export file")
    return records, notes


def apply(ledger: dict[str, Any], key: str, records: list[dict[str, Any]]) -> dict[str, Any]:
    updated = json.loads(json.dumps(ledger))
    updated["surfaces"][key]["newcomer_reviews"].extend(records)
    return updated


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--export", required=True, type=Path, help="session export JSON from the service")
    parser.add_argument("--ledger", type=Path, default=LEDGER)
    parser.add_argument("--write", action="store_true", help="append the records to the ledger")
    parser.add_argument("--accept-draft-questions", action="store_true",
                        help="an editor accepts responses to a draft question set as formal evidence")
    args = parser.parse_args()
    try:
        export_data = load_export(args.export)
        ledger = load_ledger(args.ledger)
        records, notes = stage(export_data, ledger, accept_draft_questions=args.accept_draft_questions)
    except (OSError, json.JSONDecodeError, StagingError, ValueError) as error:
        print(f"Cannot stage: {error}")
        return 1
    key = export_data["session"]["surface_key"]
    print(f"Session {export_data['session']['code']} for {key}: {len(records)} record(s) to stage.")
    for note in notes:
        print(f"- {note}")
    if not records:
        return 0
    updated = apply(ledger, key, records)
    failures = collect_failures(updated, REPO_ROOT)
    if failures:
        print("\nThe ledger would fail its check after staging; nothing written:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    if not args.write:
        print("\nDry run. Re-run with --write to append these records.")
        return 0
    args.ledger.write_text(json.dumps(updated, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nAppended {len(records)} record(s) to {args.ledger.relative_to(REPO_ROOT) if args.ledger.is_relative_to(REPO_ROOT) else args.ledger}.")
    print("Next: python scripts/check_newcomer_reviews.py; update the surface's ledger status by hand if the gates change.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
