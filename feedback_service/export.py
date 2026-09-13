"""Exports: the filtered queue, and the reviewed formal-session export.

The session export is shaped for `reviews/newcomer-review-ledger.json` and
is consumed by `scripts/stage_feedback_evidence.py`. It includes only
comprehension responses from a formal session that a maintainer has assessed
and that count for their participant and body version. Everything else is
listed under `excluded` with the reason, so nothing disappears silently.
Contact details are never exported.
"""

from __future__ import annotations

import json
from typing import Any

from .storage import Storage, utcnow

EXPORT_FORMAT = 1


def _row(row) -> dict[str, Any]:
    return {key: row[key] for key in row.keys()}


def submission_document(storage: Storage, row) -> dict[str, Any]:
    """A full, contact-free view of one submission with its history."""
    document = _row(row)
    document["terms"] = [{"id": t["term_id"], "basis": t["basis"]} for t in storage.terms_for(row["id"])]
    document["glossary_versions"] = json.loads(row["glossary_versions_json"] or "{}")
    document["answers"] = json.loads(row["answers_json"]) if row["answers_json"] else None
    document["dispositions"] = [_row(d) for d in storage.dispositions(row["id"])]
    for key in ("terms_json", "glossary_versions_json", "answers_json", "id"):
        document.pop(key, None)
    if row["session_id"]:
        session = storage.connection.execute(
            "SELECT code, surface_key, title FROM sessions WHERE id = ?", (row["session_id"],)
        ).fetchone()
        participant = storage.participant_by_id(row["participant_id"]) if row["participant_id"] else None
        document["session"] = {
            "code": session["code"] if session else None,
            "participant": participant["label"] if participant else None,
            "participant_kind": participant["kind"] if participant else None,
        }
    else:
        document["session"] = None
    for key in ("session_id", "participant_id"):
        document.pop(key, None)
    return document


def queue_export(storage: Storage, filters: dict[str, str], limit: int = 5000) -> dict[str, Any]:
    rows = storage.query(filters, limit=limit)
    return {
        "export_kind": "reader-feedback-queue",
        "export_format": EXPORT_FORMAT,
        "exported_at": utcnow(),
        "filters": {k: v for k, v in filters.items() if v},
        "count": len(rows),
        "submissions": [submission_document(storage, row) for row in rows],
    }


def session_export(storage: Storage, code: str) -> dict[str, Any] | None:
    session = storage.session_by_code(code)
    if session is None:
        return None
    participants = {p["id"]: p for p in storage.participants(session["id"])}
    rows = storage.connection.execute(
        "SELECT * FROM submissions WHERE session_id = ? AND target = 'comprehension' "
        "ORDER BY received_at, id",
        (session["id"],),
    ).fetchall()
    records: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []
    for row in rows:
        participant = participants.get(row["participant_id"])
        label = participant["label"] if participant else None
        base = {"submission_id": row["public_id"], "participant": label}
        if row["channel"] != "formal" or participant is None:
            excluded.append(dict(base, reason="not a formal-session response"))
            continue
        if not row["counts_for_session"]:
            excluded.append(dict(base, reason="a counted response for this participant and body version already exists"))
            continue
        if not row["assessment"]:
            excluded.append(dict(base, reason="not yet assessed by a maintainer"))
            continue
        if participant["independent"] is None:
            excluded.append(dict(base, reason="facilitator has not recorded whether the session was independent"))
            continue
        answers = json.loads(row["answers_json"] or "{}")
        returning = None
        if participant["returning_from_participant_id"]:
            earlier = storage.participant_by_id(participant["returning_from_participant_id"])
            if earlier is not None:
                earlier_session = storage.connection.execute(
                    "SELECT code FROM sessions WHERE id = ?", (earlier["session_id"],)
                ).fetchone()
                returning = {"session": earlier_session["code"] if earlier_session else None,
                             "participant": earlier["label"]}
        records.append({
            "participant": label,
            "participant_kind": participant["kind"],
            "returning_from": returning,
            "reviewed_on": row["received_at"][:10],
            "independent": bool(participant["independent"]),
            "what_happened": answers.get("paraphrase", ""),
            "practical_point": answers.get("specific", ""),
            "confusing_words": [answers["reread"]] if answers.get("reread") else [],
            "pass": row["assessment"] == "pass",
            "assessment": row["assessment"],
            "assessment_note": row["assessment_note"],
            "body_sha256": row["body_sha256"],
            "familiarity": row["familiarity"],
            "question_version": row["question_version"],
            "question_set_sha256": row["question_set_sha256"],
            "question_editorial_status": row["question_editorial_status"],
            "submission_id": row["public_id"],
        })
    return {
        "export_kind": "formal-session-review",
        "export_format": EXPORT_FORMAT,
        "exported_at": utcnow(),
        "session": {
            "code": session["code"],
            "surface_key": session["surface_key"],
            "title": session["title"],
            "created_at": session["created_at"],
            "closed_at": session["closed_at"],
        },
        "participants": [
            {"label": p["label"], "kind": p["kind"], "independent": p["independent"]}
            for p in participants.values()
        ],
        "records": records,
        "excluded": excluded,
    }
