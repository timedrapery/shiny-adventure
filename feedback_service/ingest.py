"""Load submissions that arrived through a Google Form into the queue.

When there is nothing to host, the public page posts each submission as one
JSON string into a Google Form the editors own. Google keeps the responses
in a private sheet. This module reads that sheet's CSV export (or the JSON
the page would have sent) and stores each row exactly as the live endpoint
would have: full validation, session resolution, and the client submission
id as the duplicate guard, so a retry that reached the form twice becomes
one row here.

    python -m feedback_service ingest --csv responses.csv
"""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .storage import Storage, stamp
from .validation import ValidationError, validate_submission

# Google Sheets writes the form's response time in the first column in the
# sheet's locale; a few common shapes are accepted, and anything else falls
# back to the ingest time with a note.
TIMESTAMP_FORMATS = (
    "%m/%d/%Y %H:%M:%S",
    "%d/%m/%Y %H:%M:%S",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%dT%H:%M:%SZ",
)


class IngestResult:
    def __init__(self) -> None:
        self.stored: list[str] = []
        self.duplicates: list[str] = []
        self.rejected: list[tuple[int, str]] = []
        self.dropped: list[int] = []

    def summary(self) -> str:
        return (
            f"stored {len(self.stored)}, already present {len(self.duplicates)}, "
            f"rejected {len(self.rejected)}, dropped {len(self.dropped)}"
        )


def parse_timestamp(value: str) -> str | None:
    text = (value or "").strip()
    for pattern in TIMESTAMP_FORMATS:
        try:
            moment = datetime.strptime(text, pattern)
        except ValueError:
            continue
        return stamp(moment.replace(tzinfo=timezone.utc))
    return None


def payload_column(header: list[str]) -> int:
    """The column holding the JSON payload: the one that is not the timestamp."""
    candidates = [i for i, name in enumerate(header) if name.strip().lower() != "timestamp"]
    if len(candidates) != 1:
        raise ValueError(
            "expected a sheet with a Timestamp column and exactly one payload column; "
            f"found columns {header!r}"
        )
    return candidates[0]


def rows_from_csv(path: Path) -> Iterable[tuple[int, str | None, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader, None)
        if header is None:
            return
        column = payload_column(header)
        timestamp_column = next(
            (i for i, name in enumerate(header) if name.strip().lower() == "timestamp"), None
        )
        for number, row in enumerate(reader, start=2):
            if not row or all(not cell.strip() for cell in row):
                continue
            received = parse_timestamp(row[timestamp_column]) if timestamp_column is not None else None
            yield number, received, row[column] if column < len(row) else ""


def store_payload(storage: Storage, payload: Any, *, received_at: str | None,
                  contact_enabled: bool, result: IngestResult, line: int) -> None:
    try:
        validated = validate_submission(payload, contact_enabled=contact_enabled)
    except ValidationError as error:
        result.rejected.append((line, str(error)))
        return
    if validated["honeypot"]:
        result.dropped.append(line)
        return
    record = validated["record"]
    existing = storage.submission_by_client_id(record["client_submission_id"])
    if existing is not None:
        result.duplicates.append(existing["public_id"])
        return
    record["channel"] = "public"
    if validated["session"] is not None:
        session = storage.session_by_code(validated["session"]["code"])
        participant = (
            storage.participant(session["id"], validated["session"]["participant"])
            if session is not None else None
        )
        if session is None or participant is None or session["surface_key"] != record["surface_key"]:
            result.rejected.append((line, "session: unknown session, participant, or wrong text"))
            return
        record["channel"] = "formal"
        record["session_id"] = session["id"]
        record["participant_id"] = participant["id"]
    if received_at:
        record["received_at"] = received_at
    contact = None
    if validated["contact"] is not None:
        from .app import CONSENT_TEXT

        contact = {"email": validated["contact"]["email"], "consent_text": CONSENT_TEXT}
    stored = storage.insert_submission(record, validated["terms"], contact)
    result.stored.append(stored["public_id"])


def ingest_csv(storage: Storage, path: Path, *, contact_enabled: bool = False) -> IngestResult:
    result = IngestResult()
    for line, received, raw in rows_from_csv(path):
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            result.rejected.append((line, "payload is not JSON"))
            continue
        store_payload(storage, payload, received_at=received, contact_enabled=contact_enabled,
                      result=result, line=line)
    return result
