"""Minimal SQLite-backed Project Registry Adapter.

This module owns Project Registry persistence and audit events only. Project
State, lifecycle decisions, routing, and user-facing responses are outside
its scope.
"""

from __future__ import annotations

import json
import sqlite3
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

try:
    from .storage import resolve_database_path
except ImportError:  # Supports direct test-module execution.
    from storage import resolve_database_path


STATUSES = {
    "proposed",
    "active",
    "blocked",
    "awaiting_approval",
    "completed",
    "cancelled",
}

AUDIT_EVENTS = {
    "project_created",
    "project_updated",
    "duplicate_rejected",
    "version_conflict",
}


class RegistryError(Exception):
    """Base error for Registry Adapter failures."""


class ValidationError(RegistryError):
    """Input does not satisfy the Registry contract."""


class DuplicateProjectError(RegistryError):
    """A project identity already exists."""


class ProjectNotFoundError(RegistryError):
    """The requested Project Instance does not exist."""


class VersionConflictError(RegistryError):
    """An update was based on a stale Registry version."""


@dataclass(frozen=True)
class ProjectMetadata:
    project_name: str
    owner: str
    location: str
    os_version: str
    status: str = "proposed"
    current_phase: str = "Discovery"
    audit_metadata: dict[str, Any] | None = None


class ProjectRegistryAdapter:
    """SQLite implementation of the approved Registry Adapter contract."""

    def __init__(self, database: str | Path | None = None) -> None:
        self.database = resolve_database_path(database)
        try:
            # The Runtime API may dispatch requests from a server thread.
            self._connection = sqlite3.connect(self.database, check_same_thread=False)
            self._connection.row_factory = sqlite3.Row
            self._connection.execute("PRAGMA foreign_keys = ON")
            self._initialize_schema()
        except sqlite3.Error as exc:
            raise RegistryError("Registry unavailable") from exc

    def close(self) -> None:
        self._connection.close()

    def __enter__(self) -> "ProjectRegistryAdapter":
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        self.close()

    def _initialize_schema(self) -> None:
        schema_path = Path(__file__).with_name("schema.sql")
        try:
            self._connection.executescript(schema_path.read_text(encoding="utf-8"))
            self._connection.commit()
        except (OSError, sqlite3.Error) as exc:
            self._connection.rollback()
            raise RegistryError("Registry schema initialization failed") from exc

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _normalize_name(project_name: str) -> str:
        return " ".join(project_name.casefold().split())

    @staticmethod
    def _validate_non_empty(value: str, field_name: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValidationError(f"{field_name} is required")

    @staticmethod
    def _validate_status(status: str) -> None:
        if status not in STATUSES:
            raise ValidationError(f"Unsupported status: {status}")

    @staticmethod
    def _json(value: Any) -> str:
        try:
            return json.dumps(value or {}, ensure_ascii=False, sort_keys=True)
        except (TypeError, ValueError) as exc:
            raise ValidationError("audit_metadata must be JSON-serializable") from exc

    @staticmethod
    def _row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
        result = dict(row)
        result["audit_metadata"] = json.loads(result["audit_metadata"])
        return result

    def _record_audit(
        self,
        *,
        event_type: str,
        project_id: str | None,
        actor: str,
        previous_version: int | None,
        new_version: int | None,
        details: dict[str, Any] | None = None,
    ) -> None:
        if event_type not in AUDIT_EVENTS:
            raise ValidationError(f"Unsupported audit event: {event_type}")
        self._validate_non_empty(actor, "actor")
        self._connection.execute(
            """
            INSERT INTO registry_audit
                (event_type, project_id, actor, event_timestamp,
                 previous_version, new_version, details)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event_type,
                project_id,
                actor,
                self._now(),
                previous_version,
                new_version,
                self._json(details),
            ),
        )

    def create_project(
        self,
        metadata: ProjectMetadata,
        *,
        actor: str,
        project_id: str | None = None,
    ) -> dict[str, Any]:
        """Create one Registry entry and its audit event atomically."""

        self._validate_non_empty(metadata.project_name, "project_name")
        self._validate_non_empty(metadata.owner, "owner")
        self._validate_non_empty(metadata.location, "location")
        self._validate_non_empty(metadata.os_version, "os_version")
        self._validate_non_empty(metadata.current_phase, "current_phase")
        self._validate_status(metadata.status)
        self._validate_non_empty(actor, "actor")

        project_id = project_id or str(uuid.uuid4())
        self._validate_non_empty(project_id, "project_id")
        name_key = self._normalize_name(metadata.project_name)
        now = self._now()

        try:
            existing = self._connection.execute(
                """
                SELECT project_id, project_name, version
                FROM project_registry
                WHERE project_id = ? OR project_name_key = ?
                """,
                (project_id, name_key),
            ).fetchall()
            if existing:
                with self._connection:
                    self._record_audit(
                        event_type="duplicate_rejected",
                        project_id=project_id,
                        actor=actor,
                        previous_version=None,
                        new_version=None,
                        details={
                            "project_name": metadata.project_name,
                            "matches": [dict(row) for row in existing],
                        },
                    )
                raise DuplicateProjectError(
                    f"Project identity already exists: {metadata.project_name}"
                )

            with self._connection:
                self._connection.execute(
                    """
                    INSERT INTO project_registry
                        (project_id, project_name, project_name_key, owner,
                         status, current_phase, os_version, location,
                         created_at, updated_at, last_activity, version,
                         audit_metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        project_id,
                        metadata.project_name.strip(),
                        name_key,
                        metadata.owner.strip(),
                        metadata.status,
                        metadata.current_phase.strip(),
                        metadata.os_version.strip(),
                        metadata.location.strip(),
                        now,
                        now,
                        now,
                        1,
                        self._json(metadata.audit_metadata),
                    ),
                )
                self._record_audit(
                    event_type="project_created",
                    project_id=project_id,
                    actor=actor,
                    previous_version=None,
                    new_version=1,
                    details={"project_name": metadata.project_name},
                )
                return self.get_project(project_id)
        except sqlite3.IntegrityError as exc:
            raise DuplicateProjectError("Project identity already exists") from exc
        except sqlite3.Error as exc:
            raise RegistryError("Registry unavailable during create") from exc

    def get_project(self, project_id: str) -> dict[str, Any]:
        self._validate_non_empty(project_id, "project_id")
        try:
            row = self._connection.execute(
                "SELECT * FROM project_registry WHERE project_id = ?",
                (project_id,),
            ).fetchone()
        except sqlite3.Error as exc:
            raise RegistryError("Registry unavailable during get") from exc
        if row is None:
            raise ProjectNotFoundError(f"Project not found: {project_id}")
        return self._row_to_dict(row)

    def find_projects(
        self,
        *,
        project_id: str | None = None,
        project_name: str | None = None,
    ) -> list[dict[str, Any]]:
        """Find by ID or normalized name; never chooses among multiple matches."""

        if project_id is None and project_name is None:
            raise ValidationError("project_id or project_name is required")
        if project_id is not None:
            self._validate_non_empty(project_id, "project_id")
            query = "SELECT * FROM project_registry WHERE project_id = ?"
            params: Iterable[str] = (project_id,)
        else:
            self._validate_non_empty(project_name or "", "project_name")
            query = "SELECT * FROM project_registry WHERE project_name_key = ?"
            params = (self._normalize_name(project_name or ""),)
        try:
            rows = self._connection.execute(query, tuple(params)).fetchall()
        except sqlite3.Error as exc:
            raise RegistryError("Registry unavailable during find") from exc
        return [self._row_to_dict(row) for row in rows]

    def update_project_metadata(
        self,
        project_id: str,
        *,
        expected_version: int,
        actor: str,
        status: str | None = None,
        current_phase: str | None = None,
        location: str | None = None,
        last_activity: str | None = None,
    ) -> dict[str, Any]:
        """Apply an allowlisted optimistic-concurrency metadata update."""

        self._validate_non_empty(project_id, "project_id")
        self._validate_non_empty(actor, "actor")
        if not isinstance(expected_version, int) or expected_version < 1:
            raise ValidationError("expected_version must be a positive integer")
        if status is None and current_phase is None and location is None and last_activity is None:
            raise ValidationError("At least one controlled field is required")
        if status is not None:
            self._validate_status(status)
        if current_phase is not None:
            self._validate_non_empty(current_phase, "current_phase")
        if location is not None:
            self._validate_non_empty(location, "location")
        if last_activity is not None:
            self._validate_non_empty(last_activity, "last_activity")

        changes: dict[str, Any] = {
            key: value
            for key, value in {
                "status": status,
                "current_phase": current_phase,
                "location": location,
                "last_activity": last_activity,
            }.items()
            if value is not None
        }
        now = self._now()
        if "last_activity" not in changes:
            changes["last_activity"] = now

        assignments = ", ".join(f"{field} = ?" for field in changes)
        values = [*changes.values(), now, project_id, expected_version]

        try:
            with self._connection:
                row = self._connection.execute(
                    "SELECT version FROM project_registry WHERE project_id = ?",
                    (project_id,),
                ).fetchone()
                if row is None:
                    raise ProjectNotFoundError(f"Project not found: {project_id}")
                current_version = int(row["version"])
                if current_version != expected_version:
                    conflict = (current_version, expected_version)
                else:
                    conflict = None

                if conflict is not None:
                    pass
                else:
                    cursor = self._connection.execute(
                        f"""
                        UPDATE project_registry
                        SET {assignments}, updated_at = ?, version = version + 1
                        WHERE project_id = ? AND version = ?
                        """,
                        tuple(values),
                    )
                    if cursor.rowcount != 1:
                        conflict = (current_version, expected_version)

                if conflict is not None:
                    self._connection.rollback()
                    current_version, expected_version = conflict
                    with self._connection:
                        self._record_audit(
                            event_type="version_conflict",
                            project_id=project_id,
                            actor=actor,
                            previous_version=current_version,
                            new_version=None,
                            details={
                                "expected_version": expected_version,
                                "current_version": current_version,
                            },
                        )
                    raise VersionConflictError(
                        f"Version conflict: expected {expected_version}, current {current_version}"
                    )

                new_version = expected_version + 1
                self._record_audit(
                    event_type="project_updated",
                    project_id=project_id,
                    actor=actor,
                    previous_version=expected_version,
                    new_version=new_version,
                    details={"changes": changes},
                )
                return self.get_project(project_id)
        except (ProjectNotFoundError, VersionConflictError):
            raise
        except sqlite3.Error as exc:
            raise RegistryError("Registry unavailable during update") from exc

    def audit_events(self, project_id: str | None = None) -> list[dict[str, Any]]:
        """Return audit events for verification and operational inspection."""

        query = "SELECT * FROM registry_audit"
        params: tuple[str, ...] = ()
        if project_id is not None:
            query += " WHERE project_id = ?"
            params = (project_id,)
        query += " ORDER BY audit_id"
        try:
            rows = self._connection.execute(query, params).fetchall()
        except sqlite3.Error as exc:
            raise RegistryError("Registry unavailable during audit read") from exc
        return [
            {**dict(row), "details": json.loads(row["details"])} for row in rows
        ]
