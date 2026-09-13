"""Command line for the reader feedback service.

    python -m feedback_service serve [--host H] [--port P] [--site-dir site]
    python -m feedback_service migrate
    python -m feedback_service hash-password
    python -m feedback_service backup --out backups/
    python -m feedback_service purge --older-than 365 [--dry-run]
    python -m feedback_service delete --id fb_xxx [--contact-only]
    python -m feedback_service create-session --surface sn36_6 [--title ...]
    python -m feedback_service add-participant --session CODE --label R1 [--returning-from CODE/LABEL] [--independent yes|no]
    python -m feedback_service ingest --csv responses.csv
    python -m feedback_service export --out queue.json [--surface ...] [--status ...]
    python -m feedback_service export-session --code CODE --out session.json
    python -m feedback_service stats

Every command reads FEEDBACK_DB (default feedback-data/feedback.sqlite).
"""

from __future__ import annotations

import argparse
import getpass
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from wsgiref.simple_server import WSGIRequestHandler, make_server

from . import auth, export, ingest
from .app import FeedbackApp
from .config import settings_from_env
from .storage import Storage


class QuietHandler(WSGIRequestHandler):
    """wsgiref logs every request line by default; the app already does."""

    def log_message(self, format, *args):  # noqa: A002 - signature fixed by base class
        return


def cmd_serve(args: argparse.Namespace) -> int:
    overrides = {}
    if args.site_dir:
        overrides["site_dir"] = Path(args.site_dir)
    if args.db:
        overrides["db_path"] = Path(args.db)
    settings = settings_from_env(**overrides)
    app = FeedbackApp(settings)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    if not settings.admin_enabled:
        print("note: maintainer area disabled (set FEEDBACK_MAINTAINER_USER and "
              "FEEDBACK_MAINTAINER_PASSWORD_HASH to enable it)", file=sys.stderr)
    if settings.secret_is_ephemeral:
        print("note: FEEDBACK_SECRET_KEY is unset; using an ephemeral key for this run", file=sys.stderr)
    server = make_server(args.host, args.port, app, handler_class=QuietHandler)
    print(f"reader feedback service on http://{args.host}:{args.port}/ (db: {settings.db_path})",
          file=sys.stderr, flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


def storage_for(args: argparse.Namespace) -> Storage:
    settings = settings_from_env(**({"db_path": Path(args.db)} if getattr(args, "db", None) else {}))
    return Storage(settings.db_path)


def cmd_migrate(args: argparse.Namespace) -> int:
    storage = storage_for(args)
    applied = storage.migrate()
    print(f"database {storage.path}: {len(applied)} migration(s) applied" + (": " + ", ".join(applied) if applied else "; up to date"))
    return 0


def cmd_hash_password(args: argparse.Namespace) -> int:
    password = args.password if args.password is not None else getpass.getpass("Maintainer password: ")
    if len(password) < 12:
        print("use at least 12 characters", file=sys.stderr)
        return 2
    print(auth.hash_password(password))
    return 0


def cmd_backup(args: argparse.Namespace) -> int:
    storage = storage_for(args)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    destination = Path(args.out) / f"feedback-{stamp}.sqlite"
    storage.backup(destination)
    print(f"backup written to {destination}")
    return 0


def cmd_purge(args: argparse.Namespace) -> int:
    storage = storage_for(args)
    count = storage.purge_older_than(args.older_than, dry_run=args.dry_run)
    verb = "would delete" if args.dry_run else "deleted"
    print(f"{verb} {count} submission(s) older than {args.older_than} day(s)")
    return 0


def cmd_delete(args: argparse.Namespace) -> int:
    storage = storage_for(args)
    if args.contact_only:
        ok = storage.delete_contact(args.id)
        print("contact deleted" if ok else "no contact stored for that submission")
    else:
        ok = storage.delete_submission(args.id)
        print("submission deleted" if ok else "no such submission")
    return 0 if ok else 1


def cmd_create_session(args: argparse.Namespace) -> int:
    storage = storage_for(args)
    session = storage.create_session(args.surface, args.title or "", args.note or "", code=args.code)
    print(session["code"])
    return 0


def cmd_add_participant(args: argparse.Namespace) -> int:
    storage = storage_for(args)
    session = storage.session_by_code(args.session)
    if session is None:
        print("no such session", file=sys.stderr)
        return 1
    returning = None
    if args.returning_from:
        code, label = args.returning_from.split("/", 1)
        earlier_session = storage.session_by_code(code)
        earlier = storage.participant(earlier_session["id"], label) if earlier_session else None
        if earlier is None:
            print("earlier session/participant not found", file=sys.stderr)
            return 1
        returning = earlier["id"]
    independent = None if args.independent is None else args.independent == "yes"
    storage.add_participant(session["id"], args.label, "returning" if returning else "fresh", returning, independent)
    print(f"{session['code']}/{args.label}")
    return 0


def cmd_ingest(args: argparse.Namespace) -> int:
    storage = storage_for(args)
    settings = settings_from_env()
    try:
        result = ingest.ingest_csv(storage, Path(args.csv), contact_enabled=settings.contact_enabled)
    except (OSError, ValueError) as error:
        print(f"cannot ingest: {error}", file=sys.stderr)
        return 1
    print(result.summary())
    for line, reason in result.rejected:
        print(f"  line {line}: rejected ({reason})")
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    storage = storage_for(args)
    filters = {k: getattr(args, k) or "" for k in ("surface", "passage", "term", "category", "version", "status", "channel", "target", "session")}
    data = export.queue_export(storage, filters)
    Path(args.out).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {data['count']} submission(s) to {args.out}")
    return 0


def cmd_export_session(args: argparse.Namespace) -> int:
    storage = storage_for(args)
    data = export.session_export(storage, args.code)
    if data is None:
        print("no such session", file=sys.stderr)
        return 1
    Path(args.out).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(data['records'])} record(s) and {len(data['excluded'])} exclusion(s) to {args.out}")
    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    storage = storage_for(args)
    print(json.dumps(storage.counts()))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m feedback_service", description=__doc__.split("\n\n")[0])
    parser.add_argument("--db", help="SQLite path (overrides FEEDBACK_DB)")
    sub = parser.add_subparsers(dest="command", required=True)

    serve = sub.add_parser("serve", help="run the service")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8765)
    serve.add_argument("--site-dir", help="also serve a built reader from this directory (local trials)")
    serve.set_defaults(func=cmd_serve)

    sub.add_parser("migrate", help="apply pending migrations").set_defaults(func=cmd_migrate)

    hp = sub.add_parser("hash-password", help="print a password hash for FEEDBACK_MAINTAINER_PASSWORD_HASH")
    hp.add_argument("--password", help="read from the terminal when omitted")
    hp.set_defaults(func=cmd_hash_password)

    backup = sub.add_parser("backup", help="write a consistent copy of the database")
    backup.add_argument("--out", required=True)
    backup.set_defaults(func=cmd_backup)

    purge = sub.add_parser("purge", help="delete submissions older than N days")
    purge.add_argument("--older-than", type=int, required=True, metavar="DAYS")
    purge.add_argument("--dry-run", action="store_true")
    purge.set_defaults(func=cmd_purge)

    delete = sub.add_parser("delete", help="delete one submission, or only its contact record")
    delete.add_argument("--id", required=True)
    delete.add_argument("--contact-only", action="store_true")
    delete.set_defaults(func=cmd_delete)

    cs = sub.add_parser("create-session", help="create a formal review session")
    cs.add_argument("--surface", required=True)
    cs.add_argument("--title")
    cs.add_argument("--note")
    cs.add_argument("--code", help="explicit code (default: generated)")
    cs.set_defaults(func=cmd_create_session)

    ap = sub.add_parser("add-participant", help="add an anonymous participant label to a session")
    ap.add_argument("--session", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--returning-from", metavar="CODE/LABEL")
    ap.add_argument("--independent", choices=("yes", "no"))
    ap.set_defaults(func=cmd_add_participant)

    ing = sub.add_parser("ingest", help="load a Google Form responses CSV into the queue")
    ing.add_argument("--csv", required=True, help="the responses sheet exported as CSV")
    ing.set_defaults(func=cmd_ingest)

    ex = sub.add_parser("export", help="export the queue as JSON")
    ex.add_argument("--out", required=True)
    for name in ("surface", "passage", "term", "category", "version", "status", "channel", "target", "session"):
        ex.add_argument(f"--{name}")
    ex.set_defaults(func=cmd_export)

    es = sub.add_parser("export-session", help="reviewed export of one formal session")
    es.add_argument("--code", required=True)
    es.add_argument("--out", required=True)
    es.set_defaults(func=cmd_export_session)

    sub.add_parser("stats", help="row counts").set_defaults(func=cmd_stats)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
