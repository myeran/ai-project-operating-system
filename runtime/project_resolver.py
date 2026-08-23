"""Project Resolver MVP.

The Resolver maps a Runtime Request to Registry metadata. It does not create
projects, load Project State, or make lifecycle decisions.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

try:
    from .registry_adapter import ProjectNotFoundError, ProjectRegistryAdapter, RegistryError
    from .runtime_gateway import RuntimeRequest
except ImportError:  # Supports direct test-module execution.
    from registry_adapter import ProjectNotFoundError, ProjectRegistryAdapter, RegistryError
    from runtime_gateway import RuntimeRequest


class ResolverError(RegistryError):
    """Project resolution failed at the Registry boundary."""


@dataclass(frozen=True)
class ResolutionResult:
    status: str
    project_id: str | None = None
    project_name: str | None = None
    current_phase: str | None = None
    current_status: str | None = None
    os_version: str | None = None
    location: str | None = None
    matches: list[dict[str, Any]] = field(default_factory=list)
    reason: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ProjectResolver:
    """Resolve a Runtime Request through the canonical Project Registry."""

    def __init__(self, registry: ProjectRegistryAdapter) -> None:
        self.registry = registry

    def resolve(self, request: RuntimeRequest) -> ResolutionResult:
        """Resolve by exact Project ID first, then exact normalized name."""

        if request.project_id:
            return self._resolve_by_id(request.project_id, request.project_name)
        if request.project_name:
            return self._resolve_by_name(request.project_name)
        return ResolutionResult(
            status="NOT_FOUND",
            reason="No project identifier or project name was provided",
        )

    def _resolve_by_id(
        self,
        project_id: str,
        requested_name: str | None,
    ) -> ResolutionResult:
        try:
            project = self.registry.get_project(project_id)
        except ProjectNotFoundError:
            return ResolutionResult(
                status="NOT_FOUND",
                project_id=project_id,
                reason="Project ID was not found in the Registry",
            )
        except RegistryError as exc:
            raise ResolverError("Registry unavailable during Project ID resolution") from exc

        if requested_name and requested_name.casefold().strip() != project["project_name"].casefold().strip():
            return ResolutionResult(
                status="AMBIGUOUS",
                project_id=project_id,
                project_name=project["project_name"],
                matches=[self._metadata(project)],
                reason="Project ID and project name identify different values",
            )
        return ResolutionResult(status="RESOLVED", **self._metadata(project))

    def _resolve_by_name(self, project_name: str) -> ResolutionResult:
        try:
            matches = self.registry.find_projects(project_name=project_name)
        except RegistryError as exc:
            raise ResolverError("Registry unavailable during Project name resolution") from exc

        if not matches:
            return ResolutionResult(
                status="NOT_FOUND",
                project_name=project_name,
                reason="Project name was not found in the Registry",
            )
        if len(matches) > 1:
            return ResolutionResult(
                status="AMBIGUOUS",
                project_name=project_name,
                matches=[self._metadata(project) for project in matches],
                reason="Multiple Project Instances match the requested name",
            )
        return ResolutionResult(status="RESOLVED", **self._metadata(matches[0]))

    @staticmethod
    def _metadata(project: dict[str, Any]) -> dict[str, Any]:
        return {
            "project_id": project["project_id"],
            "project_name": project["project_name"],
            "current_phase": project["current_phase"],
            "current_status": project["status"],
            "os_version": project["os_version"],
            "location": project["location"],
        }
