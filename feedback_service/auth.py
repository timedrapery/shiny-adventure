"""Maintainer authentication and form protection for the admin area."""

from __future__ import annotations

import base64
import hashlib
import hmac
import secrets

PBKDF2_ITERATIONS = 600_000


def hash_password(password: str, iterations: int = PBKDF2_ITERATIONS) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), iterations)
    return f"pbkdf2_sha256${iterations}${salt}${digest.hex()}"


def verify_password(password: str, encoded: str) -> bool:
    try:
        algorithm, iterations, salt, expected = encoded.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        digest = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt.encode("utf-8"), int(iterations)
        )
    except (ValueError, TypeError):
        return False
    return hmac.compare_digest(digest.hex(), expected)


def parse_basic(header: str | None) -> tuple[str, str] | None:
    if not header or not header.startswith("Basic "):
        return None
    try:
        decoded = base64.b64decode(header[6:].strip(), validate=True).decode("utf-8")
    except (ValueError, UnicodeDecodeError):
        return None
    if ":" not in decoded:
        return None
    user, password = decoded.split(":", 1)
    return user, password


def authenticate(header: str | None, user: str | None, password_hash: str | None) -> str | None:
    """The authenticated maintainer name, or None."""
    if not user or not password_hash:
        return None
    parsed = parse_basic(header)
    if parsed is None:
        return None
    given_user, given_password = parsed
    # Compare the user name in constant time too, so the response does not
    # reveal which half was wrong.
    user_ok = hmac.compare_digest(given_user.encode("utf-8"), user.encode("utf-8"))
    password_ok = verify_password(given_password, password_hash)
    return user if (user_ok and password_ok) else None


def csrf_token(secret: str, user: str) -> str:
    return hmac.new(secret.encode("utf-8"), f"csrf:{user}".encode("utf-8"), hashlib.sha256).hexdigest()[:40]


def csrf_valid(secret: str, user: str, token: str | None) -> bool:
    return bool(token) and hmac.compare_digest(csrf_token(secret, user), token)


def client_hash(secret: str, address: str, day: str) -> str:
    """A per-day pseudonym for a client address, used only for rate limiting."""
    return hmac.new(secret.encode("utf-8"), f"{day}:{address}".encode("utf-8"), hashlib.sha256).hexdigest()[:32]
