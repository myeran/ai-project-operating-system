"""Project Instance Bootstrap Handler MVP.

This module coordinates Registry and State initialization only. It does not
route requests, run lifecycle work, activate Skills, or execute Workers.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

try:
    from .registry_adapter import ProjectMetadata, ProjectRegistryAdapter, RegistryError
    from .state_adapter import StateAdapter, StateAdapterError
except ImportError:  # Supports direct test-module execution.
    from registry_adapter import ProjectMetadata, ProjectRegistryAdapter, RegistryError
    from state_adapter import StateAdapter, StateAdapterError


class BootstrapError(RegistryError):
    """Project Instance initialization failed."""


@dataclass(frozen=True)
class BootstrapRequest:
    project_name: str
    owner: str
    os_version: str
    description: str = ""
    workspace_location: str | None = None
    project_context: dict[str, Any] | None = None
    actor: str = "bootstrap"


class ProjectInstanceBootstrapHandler:
    """Create a Registry entry and its initial canonical Project State."""

    def __init__(
        self,
        registry: ProjectRegistryAdapter,
        state: StateAdapter,
    ) -> None:
        self.registry = registry
        self.state = state

    @staticmethod
    def _validate_request(request: BootstrapRequest) -> None:
        for field_name in ("project_name", "owner", "os_version", "actor"):
            value = getattr(request, field_name)
            if not isinstance(value, str) or not value.strip():
                raise BootstrapError(f"{field_name} is required")
        if not isinstance(request.description, str):
            raise BootstrapError("description must be a string")
        if request.workspace_location is not None and not isinstance(
            request.workspace_location, str
        ):
            raise BootstrapError("workspace_location must be a string or null")
        if request.project_context is not None and not isinstance(request.project_context, dict):
            raise BootstrapError("project_context must be an object or null")

    @staticmethod
    def _default_workspace_location(project_name: str) -> str:
        slug = re.sub(r"[^a-z0-9]+", "-", project_name.casefold()).strip("-")
        return f"projects/{slug or 'new-project'}"

    def initialize(self, request: BootstrapRequest) -> dict[str, Any]:
        """Initialize one Project Instance in Discovery/proposed state."""

        self._validate_request(request)
        location = (
            request.workspace_location.strip()
            if request.workspace_location is not None
            else self._default_workspace_location(request.project_name)
        )
        if not location:
            raise BootstrapError("workspace_location cannot be empty")

        registry_entry = self.registry.create_project(
            ProjectMetadata(
                project_name=request.project_name.strip(),
                owner=request.owner.strip(),
                location=location,
                os_version=request.os_version.strip(),
                status="proposed",
                current_phase="Discovery",
            ),
            actor=request.actor,
        )

        project_id = registry_entry["project_id"]
        try:
            state = self.state.create_initial_state(
                project_id,
                initial_phase="Discovery",
                initial_status="proposed",
                actor=request.actor,
                description=request.description,
                project_context=request.project_context,
            )
        except (StateAdapterError, RegistryError) as exc:
            # Preserve evidence of the failed initialization and prevent the
            # partial Registry entry from appearing ready for use.
            try:
                self.registry.update_project_metadata(
                    project_id,
                    expected_version=registry_entry["version"],
                    actor=request.actor,
                    status="blocked",
                )
            except RegistryError as recovery_error:
                raise BootstrapError(
                    f"Bootstrap failed and recovery status update failed for {project_id}"
                ) from recovery_error
            raise BootstrapError(
                f"Bootstrap failed; Project Instance {project_id} is blocked"
            ) from exc

        return {
            "status": "initialized",
            "project_id": project_id,
            "os_version": registry_entry["os_version"],
            "workspace_location": registry_entry["location"],
            "registry": registry_entry,
            "state": state,
        }
