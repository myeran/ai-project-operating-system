"""Canonical Project State persistence for the Runtime MVP.

The adapter stores the approved state projection plus the canonical state
payload. It creates proposals without committing them and commits only an
approved proposal with a matching version.
"""

from __future__ import annotations

import json
import sqlite3
import uuid
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

try:
    from .registry_adapter import RegistryError, ValidationError, VersionConflictError
    from .storage import resolve_database_path
except ImportError:  # Supports direct test-module execution.
    from registry_adapter import RegistryError, ValidationError, VersionConflictError
    from storage import resolve_database_path


PHASES = {
    "Discovery",
    "Strategy",
    "Planning",
    "Design",
    "Execution",
    "Validation",
    "Launch",
    "Learning",
    "Completed",
}

STATUSES = {
    "proposed",
    "active",
    "blocked",
    "awaiting_approval",
    "completed",
    "cancelled",
}

ALLOWED_TRANSITIONS = {
    "Discovery": {"Strategy"},
    "Strategy": {"Planning"},
    "Planning": {"Design", "Execution"},
    "Design": {"Execution"},
    "Execution": {"Validation"},
    "Validation": {"Launch", "Learning"},
    "Launch": {"Learning"},
    "Learning": {"Completed"},
    "Completed": set(),
}

ALLOWED_UPDATE_FIELDS = {
    "phase",
    "status",
    "completed_outputs",
    "missing_items",
    "required_user_action",
    "expected_output",
    "completion_criteria",
    "next_recommended_action",
    "knowledge_items",
    "discovery_output",
}

KNOWLEDGE_STATUSES = {"open", "approved", "needs_update"}


class StateAdapterError(RegistryError):
    """Base error for State Adapter failures."""


class ProjectStateNotFoundError(StateAdapterError):
    """No state exists for the requested Project Instance."""


class InvalidStateError(StateAdapterError):
    """Persisted or proposed state is malformed."""


class InvalidTransitionError(StateAdapterError):
    """A proposed phase transition is not allowed."""


class ApprovalRequiredError(StateAdapterError):
    """A valid phase transition lacks explicit approval."""


class RegistryStateMismatchError(StateAdapterError):
    """Registry and Project State projections are not aligned for a commit."""


class StateAdapter:
    """SQLite-backed adapter for canonical Project State."""

    def __init__(self, database: str | Path | None = None) -> None:
        self.database = resolve_database_path(database)
        try:
            # The Runtime API may dispatch requests from a server thread.
            self._connection = sqlite3.connect(self.database, check_same_thread=False)
            self._connection.row_factory = sqlite3.Row
            self._connection.execute("PRAGMA foreign_keys = ON")
            self._initialize_schema()
        except sqlite3.Error as exc:
            raise StateAdapterError("State storage unavailable") from exc

    def close(self) -> None:
        self._connection.close()

    def __enter__(self) -> "StateAdapter":
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        self.close()

    def _initialize_schema(self) -> None:
        base_schema = Path(__file__).with_name("schema.sql").read_text(encoding="utf-8")
        state_schema = Path(__file__).with_name("state_schema.sql").read_text(encoding="utf-8")
        try:
            self._connection.executescript(base_schema)
            self._connection.executescript(state_schema)
            self._migrate_proposal_schema()
            self._migrate_audit_schema()
            self._connection.commit()
        except (OSError, sqlite3.Error) as exc:
            self._connection.rollback()
            raise StateAdapterError("State schema initialization failed") from exc

    def _migrate_proposal_schema(self) -> None:
        """Upgrade the MVP proposal table without losing existing proposals."""

        row = self._connection.execute(
            "SELECT sql FROM sqlite_master WHERE type = 'table' AND name = 'state_update_proposals'"
        ).fetchone()
        schema = row[0] if row else ""
        if "'approved'" in schema and "approved_at" in schema:
            return

        self._connection.execute("DROP INDEX IF EXISTS idx_state_proposals_project")
        self._connection.execute("ALTER TABLE state_update_proposals RENAME TO state_update_proposals_legacy")
        self._connection.execute(
            """
            CREATE TABLE state_update_proposals (
                proposal_id TEXT PRIMARY KEY,
                project_id TEXT NOT NULL,
                changes TEXT NOT NULL,
                actor TEXT NOT NULL,
                expected_version INTEGER NOT NULL,
                approved_by TEXT,
                status TEXT NOT NULL CHECK (status IN ('pending', 'approved', 'committed', 'rejected')),
                created_at TEXT NOT NULL,
                approved_at TEXT,
                committed_at TEXT,
                committed_by TEXT,
                new_version INTEGER,
                rejected_at TEXT,
                rejected_by TEXT,
                rejection_reason TEXT,
                FOREIGN KEY (project_id) REFERENCES project_registry(project_id)
            )
            """
        )
        self._connection.execute(
            """
            INSERT INTO state_update_proposals
                (proposal_id, project_id, changes, actor, expected_version,
                 approved_by, status, created_at, committed_at, committed_by, new_version)
            SELECT proposal_id, project_id, changes, actor, expected_version,
                   approved_by, status, created_at, committed_at, committed_by, new_version
            FROM state_update_proposals_legacy
            """
        )
        self._connection.execute("DROP TABLE state_update_proposals_legacy")
        self._connection.execute(
            "CREATE INDEX idx_state_proposals_project ON state_update_proposals(project_id)"
        )

    def _migrate_audit_schema(self) -> None:
        row = self._connection.execute(
            "SELECT sql FROM sqlite_master WHERE type = 'table' AND name = 'state_audit'"
        ).fetchone()
        schema = row[0] if row else ""
        if "state_proposal_approved" in schema:
            return
        self._connection.execute("ALTER TABLE state_audit RENAME TO state_audit_legacy")
        self._connection.execute(
            """
            CREATE TABLE state_audit (
                audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL CHECK (event_type IN (
                    'state_created', 'state_update_proposed', 'state_updated',
                    'version_conflict', 'invalid_transition_rejected',
                    'approval_required', 'state_proposal_approved', 'state_proposal_rejected'
                )),
                project_id TEXT NOT NULL,
                actor TEXT NOT NULL,
                event_timestamp TEXT NOT NULL,
                previous_version INTEGER,
                new_version INTEGER,
                details TEXT NOT NULL DEFAULT '{}'
            )
            """
        )
        self._connection.execute(
            """
            INSERT INTO state_audit
                (audit_id, event_type, project_id, actor, event_timestamp,
                 previous_version, new_version, details)
            SELECT audit_id, event_type, project_id, actor, event_timestamp,
                   previous_version, new_version, details
            FROM state_audit_legacy
            """
        )
        self._connection.execute("DROP TABLE state_audit_legacy")
        self._connection.execute("CREATE INDEX idx_state_audit_project ON state_audit(project_id)")

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _json(value: Any) -> str:
        try:
            return json.dumps(value, ensure_ascii=False, sort_keys=True)
        except (TypeError, ValueError) as exc:
            raise ValidationError("State value must be JSON-serializable") from exc

    @staticmethod
    def _loads(value: str, field_name: str) -> Any:
        try:
            return json.loads(value)
        except (TypeError, json.JSONDecodeError) as exc:
            raise InvalidStateError(f"Invalid JSON in {field_name}") from exc

    @staticmethod
    def _require_actor(actor: str) -> None:
        if not isinstance(actor, str) or not actor.strip():
            raise ValidationError("actor is required")

    @staticmethod
    def _validate_phase(phase: str) -> None:
        if phase not in PHASES:
            raise InvalidStateError(f"Unsupported phase: {phase}")

    @staticmethod
    def _validate_status(status: str) -> None:
        if status not in STATUSES:
            raise InvalidStateError(f"Unsupported status: {status}")

    @staticmethod
    def _validate_projection_field(field_name: str, value: Any) -> None:
        list_fields = {
            "completed_outputs",
            "missing_items",
            "expected_output",
            "completion_criteria",
        }
        text_fields = {"required_user_action", "next_recommended_action"}
        if field_name in list_fields and not isinstance(value, list):
            raise InvalidStateError(f"{field_name} must be a list")
        if field_name in text_fields and value is not None and not isinstance(value, str):
            raise InvalidStateError(f"{field_name} must be a string or null")
        if field_name == "knowledge_items":
            if not isinstance(value, list):
                raise InvalidStateError("knowledge_items must be a list")
            seen: set[str] = set()
            for item in value:
                if not isinstance(item, dict):
                    raise InvalidStateError("Each knowledge item must be an object")
                item_id = item.get("id")
                if not isinstance(item_id, str) or not item_id.strip() or item_id in seen:
                    raise InvalidStateError("Knowledge item IDs must be unique non-empty strings")
                if not isinstance(item.get("question"), str) or not item["question"].strip():
                    raise InvalidStateError("Knowledge item question is required")
                if not isinstance(item.get("answer", ""), str):
                    raise InvalidStateError("Knowledge item answer must be a string")
                if item.get("status") not in KNOWLEDGE_STATUSES:
                    raise InvalidStateError("Knowledge item status is unsupported")
                seen.add(item_id)
        if field_name == "discovery_output" and not isinstance(value, dict):
            raise InvalidStateError("discovery_output must be an object")

    def _record_audit(
        self,
        *,
        event_type: str,
        project_id: str,
        actor: str,
        previous_version: int | None,
        new_version: int | None,
        details: dict[str, Any] | None = None,
    ) -> None:
        self._connection.execute(
            """
            INSERT INTO state_audit
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
                self._json(details or {}),
            ),
        )

    def _registry_identity(self, project_id: str) -> dict[str, Any]:
        row = self._connection.execute(
            "SELECT project_id, project_name, owner FROM project_registry WHERE project_id = ?",
            (project_id,),
        ).fetchone()
        if row is None:
            raise ProjectStateNotFoundError(f"Project Registry entry not found: {project_id}")
        return dict(row)

    @staticmethod
    def _canonical_initial_state(
        identity: dict[str, Any],
        phase: str,
        status: str,
        now: str,
        project_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return {
            "project_identity": {
                "project_id": identity["project_id"],
                "name": identity["project_name"],
                "description": "",
                "owner": identity["owner"],
                "stakeholders": [],
                "project_context": project_context or {},
            },
            "current_status": {
                "current_phase": phase,
                "status": status,
                "progress": 0,
                "blockers": [],
            },
            "planning_data": {
                "goals": [],
                "scope": {"in_scope": [], "out_of_scope": [], "change_history": []},
                "timeline": {},
                "resources": [],
            },
            "decision_management": {"decisions": [], "pending_decisions": [], "approvals": []},
            "risk_management": {"risks": [], "dependencies": [], "issues": []},
            "knowledge": {"documents": [], "outputs": [], "lessons_learned": [], "items": []},
            "next_actions": {"tasks": [], "owners": [], "due_dates": []},
            "audit": {
                "last_updated_at": now,
                "last_updated_by": "state-adapter",
                "version": 1,
                "history_ref": identity["project_id"],
            },
        }

    def _row_to_state(self, row: sqlite3.Row) -> dict[str, Any]:
        state = dict(row)
        state["completed_outputs"] = self._loads(state["completed_outputs"], "completed_outputs")
        state["missing_items"] = self._loads(state["missing_items"], "missing_items")
        state["expected_output"] = self._loads(state["expected_output"], "expected_output")
        state["completion_criteria"] = self._loads(state["completion_criteria"], "completion_criteria")
        state["canonical_state"] = self._loads(state["canonical_state"], "canonical_state")
        state["knowledge_items"] = list((state["canonical_state"].get("knowledge") or {}).get("items") or [])
        state["discovery_output"] = (state["canonical_state"].get("knowledge") or {}).get("discovery_output")
        return state

    def get_state(self, project_id: str) -> dict[str, Any]:
        try:
            row = self._connection.execute(
                "SELECT * FROM project_state WHERE project_id = ?",
                (project_id,),
            ).fetchone()
        except sqlite3.Error as exc:
            raise StateAdapterError("State storage unavailable during read") from exc
        if row is None:
            raise ProjectStateNotFoundError(f"Project State not found: {project_id}")
        try:
            self._validate_phase(row["phase"])
            self._validate_status(row["status"])
            return self._row_to_state(row)
        except (InvalidStateError, json.JSONDecodeError) as exc:
            raise InvalidStateError(f"Invalid Project State: {project_id}") from exc

    def create_initial_state(
        self,
        project_id: str,
        *,
        initial_phase: str = "Discovery",
        initial_status: str = "proposed",
        actor: str = "bootstrap",
        description: str = "",
        project_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        self._validate_phase(initial_phase)
        self._validate_status(initial_status)
        self._require_actor(actor)
        identity = self._registry_identity(project_id)
        if not isinstance(description, str):
            raise ValidationError("description must be a string")
        if project_context is not None and not isinstance(project_context, dict):
            raise ValidationError("project_context must be an object")
        now = self._now()
        canonical = self._canonical_initial_state(
            identity, initial_phase, initial_status, now, project_context
        )
        canonical["project_identity"]["description"] = description.strip()
        try:
            with self._connection:
                self._connection.execute(
                    """
                    INSERT INTO project_state
                        (project_id, phase, status, completed_outputs, missing_items,
                         required_user_action, expected_output, completion_criteria,
                         next_recommended_action, canonical_state, version,
                         updated_by, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        project_id,
                        initial_phase,
                        initial_status,
                        "[]",
                        "[]",
                        None,
                        "[]",
                        "[]",
                        None,
                        self._json(canonical),
                        1,
                        actor,
                        now,
                    ),
                )
                self._record_audit(
                    event_type="state_created",
                    project_id=project_id,
                    actor=actor,
                    previous_version=None,
                    new_version=1,
                    details={"phase": initial_phase, "status": initial_status},
                )
                return self.get_state(project_id)
        except sqlite3.IntegrityError as exc:
            raise StateAdapterError(f"Project State already exists: {project_id}") from exc
        except sqlite3.Error as exc:
            raise StateAdapterError("State storage unavailable during create") from exc

    def propose_state_update(
        self,
        project_id: str,
        changes: dict[str, Any],
        *,
        actor: str,
        approved_by: str | None = None,
    ) -> dict[str, Any]:
        """Persist a validated proposal without changing canonical state."""

        self._require_actor(actor)
        if not changes or not isinstance(changes, dict):
            raise ValidationError("changes must be a non-empty mapping")
        unknown = set(changes) - ALLOWED_UPDATE_FIELDS
        if unknown:
            raise ValidationError(f"Unsupported state fields: {sorted(unknown)}")
        current = self.get_state(project_id)
        for field, value in changes.items():
            self._validate_projection_field(field, value)
        if "phase" in changes:
            self._validate_phase(changes["phase"])
            if changes["phase"] != current["phase"]:
                allowed = ALLOWED_TRANSITIONS.get(current["phase"], set())
                if changes["phase"] not in allowed:
                    with self._connection:
                        self._record_audit(
                            event_type="invalid_transition_rejected",
                            project_id=project_id,
                            actor=actor,
                            previous_version=current["version"],
                            new_version=None,
                            details={"from": current["phase"], "to": changes["phase"]},
                        )
                    raise InvalidTransitionError(
                        f"Invalid transition: {current['phase']} -> {changes['phase']}"
                    )
        if "status" in changes:
            self._validate_status(changes["status"])

        proposal_id = str(uuid.uuid4())
        now = self._now()
        try:
            with self._connection:
                self._connection.execute(
                    """
                    INSERT INTO state_update_proposals
                        (proposal_id, project_id, changes, actor, expected_version,
                         approved_by, status, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, 'pending', ?)
                    """,
                    (
                        proposal_id,
                        project_id,
                        self._json(changes),
                        actor,
                        current["version"],
                        approved_by,
                        now,
                    ),
                )
                self._record_audit(
                    event_type="state_update_proposed",
                    project_id=project_id,
                    actor=actor,
                    previous_version=current["version"],
                    new_version=None,
                    details={"proposal_id": proposal_id, "changes": changes},
                )
        except sqlite3.Error as exc:
            raise StateAdapterError("State storage unavailable during proposal") from exc
        return {
            "proposal_id": proposal_id,
            "project_id": project_id,
            "changes": changes,
            "actor": actor,
            "expected_version": current["version"],
            "approved_by": approved_by,
            "status": "pending",
            "created_at": now,
        }

    def _row_to_proposal(self, row: sqlite3.Row) -> dict[str, Any]:
        proposal = dict(row)
        proposal["changes"] = self._loads(proposal["changes"], "proposal changes")
        return proposal

    def get_proposal(self, proposal_id: str) -> dict[str, Any]:
        try:
            row = self._connection.execute(
                "SELECT * FROM state_update_proposals WHERE proposal_id = ?",
                (proposal_id,),
            ).fetchone()
        except sqlite3.Error as exc:
            raise StateAdapterError("State storage unavailable during proposal read") from exc
        if row is None:
            raise StateAdapterError(f"State proposal not found: {proposal_id}")
        return self._row_to_proposal(row)

    def list_proposals(
        self,
        project_id: str,
        *,
        status: str | None = "pending",
    ) -> list[dict[str, Any]]:
        query = "SELECT * FROM state_update_proposals WHERE project_id = ?"
        params: list[Any] = [project_id]
        if status is not None:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY created_at"
        try:
            rows = self._connection.execute(query, tuple(params)).fetchall()
        except sqlite3.Error as exc:
            raise StateAdapterError("State storage unavailable during proposal listing") from exc
        return [self._row_to_proposal(row) for row in rows]

    def approve_state_proposal(self, proposal_id: str, *, approver: str) -> dict[str, Any]:
        self._require_actor(approver)
        proposal = self.get_proposal(proposal_id)
        if proposal["status"] != "pending":
            raise StateAdapterError(f"State proposal is not pending: {proposal_id}")
        current = self.get_state(proposal["project_id"])
        if current["version"] != proposal["expected_version"]:
            with self._connection:
                self._record_audit(
                    event_type="version_conflict",
                    project_id=proposal["project_id"],
                    actor=approver,
                    previous_version=current["version"],
                    new_version=None,
                    details={"proposal_id": proposal_id, "expected_version": proposal["expected_version"]},
                )
            raise VersionConflictError(
                f"Version conflict: expected {proposal['expected_version']}, current {current['version']}"
            )
        now = self._now()
        try:
            with self._connection:
                self._connection.execute(
                    """
                    UPDATE state_update_proposals
                    SET status = 'approved', approved_by = ?, approved_at = ?
                    WHERE proposal_id = ? AND status = 'pending'
                    """,
                    (approver, now, proposal_id),
                )
                self._record_audit(
                    event_type="state_proposal_approved",
                    project_id=proposal["project_id"],
                    actor=approver,
                    previous_version=current["version"],
                    new_version=None,
                    details={"proposal_id": proposal_id},
                )
        except sqlite3.Error as exc:
            raise StateAdapterError("State storage unavailable during proposal approval") from exc
        return self.get_proposal(proposal_id)

    def reject_state_proposal(
        self,
        proposal_id: str,
        *,
        rejector: str,
        reason: str = "Proposal rejected",
    ) -> dict[str, Any]:
        self._require_actor(rejector)
        if not isinstance(reason, str) or not reason.strip():
            raise ValidationError("rejection reason is required")
        proposal = self.get_proposal(proposal_id)
        if proposal["status"] != "pending":
            raise StateAdapterError(f"State proposal is not pending: {proposal_id}")
        now = self._now()
        try:
            with self._connection:
                self._connection.execute(
                    """
                    UPDATE state_update_proposals
                    SET status = 'rejected', rejected_by = ?, rejected_at = ?, rejection_reason = ?
                    WHERE proposal_id = ? AND status = 'pending'
                    """,
                    (rejector, now, reason.strip(), proposal_id),
                )
                self._record_audit(
                    event_type="state_proposal_rejected",
                    project_id=proposal["project_id"],
                    actor=rejector,
                    previous_version=proposal["expected_version"],
                    new_version=None,
                    details={"proposal_id": proposal_id, "reason": reason.strip()},
                )
        except sqlite3.Error as exc:
            raise StateAdapterError("State storage unavailable during proposal rejection") from exc
        return self.get_proposal(proposal_id)

    def commit_state_update(
        self,
        proposal_id: str,
        *,
        expected_version: int,
        approved_by: str | None = None,
        require_approval: bool = False,
    ) -> dict[str, Any]:
        """Commit an approved proposal with optimistic version checking."""

        self._require_actor(approved_by or "system")
        proposal = self._connection.execute(
            "SELECT * FROM state_update_proposals WHERE proposal_id = ?",
            (proposal_id,),
        ).fetchone()
        if proposal is None:
            raise StateAdapterError(f"State proposal not found: {proposal_id}")
        if proposal["status"] not in {"pending", "approved"}:
            raise StateAdapterError(f"State proposal cannot be committed: {proposal_id}")
        if require_approval and proposal["status"] != "approved":
            raise ApprovalRequiredError(f"State proposal must be approved before commit: {proposal_id}")

        project_id = proposal["project_id"]
        current = self.get_state(project_id)
        changes = self._loads(proposal["changes"], "proposal changes")
        if current["version"] != expected_version or expected_version != proposal["expected_version"]:
            with self._connection:
                self._record_audit(
                    event_type="version_conflict",
                    project_id=project_id,
                    actor=approved_by or "system",
                    previous_version=current["version"],
                    new_version=None,
                    details={
                        "proposal_id": proposal_id,
                        "expected_version": expected_version,
                        "proposal_version": proposal["expected_version"],
                    },
                )
            raise VersionConflictError(
                f"Version conflict: expected {expected_version}, current {current['version']}"
            )

        if "phase" in changes and changes["phase"] != current["phase"]:
            approver = approved_by or proposal["approved_by"]
            if not approver:
                with self._connection:
                    self._record_audit(
                        event_type="approval_required",
                        project_id=project_id,
                        actor=proposal["actor"],
                        previous_version=current["version"],
                        new_version=None,
                        details={"proposal_id": proposal_id, "phase": changes["phase"]},
                    )
                raise ApprovalRequiredError("Explicit approval is required for phase transition")

        now = self._now()
        new_version = current["version"] + 1
        new_state = dict(current)
        new_state.update(changes)
        canonical = current["canonical_state"]
        canonical.setdefault("current_status", {})
        if "phase" in changes:
            canonical["current_status"]["current_phase"] = changes["phase"]
        if "status" in changes:
            canonical["current_status"]["status"] = changes["status"]
        if "completed_outputs" in changes:
            canonical.setdefault("knowledge", {})["outputs"] = changes["completed_outputs"]
        if "missing_items" in changes:
            canonical["current_status"]["blockers"] = changes["missing_items"]
        if "knowledge_items" in changes:
            canonical.setdefault("knowledge", {})["items"] = changes["knowledge_items"]
        if "discovery_output" in changes:
            canonical.setdefault("knowledge", {})["discovery_output"] = changes["discovery_output"]
        canonical.setdefault("audit", {})
        canonical["audit"].update({
            "last_updated_at": now,
            "last_updated_by": approved_by or proposal["actor"],
            "version": new_version,
        })
        new_state["canonical_state"] = canonical
        update_fields = {
            "phase": new_state["phase"],
            "status": new_state["status"],
            "completed_outputs": new_state["completed_outputs"],
            "missing_items": new_state["missing_items"],
            "required_user_action": new_state["required_user_action"],
            "expected_output": new_state["expected_output"],
            "completion_criteria": new_state["completion_criteria"],
            "next_recommended_action": new_state["next_recommended_action"],
            "canonical_state": new_state["canonical_state"],
        }
        assignments = ", ".join(f"{field} = ?" for field in update_fields)
        values = [
            self._json(value) if field in {
                "completed_outputs", "missing_items", "expected_output",
                "completion_criteria", "canonical_state",
            } else value
            for field, value in update_fields.items()
        ]
        values.extend([new_version, approved_by or proposal["actor"], now, project_id, expected_version])

        try:
            with self._connection:
                registry_row = self._connection.execute(
                    """
                    SELECT status, current_phase, version
                    FROM project_registry
                    WHERE project_id = ?
                    """,
                    (project_id,),
                ).fetchone()
                if registry_row is None:
                    raise RegistryStateMismatchError(
                        f"Project Registry entry not found: {project_id}"
                    )
                if (
                    registry_row["status"] != current["status"]
                    or registry_row["current_phase"] != current["phase"]
                ):
                    raise RegistryStateMismatchError(
                        "Project Registry and Project State are out of sync"
                    )

                registry_changes = {}
                if "phase" in changes:
                    registry_changes["current_phase"] = changes["phase"]
                if "status" in changes:
                    registry_changes["status"] = changes["status"]
                if registry_changes:
                    registry_changes["last_activity"] = now
                    registry_assignments = ", ".join(
                        f"{field} = ?" for field in registry_changes
                    )
                    registry_values = list(registry_changes.values())
                    registry_values.extend([now, project_id, registry_row["version"]])
                    registry_cursor = self._connection.execute(
                        f"""
                        UPDATE project_registry
                        SET {registry_assignments}, updated_at = ?, version = version + 1
                        WHERE project_id = ? AND version = ?
                        """,
                        tuple(registry_values),
                    )
                    if registry_cursor.rowcount != 1:
                        raise VersionConflictError(
                            "Project Registry version changed during State transition"
                        )
                    self._connection.execute(
                        """
                        INSERT INTO registry_audit
                            (event_type, project_id, actor, event_timestamp,
                             previous_version, new_version, details)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            "project_updated",
                            project_id,
                            approved_by or proposal["actor"],
                            now,
                            registry_row["version"],
                            registry_row["version"] + 1,
                            self._json({
                                "changes": registry_changes,
                                "source": "state_transition",
                                "state_proposal_id": proposal_id,
                            }),
                        ),
                    )
                cursor = self._connection.execute(
                    f"""
                    UPDATE project_state
                    SET {assignments}, version = ?, updated_by = ?, updated_at = ?
                    WHERE project_id = ? AND version = ?
                    """,
                    tuple(values),
                )
                if cursor.rowcount != 1:
                    self._record_audit(
                        event_type="version_conflict",
                        project_id=project_id,
                        actor=approved_by or proposal["actor"],
                        previous_version=current["version"],
                        new_version=None,
                        details={"proposal_id": proposal_id, "expected_version": expected_version},
                    )
                    raise VersionConflictError("State update lost its version race")
                self._connection.execute(
                    """
                    UPDATE state_update_proposals
                    SET status = 'committed', committed_at = ?, committed_by = ?, new_version = ?
                    WHERE proposal_id = ?
                    """,
                    (now, approved_by or proposal["actor"], new_version, proposal_id),
                )
                self._record_audit(
                    event_type="state_updated",
                    project_id=project_id,
                    actor=approved_by or proposal["actor"],
                    previous_version=current["version"],
                    new_version=new_version,
                    details={"proposal_id": proposal_id, "changes": changes},
                )
                return self.get_state(project_id)
        except VersionConflictError:
            raise
        except sqlite3.Error as exc:
            raise StateAdapterError("State storage unavailable during commit") from exc

    def audit_events(self, project_id: str | None = None) -> list[dict[str, Any]]:
        query = "SELECT * FROM state_audit"
        params: tuple[str, ...] = ()
        if project_id is not None:
            query += " WHERE project_id = ?"
            params = (project_id,)
        query += " ORDER BY audit_id"
        try:
            rows = self._connection.execute(query, params).fetchall()
        except sqlite3.Error as exc:
            raise StateAdapterError("State storage unavailable during audit read") from exc
        return [
            {**dict(row), "details": self._loads(row["details"], "audit details")}
            for row in rows
        ]
