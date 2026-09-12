"""SQLite storage for the feedback service.

Migrations are numbered SQL files in `migrations/`, applied in order and
recorded in `schema_migrations`. The service applies pending migrations when
it opens the database, and `python -m feedback_service migrate` does the same
without starting the server.
"""

from __future__ import annotations

import json
import secrets
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

MIGRATIONS_DIR = Path(__file__).resolve().parent / "migrations"
STATUSES = ("received", "examined", "proposed", "revised", "checked")
FIX_LAYERS = ("", "translation", "glossary", "introduction", "lexicon", "none")
ASSESSMENTS = ("pass", "fail", "unclear")


def stamp(moment: datetime) -> str:
    """One timestamp format everywhere, so string comparison orders correctly."""
    return moment.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def utcnow() -> str:
    return stamp(datetime.now(timezone.utc))


def public_id() -> str:
    return "fb_" + secrets.token_urlsafe(9)


def session_code() -> str:
    alphabet = "abcdefghjkmnpqrstuvwxyz23456789"
    return "".join(secrets.choice(alphabet) for _ in range(8))


class Storage:
    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        if str(self.path) != ":memory:":
            self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(str(self.path), check_same_thread=False, isolation_level=None)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.execute("PRAGMA journal_mode = WAL") if str(self.path) != ":memory:" else None
        self.migrate()

    # -- migrations -------------------------------------------------------

    def migrate(self) -> list[str]:
        con = self.connection
        con.execute(
            "CREATE TABLE IF NOT EXISTS schema_migrations ("
            "version TEXT PRIMARY KEY, applied_at TEXT NOT NULL)"
        )
        applied = {row[0] for row in con.execute("SELECT version FROM schema_migrations")}
        done: list[str] = []
        for path in sorted(MIGRATIONS_DIR.glob("*.sql")):
            version = path.stem
            if version in applied:
                continue
            with con:
                con.execute("BEGIN")
                con.executescript(path.read_text(encoding="utf-8"))
                con.execute(
                    "INSERT INTO schema_migrations (version, applied_at) VALUES (?, ?)",
                    (version, utcnow()),
                )
            done.append(version)
        return done

    def close(self) -> None:
        self.connection.close()

    # -- rate limiting ----------------------------------------------------

    def rate_limited(self, client_hash: str, limit: int, window_seconds: int = 3600) -> bool:
        if limit <= 0:
            return False
        con = self.connection
        cutoff = stamp(datetime.now(timezone.utc) - timedelta(seconds=window_seconds))
        con.execute("DELETE FROM rate_events WHERE at < ?", (cutoff,))
        count = con.execute(
            "SELECT COUNT(*) FROM rate_events WHERE client_hash = ? AND at >= ?",
            (client_hash, cutoff),
        ).fetchone()[0]
        if count >= limit:
            return True
        con.execute(
            "INSERT INTO rate_events (client_hash, at) VALUES (?, ?)",
            (client_hash, utcnow()),
        )
        return False

    # -- sessions and participants -----------------------------------------

    def create_session(self, surface_key: str, title: str = "", note: str = "",
                       code: str | None = None) -> sqlite3.Row:
        code = code or session_code()
        self.connection.execute(
            "INSERT INTO sessions (code, surface_key, title, facilitator_note, created_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (code, surface_key, title, note, utcnow()),
        )
        return self.session_by_code(code)

    def session_by_code(self, code: str) -> sqlite3.Row | None:
        return self.connection.execute("SELECT * FROM sessions WHERE code = ?", (code,)).fetchone()

    def sessions(self) -> list[sqlite3.Row]:
        return list(self.connection.execute("SELECT * FROM sessions ORDER BY created_at DESC, id DESC"))

    def close_session(self, code: str, closed: bool = True) -> None:
        self.connection.execute(
            "UPDATE sessions SET closed_at = ? WHERE code = ?",
            (utcnow() if closed else None, code),
        )

    def add_participant(self, session_id: int, label: str, kind: str,
                        returning_from: int | None = None,
                        independent: bool | None = None) -> sqlite3.Row:
        self.connection.execute(
            "INSERT INTO participants (session_id, label, kind, returning_from_participant_id, "
            "independent, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (session_id, label, kind, returning_from,
             None if independent is None else int(independent), utcnow()),
        )
        return self.participant(session_id, label)

    def participant(self, session_id: int, label: str) -> sqlite3.Row | None:
        return self.connection.execute(
            "SELECT * FROM participants WHERE session_id = ? AND label = ?", (session_id, label)
        ).fetchone()

    def participant_by_id(self, participant_id: int) -> sqlite3.Row | None:
        return self.connection.execute(
            "SELECT * FROM participants WHERE id = ?", (participant_id,)
        ).fetchone()

    def participants(self, session_id: int) -> list[sqlite3.Row]:
        return list(self.connection.execute(
            "SELECT * FROM participants WHERE session_id = ? ORDER BY label", (session_id,)
        ))

    def set_participant_independent(self, participant_id: int, independent: bool | None) -> None:
        self.connection.execute(
            "UPDATE participants SET independent = ? WHERE id = ?",
            (None if independent is None else int(independent), participant_id),
        )

    # -- submissions ------------------------------------------------------

    def submission_by_client_id(self, client_submission_id: str) -> sqlite3.Row | None:
        return self.connection.execute(
            "SELECT * FROM submissions WHERE client_submission_id = ?", (client_submission_id,)
        ).fetchone()

    def submission(self, public_id_value: str) -> sqlite3.Row | None:
        return self.connection.execute(
            "SELECT * FROM submissions WHERE public_id = ?", (public_id_value,)
        ).fetchone()

    def insert_submission(self, record: dict[str, Any], terms: list[dict[str, str]],
                          contact: dict[str, Any] | None = None) -> sqlite3.Row:
        """Store one validated submission; idempotent on client_submission_id."""
        con = self.connection
        existing = self.submission_by_client_id(record["client_submission_id"])
        if existing is not None:
            return existing
        record = dict(record)
        record.setdefault("public_id", public_id())
        record.setdefault("received_at", utcnow())
        record.setdefault("terms_json", json.dumps(terms, ensure_ascii=False))
        counts = 0
        if record["target"] == "comprehension" and record.get("participant_id"):
            # One counted comprehension response per participant per body
            # version. A second one is kept, but never counted twice.
            already = con.execute(
                "SELECT COUNT(*) FROM submissions WHERE participant_id = ? AND target = ? "
                "AND body_sha256 = ? AND counts_for_session = 1",
                (record["participant_id"], "comprehension", record["body_sha256"]),
            ).fetchone()[0]
            counts = 0 if already else 1
        record["counts_for_session"] = counts
        columns = ", ".join(record)
        placeholders = ", ".join("?" for _ in record)
        with con:
            con.execute("BEGIN")
            try:
                cursor = con.execute(
                    f"INSERT INTO submissions ({columns}) VALUES ({placeholders})",
                    tuple(record.values()),
                )
            except sqlite3.IntegrityError:
                con.execute("ROLLBACK")
                return self.submission_by_client_id(record["client_submission_id"])
            row_id = cursor.lastrowid
            seen: set[str] = set()
            for term in terms:
                if term["id"] in seen:
                    continue
                seen.add(term["id"])
                con.execute(
                    "INSERT INTO submission_terms (submission_id, term_id, basis) VALUES (?, ?, ?)",
                    (row_id, term["id"], term["basis"]),
                )
            if contact is not None:
                con.execute(
                    "INSERT INTO contacts (submission_id, email, consent_text, recorded_at) "
                    "VALUES (?, ?, ?, ?)",
                    (row_id, contact["email"], contact["consent_text"], utcnow()),
                )
        return self.submission(record["public_id"])

    def terms_for(self, submission_id: int) -> list[sqlite3.Row]:
        return list(self.connection.execute(
            "SELECT term_id, basis FROM submission_terms WHERE submission_id = ? ORDER BY term_id",
            (submission_id,),
        ))

    def query(self, filters: dict[str, str], limit: int = 200, offset: int = 0) -> list[sqlite3.Row]:
        clauses: list[str] = []
        params: list[Any] = []
        simple = {
            "surface": "s.surface_key = ?",
            "passage": "s.passage_id = ?",
            "category": "(s.category = ? OR s.rating = ?)",
            "status": "s.status = ?",
            "channel": "s.channel = ?",
            "target": "s.target = ?",
        }
        for key, clause in simple.items():
            value = filters.get(key)
            if value:
                clauses.append(clause)
                params.extend([value] * clause.count("?"))
        version = filters.get("version")
        if version:
            clauses.append("s.body_sha256 LIKE ?")
            params.append(version + "%")
        term = filters.get("term")
        if term:
            clauses.append("EXISTS (SELECT 1 FROM submission_terms t WHERE t.submission_id = s.id AND t.term_id = ?)")
            params.append(term)
        session = filters.get("session")
        if session:
            clauses.append("s.session_id = (SELECT id FROM sessions WHERE code = ?)")
            params.append(session)
        where = (" WHERE " + " AND ".join(clauses)) if clauses else ""
        params.extend([limit, offset])
        return list(self.connection.execute(
            f"SELECT s.* FROM submissions s{where} ORDER BY s.received_at DESC, s.id DESC LIMIT ? OFFSET ?",
            params,
        ))

    def distinct(self, column: str) -> list[str]:
        assert column in {"surface_key", "status", "channel", "target", "category", "rating", "passage_id"}
        return [row[0] for row in self.connection.execute(
            f"SELECT DISTINCT {column} FROM submissions WHERE {column} IS NOT NULL AND {column} != '' ORDER BY 1"
        )]

    def term_groups(self) -> list[sqlite3.Row]:
        return list(self.connection.execute(
            "SELECT t.term_id, COUNT(*) AS submissions, "
            "COUNT(DISTINCT s.surface_key) AS surfaces, "
            "GROUP_CONCAT(DISTINCT s.surface_key) AS surface_keys, "
            "SUM(CASE WHEN s.status = 'received' THEN 1 ELSE 0 END) AS unexamined, "
            "SUM(CASE WHEN t.basis = 'explicit' THEN 1 ELSE 0 END) AS explicit_count "
            "FROM submission_terms t JOIN submissions s ON s.id = t.submission_id "
            "GROUP BY t.term_id ORDER BY submissions DESC, t.term_id"
        ))

    # -- dispositions -----------------------------------------------------

    def record_disposition(self, submission_id: int, recorded_by: str, status: str,
                           problem: str = "", fix_layer: str = "", rationale: str = "",
                           change_reference: str = "", follow_up_evidence: str = "",
                           confirmed_terms: str = "") -> None:
        if status not in STATUSES:
            raise ValueError(f"unknown status {status!r}")
        if fix_layer not in FIX_LAYERS:
            raise ValueError(f"unknown fix layer {fix_layer!r}")
        con = self.connection
        with con:
            con.execute("BEGIN")
            con.execute(
                "INSERT INTO dispositions (submission_id, recorded_at, recorded_by, status, problem, "
                "fix_layer, rationale, change_reference, follow_up_evidence, confirmed_terms) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (submission_id, utcnow(), recorded_by, status, problem, fix_layer, rationale,
                 change_reference, follow_up_evidence, confirmed_terms),
            )
            con.execute("UPDATE submissions SET status = ? WHERE id = ?", (status, submission_id))

    def dispositions(self, submission_id: int) -> list[sqlite3.Row]:
        return list(self.connection.execute(
            "SELECT * FROM dispositions WHERE submission_id = ? ORDER BY recorded_at, id",
            (submission_id,),
        ))

    def record_assessment(self, submission_id: int, assessment: str, note: str = "") -> None:
        if assessment not in ASSESSMENTS:
            raise ValueError(f"unknown assessment {assessment!r}")
        self.connection.execute(
            "UPDATE submissions SET assessment = ?, assessment_note = ?, assessed_at = ? WHERE id = ?",
            (assessment, note, utcnow(), submission_id),
        )

    # -- operations -------------------------------------------------------

    def delete_submission(self, public_id_value: str) -> bool:
        cursor = self.connection.execute(
            "DELETE FROM submissions WHERE public_id = ?", (public_id_value,)
        )
        return cursor.rowcount > 0

    def delete_contact(self, public_id_value: str) -> bool:
        cursor = self.connection.execute(
            "DELETE FROM contacts WHERE submission_id = (SELECT id FROM submissions WHERE public_id = ?)",
            (public_id_value,),
        )
        return cursor.rowcount > 0

    def purge_older_than(self, days: int, dry_run: bool = False) -> int:
        cutoff = stamp(datetime.now(timezone.utc) - timedelta(days=days))
        if dry_run:
            return self.connection.execute(
                "SELECT COUNT(*) FROM submissions WHERE received_at < ?", (cutoff,)
            ).fetchone()[0]
        cursor = self.connection.execute("DELETE FROM submissions WHERE received_at < ?", (cutoff,))
        self.connection.execute("DELETE FROM rate_events WHERE at < ?", (cutoff,))
        return cursor.rowcount

    def backup(self, destination: Path) -> Path:
        destination.parent.mkdir(parents=True, exist_ok=True)
        target = sqlite3.connect(str(destination))
        try:
            self.connection.backup(target)
        finally:
            target.close()
        return destination

    def counts(self) -> dict[str, int]:
        con = self.connection
        return {
            "submissions": con.execute("SELECT COUNT(*) FROM submissions").fetchone()[0],
            "contacts": con.execute("SELECT COUNT(*) FROM contacts").fetchone()[0],
            "sessions": con.execute("SELECT COUNT(*) FROM sessions").fetchone()[0],
        }
