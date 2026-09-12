"""Reader feedback submission service.

A small WSGI application, standard library only, backed by SQLite. It
receives feedback from the generated reader, keeps it in a private queue for
maintainers, and exports reviewed formal-session evidence for the repository's
newcomer ledger. See README.md in this directory.
"""

__all__ = ["create_app"]

from .app import create_app  # noqa: E402
