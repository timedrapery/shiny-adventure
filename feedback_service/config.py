"""Service settings, read from the environment.

Nothing here has a secret default. The admin area stays disabled until a
maintainer user, a password hash, and a secret key are supplied.
"""

from __future__ import annotations

import os
import secrets
from dataclasses import dataclass, field
from pathlib import Path


def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None or not raw.strip():
        return default
    try:
        return int(raw)
    except ValueError as error:
        raise SystemExit(f"{name} must be an integer, got {raw!r}") from error


def _env_list(name: str) -> tuple[str, ...]:
    raw = os.environ.get(name, "")
    return tuple(item.strip().rstrip("/") for item in raw.split(",") if item.strip())


@dataclass(frozen=True)
class Settings:
    db_path: Path
    site_dir: Path | None
    allowed_origins: tuple[str, ...]
    trust_proxy: bool
    max_body_bytes: int
    rate_limit_per_hour: int
    contact_enabled: bool
    maintainer_user: str | None
    maintainer_password_hash: str | None
    secret_key: str
    secret_is_ephemeral: bool
    retention_days: int | None
    base_path: str = ""
    extra: dict = field(default_factory=dict)

    @property
    def admin_enabled(self) -> bool:
        return bool(self.maintainer_user and self.maintainer_password_hash)


def settings_from_env(**overrides) -> Settings:
    env = os.environ
    secret = env.get("FEEDBACK_SECRET_KEY", "").strip()
    ephemeral = not secret
    if ephemeral:
        secret = secrets.token_hex(32)
    retention = env.get("FEEDBACK_RETENTION_DAYS", "").strip()
    values = dict(
        db_path=Path(env.get("FEEDBACK_DB", "feedback-data/feedback.sqlite")),
        site_dir=Path(env["FEEDBACK_SITE_DIR"]) if env.get("FEEDBACK_SITE_DIR") else None,
        allowed_origins=_env_list("FEEDBACK_ALLOWED_ORIGINS"),
        trust_proxy=env.get("FEEDBACK_TRUST_PROXY", "") == "1",
        max_body_bytes=_env_int("FEEDBACK_MAX_BODY_BYTES", 32 * 1024),
        rate_limit_per_hour=_env_int("FEEDBACK_RATE_LIMIT_PER_HOUR", 30),
        contact_enabled=env.get("FEEDBACK_ALLOW_CONTACT", "") == "1",
        maintainer_user=env.get("FEEDBACK_MAINTAINER_USER") or None,
        maintainer_password_hash=env.get("FEEDBACK_MAINTAINER_PASSWORD_HASH") or None,
        secret_key=secret,
        secret_is_ephemeral=ephemeral,
        retention_days=int(retention) if retention else None,
    )
    values.update(overrides)
    return Settings(**values)
