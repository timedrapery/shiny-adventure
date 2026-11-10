"""Load submissions that arrived through a Google Form into the queue.

When there is nothing to host, the public page posts each submission as one
JSON string into a Google Form the editors own. Google keeps the responses
in a private sheet. This module reads that sheet's CSV export (or the JSON
the page would have sent) and stores each row exactly as the live endpoint
would have: full validation, session resolution, and the client submission
id as the duplicate guard, so a retry that reached the form twice becomes
one row here.

    python -m feedback_service ingest --csv responses.csv \
        --date-order mdy --timezone America/Los_Angeles
"""

from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .config import settings_from_env
from .storage import Storage, stamp
from .validation import ValidationError, validate_submission

# Google Sheets writes the form's response time in the sheet's own locale
# and time zone, and the CSV says neither. `03/04/2026` is March in one
# locale and April in another, so the importer never guesses: the editor
# states the sheet's date order and time zone, and a stamp that cannot be
# read that way is stored with the import time and a note saying so.
DATE_ORDERS = {
    "mdy": ("%m/%d/%Y %H:%M:%S", "%m/%d/%Y %H:%M"),
    "dmy": ("%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M"),
}
ISO_LOCAL_FORMATS = ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S")
ISO_UTC_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def sheet_zone(name: str) -> ZoneInfo:
    try:
        return ZoneInfo(name)
    except (ZoneInfoNotFoundError, ValueError) as error:
        raise ValueError(
            f"unknown time zone {name!r}; use an IANA name such as America/Los_Angeles "
            "(on Windows, install the tzdata package first)"
        ) from error


class IngestResult:
    def __init__(self) -> None:
        self.stored: list[str] = []
        self.duplicates: list[str] = []
        self.rejected: list[tuple[int, str]] = []
        self.dropped: list[int] = []
        self.unread_timestamps: list[tuple[int, str]] = []

    def summary(self) -> str:
        text = (
            f"stored {len(self.stored)}, already present {len(self.duplicates)}, "
            f"rejected {len(self.rejected)}, dropped {len(self.dropped)}"
        )
        if self.unread_timestamps:
            text += f", stored with an unreadable timestamp {len(self.unread_timestamps)}"
        return text


def parse_timestamp(value: str, *, date_order: str, zone: ZoneInfo) -> str | None:
    """The sheet's stamp as UTC, read in the stated date order and zone, or None."""
    if date_order not in DATE_ORDERS:
        raise ValueError(f"date order must be one of {sorted(DATE_ORDERS)}")
    text = (value or "").strip()
    try:
        return stamp(datetime.strptime(text, ISO_UTC_FORMAT).replace(tzinfo=timezone.utc))
    except ValueError:
        pass
    for pattern in DATE_ORDERS[date_order] + ISO_LOCAL_FORMATS:
        try:
            moment = datetime.strptime(text, pattern)
        except ValueError:
            continue
        return stamp(moment.replace(tzinfo=zone))
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


def rows_from_csv(path: Path) -> Iterable[tuple[int, str, str]]:
    # The csv module refuses any cell over 128 KiB by raising from the
    # reader, which ends the iteration and with it every row that follows.
    # The sheet is a local file the editor chose to import, so let the cell
    # through and reject it by size like any other oversized payload.
    csv.field_size_limit(min(sys.maxsize, 2**31 - 1))
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
            raw_stamp = row[timestamp_column] if timestamp_column is not None and timestamp_column < len(row) else ""
            yield number, raw_stamp, row[column] if column < len(row) else ""


def store_payload(storage: Storage, payload: Any, *, received_at: str | None,
                  contact_enabled: bool, result: IngestResult, line: int,
                  received_at_note: str = "") -> None:
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
        # The live endpoint refuses a closed session; the import must agree,
        # or a response the facilitator meant to exclude is counted anyway.
        # A row the form received before the session closed is still valid.
        if session["closed_at"] and not (received_at and received_at < session["closed_at"]):
            result.rejected.append((line, "session: closed"))
            return
        record["channel"] = "formal"
        record["session_id"] = session["id"]
        record["participant_id"] = participant["id"]
    if received_at:
        record["received_at"] = received_at
    if received_at_note:
        record["received_at_note"] = received_at_note
    contact = None
    if validated["contact"] is not None:
        from .app import CONSENT_TEXT

        contact = {"email": validated["contact"]["email"], "consent_text": CONSENT_TEXT}
    stored = storage.insert_submission(record, validated["terms"], contact)
    result.stored.append(stored["public_id"])


def ingest_csv(storage: Storage, path: Path, *, date_order: str, timezone_name: str,
               contact_enabled: bool = False, max_payload_bytes: int | None = None) -> IngestResult:
    """Import every row it can, and say why for each row it cannot.

    The form is public, so a row can hold anything. One row that cannot be
    read must never cost the rows after it: each is handled on its own, and a
    failure is recorded against its line number instead of ending the import.
    """
    if date_order not in DATE_ORDERS:
        raise ValueError(f"date order must be one of {sorted(DATE_ORDERS)}")
    zone = sheet_zone(timezone_name)
    limit = settings_from_env().max_body_bytes if max_payload_bytes is None else max_payload_bytes
    result = IngestResult()
    for line, raw_stamp, raw in rows_from_csv(path):
        received = parse_timestamp(raw_stamp, date_order=date_order, zone=zone)
        note = ""
        if received is None:
            note = (
                f"sheet timestamp {raw_stamp.strip()[:64]!r} could not be read as {date_order} "
                f"in {timezone_name}; the import time was stored instead"
            )
        if len(raw.encode("utf-8", errors="replace")) > limit:
            result.rejected.append((line, "payload too large"))
            continue
        try:
            # ValueError also covers an integer too long to parse, which is
            # not a JSONDecodeError.
            payload = json.loads(raw)
        except (ValueError, RecursionError):
            result.rejected.append((line, "payload is not JSON"))
            continue
        try:
            before = len(result.stored)
            store_payload(storage, payload, received_at=received, contact_enabled=contact_enabled,
                          result=result, line=line, received_at_note=note)
            if note and len(result.stored) > before:
                result.unread_timestamps.append((line, raw_stamp.strip()[:64]))
        except Exception as error:  # noqa: BLE001 - one bad row must not end the import
            result.rejected.append((line, f"could not be stored ({type(error).__name__})"))
    return result
