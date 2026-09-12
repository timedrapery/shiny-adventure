"""The WSGI application.

Routes:

  GET  /api/health                      public probe used by the reader script
  POST /api/submissions                 public submission endpoint
  GET  /admin/...                       maintainer queue (HTTP Basic auth)
  GET  /<site files>                    the built reader, when --site-dir is set
                                        (local trial only; production serves the
                                        site from GitHub Pages and this service
                                        answers cross-origin API calls)

Request logging records method, path, status, and the submission's public id.
Bodies are never logged.
"""

from __future__ import annotations

import json
import logging
import mimetypes
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable
from urllib.parse import parse_qs, urlsplit

from . import admin as admin_views
from . import auth
from .config import Settings, settings_from_env
from .storage import Storage
from .validation import ValidationError, validate_submission

log = logging.getLogger("feedback_service")

JSON_HEADERS = [
    ("Content-Type", "application/json; charset=utf-8"),
    ("Cache-Control", "no-store"),
    ("X-Content-Type-Options", "nosniff"),
]
HTML_HEADERS = [
    ("Content-Type", "text/html; charset=utf-8"),
    ("Cache-Control", "no-store"),
    ("X-Content-Type-Options", "nosniff"),
    ("Referrer-Policy", "no-referrer"),
    ("X-Frame-Options", "DENY"),
    (
        "Content-Security-Policy",
        "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; "
        "base-uri 'none'; frame-ancestors 'none'",
    ),
]

CONSENT_TEXT = (
    "I agree that the editors may contact me once about this feedback. The "
    "address is stored separately from the feedback and deleted when the reply is sent."
)


class Request:
    def __init__(self, environ: dict[str, Any]) -> None:
        self.environ = environ
        self.method = environ.get("REQUEST_METHOD", "GET").upper()
        self.path = environ.get("PATH_INFO", "/") or "/"
        self.query = parse_qs(environ.get("QUERY_STRING", ""), keep_blank_values=False)
        self.headers = {
            key[5:].replace("_", "-").lower(): value
            for key, value in environ.items() if key.startswith("HTTP_")
        }
        if "CONTENT_TYPE" in environ:
            self.headers["content-type"] = environ["CONTENT_TYPE"]
        self._body: bytes | None = None

    def header(self, name: str) -> str | None:
        return self.headers.get(name.lower())

    def param(self, name: str) -> str:
        values = self.query.get(name)
        return values[0].strip() if values else ""

    def body(self, limit: int) -> bytes:
        if self._body is not None:
            return self._body
        try:
            length = int(self.environ.get("CONTENT_LENGTH") or 0)
        except ValueError:
            length = 0
        if length > limit:
            raise PayloadTooLarge()
        stream = self.environ.get("wsgi.input")
        data = stream.read(length) if (stream is not None and length) else b""
        if len(data) > limit:
            raise PayloadTooLarge()
        self._body = data
        return data

    def form(self, limit: int) -> dict[str, str]:
        data = self.body(limit).decode("utf-8", errors="replace")
        parsed = parse_qs(data, keep_blank_values=True)
        return {key: values[0] for key, values in parsed.items()}

    def client_address(self, trust_proxy: bool) -> str:
        if trust_proxy:
            forwarded = self.header("x-forwarded-for")
            if forwarded:
                return forwarded.split(",")[0].strip()
        return self.environ.get("REMOTE_ADDR", "unknown")

    def own_origin(self) -> str:
        scheme = self.environ.get("wsgi.url_scheme", "http")
        host = self.header("host") or self.environ.get("SERVER_NAME", "localhost")
        return f"{scheme}://{host}"


class PayloadTooLarge(Exception):
    pass


class Response:
    def __init__(self, status: str, headers: list[tuple[str, str]], body: bytes) -> None:
        self.status = status
        self.headers = headers
        self.body = body

    @classmethod
    def json(cls, payload: Any, status: str = "200 OK", extra: list[tuple[str, str]] | None = None) -> "Response":
        return cls(status, JSON_HEADERS + (extra or []), json.dumps(payload).encode("utf-8"))

    @classmethod
    def html(cls, markup: str, status: str = "200 OK", extra: list[tuple[str, str]] | None = None) -> "Response":
        return cls(status, HTML_HEADERS + (extra or []), markup.encode("utf-8"))

    @classmethod
    def redirect(cls, location: str) -> "Response":
        return cls("303 See Other", [("Location", location), ("Cache-Control", "no-store")], b"")

    @classmethod
    def text(cls, text: str, status: str) -> "Response":
        return cls(status, [("Content-Type", "text/plain; charset=utf-8"), ("Cache-Control", "no-store")], text.encode("utf-8"))


class FeedbackApp:
    def __init__(self, settings: Settings, storage: Storage | None = None) -> None:
        self.settings = settings
        self.storage = storage or Storage(settings.db_path)

    # -- WSGI entry point ---------------------------------------------------

    def __call__(self, environ: dict[str, Any], start_response: Callable) -> Iterable[bytes]:
        request = Request(environ)
        try:
            response = self.dispatch(request)
        except PayloadTooLarge:
            response = Response.json({"error": "payload too large"}, "413 Payload Too Large")
        except Exception:  # noqa: BLE001 - never leak a traceback to a client
            log.exception("unhandled error on %s %s", request.method, request.path)
            response = Response.json({"error": "internal error"}, "500 Internal Server Error")
        headers = list(response.headers) + [("Content-Length", str(len(response.body)))]
        log.info("%s %s -> %s", request.method, request.path, response.status.split(" ", 1)[0])
        start_response(response.status, headers)
        if request.method == "HEAD":
            return [b""]
        return [response.body]

    # -- routing ------------------------------------------------------------

    def dispatch(self, request: Request) -> Response:
        path = request.path
        if path == "/api/health" or path == "/api/submissions":
            return self.api(request)
        if path == "/admin" or path.startswith("/admin/"):
            return self.admin(request)
        if self.settings.site_dir is not None and request.method in {"GET", "HEAD"}:
            return self.static(request)
        return Response.json({"error": "not found"}, "404 Not Found")

    # -- public API ---------------------------------------------------------

    def cors_headers(self, request: Request) -> list[tuple[str, str]] | None:
        """CORS headers for an allowed origin, [] for same-origin, None if refused."""
        origin = request.header("origin")
        if not origin:
            return []
        if origin.rstrip("/") == request.own_origin():
            return []
        if origin.rstrip("/") in self.settings.allowed_origins:
            return [
                ("Access-Control-Allow-Origin", origin),
                ("Access-Control-Allow-Methods", "GET, POST, OPTIONS"),
                ("Access-Control-Allow-Headers", "Content-Type"),
                ("Access-Control-Max-Age", "600"),
                ("Vary", "Origin"),
            ]
        return None

    def api(self, request: Request) -> Response:
        cors = self.cors_headers(request)
        if cors is None:
            return Response.json({"error": "origin not allowed"}, "403 Forbidden")
        if request.method == "OPTIONS":
            return Response("204 No Content", cors + [("Cache-Control", "no-store")], b"")
        if request.path == "/api/health":
            if request.method not in {"GET", "HEAD"}:
                return Response.json({"error": "method not allowed"}, "405 Method Not Allowed", cors)
            return Response.json({"ok": True, "service": "reader-feedback"}, extra=cors)
        if request.method != "POST":
            return Response.json({"error": "method not allowed"}, "405 Method Not Allowed", cors)
        return self.submit(request, cors)

    def submit(self, request: Request, cors: list[tuple[str, str]]) -> Response:
        content_type = (request.header("content-type") or "").split(";")[0].strip().lower()
        if content_type != "application/json":
            return Response.json({"error": "expected application/json"}, "415 Unsupported Media Type", cors)
        raw = request.body(self.settings.max_body_bytes)
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return Response.json({"error": "invalid JSON"}, "400 Bad Request", cors)
        try:
            validated = validate_submission(payload, contact_enabled=self.settings.contact_enabled)
        except ValidationError as error:
            return Response.json({"error": str(error)}, "422 Unprocessable Content", cors)

        # Retries: the same client id always yields the first stored result,
        # before any rate accounting, so a retry is never punished or doubled.
        existing = self.storage.submission_by_client_id(validated["record"]["client_submission_id"])
        if existing is not None:
            return Response.json({"ok": True, "id": existing["public_id"], "duplicate": True}, extra=cors)

        if validated["honeypot"]:
            # Hidden field filled: almost certainly automated. Say yes, store nothing.
            return Response.json({"ok": True, "id": "fb_" + "0" * 12}, extra=cors)

        day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        client = auth.client_hash(self.settings.secret_key, request.client_address(self.settings.trust_proxy), day)
        if self.storage.rate_limited(client, self.settings.rate_limit_per_hour):
            return Response.json({"error": "too many submissions; try again later"}, "429 Too Many Requests",
                                 cors + [("Retry-After", "600")])

        record = validated["record"]
        record["channel"] = "public"
        if validated["session"] is not None:
            session = self.storage.session_by_code(validated["session"]["code"])
            if session is None or session["closed_at"]:
                return Response.json({"error": "session: unknown or closed session code"}, "422 Unprocessable Content", cors)
            if session["surface_key"] != record["surface_key"]:
                return Response.json({"error": "session: this session is for a different text"}, "422 Unprocessable Content", cors)
            participant = self.storage.participant(session["id"], validated["session"]["participant"])
            if participant is None:
                return Response.json({"error": "session: unknown participant label"}, "422 Unprocessable Content", cors)
            record["channel"] = "formal"
            record["session_id"] = session["id"]
            record["participant_id"] = participant["id"]

        contact = None
        if validated["contact"] is not None:
            contact = {"email": validated["contact"]["email"], "consent_text": CONSENT_TEXT}
        stored = self.storage.insert_submission(record, validated["terms"], contact)
        log.info("stored submission %s", stored["public_id"])
        return Response.json({"ok": True, "id": stored["public_id"]}, "201 Created", cors)

    # -- admin --------------------------------------------------------------

    def admin(self, request: Request) -> Response:
        if not self.settings.admin_enabled:
            return Response.text(
                "The maintainer area is disabled until FEEDBACK_MAINTAINER_USER and "
                "FEEDBACK_MAINTAINER_PASSWORD_HASH are configured.\n",
                "503 Service Unavailable",
            )
        user = auth.authenticate(
            request.header("authorization"),
            self.settings.maintainer_user,
            self.settings.maintainer_password_hash,
        )
        if user is None:
            return Response(
                "401 Unauthorized",
                [("WWW-Authenticate", 'Basic realm="Reader feedback maintainers", charset="UTF-8"'),
                 ("Content-Type", "text/plain; charset=utf-8"), ("Cache-Control", "no-store")],
                b"Authentication required.\n",
            )
        if request.method == "POST":
            fetch_site = (request.header("sec-fetch-site") or "").lower()
            origin = request.header("origin")
            if fetch_site in {"cross-site"} or (origin and origin.rstrip("/") != request.own_origin()):
                return Response.text("Cross-site form submission refused.\n", "403 Forbidden")
            form = request.form(self.settings.max_body_bytes * 4)
            if not auth.csrf_valid(self.settings.secret_key, user, form.get("csrf")):
                return Response.text("Form token missing or stale; reload and try again.\n", "403 Forbidden")
            return admin_views.handle_post(self, request, user, form)
        if request.method not in {"GET", "HEAD"}:
            return Response.text("Method not allowed.\n", "405 Method Not Allowed")
        return admin_views.handle_get(self, request, user)

    # -- static site (local trials) ------------------------------------------

    def static(self, request: Request) -> Response:
        root = self.settings.site_dir.resolve()
        relative = request.path.lstrip("/")
        candidate = (root / relative).resolve() if relative else root
        if root not in candidate.parents and candidate != root:
            return Response.text("Not found.\n", "404 Not Found")
        if candidate.is_dir():
            if not request.path.endswith("/"):
                return Response.redirect(request.path + "/")
            candidate = candidate / "index.html"
        if not candidate.is_file():
            return Response.text("Not found.\n", "404 Not Found")
        content_type = mimetypes.guess_type(str(candidate))[0] or "application/octet-stream"
        if content_type.startswith("text/") or content_type in {"application/javascript", "application/json"}:
            content_type += "; charset=utf-8"
        return Response("200 OK", [("Content-Type", content_type), ("Cache-Control", "no-cache")],
                        candidate.read_bytes())


def create_app(settings: Settings | None = None, storage: Storage | None = None) -> FeedbackApp:
    return FeedbackApp(settings or settings_from_env(), storage)
