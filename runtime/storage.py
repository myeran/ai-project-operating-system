"""Persistent Runtime MVP storage configuration."""

from __future__ import annotations

from pathlib import Path


RUNTIME_DATA_DIR = Path(__file__).with_name("data")
DEFAULT_DATABASE_PATH = RUNTIME_DATA_DIR / "runtime.sqlite3"


def resolve_database_path(database: str | Path | None) -> str:
    """Return a reusable database path and create its parent when needed."""

    if database is None:
        RUNTIME_DATA_DIR.mkdir(parents=True, exist_ok=True)
        return str(DEFAULT_DATABASE_PATH)
    if str(database) == ":memory:":
        return ":memory:"
    path = Path(database)
    path.parent.mkdir(parents=True, exist_ok=True)
    return str(path)
