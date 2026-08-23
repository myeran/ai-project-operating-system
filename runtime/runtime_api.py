"""Client-independent Runtime API MVP.

The API is a thin HTTP boundary. All project actions pass through the existing
Gateway, Resolver, Bootstrap/State, and Orchestrator components.
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import urlparse

try:
    from .bootstrap_handler import BootstrapRequest, ProjectInstanceBootstrapHandler
    from .orchestrator import ProjectOrchestrator
    from .project_resolver import ProjectResolver
    from .registry_adapter import DuplicateProjectError, ProjectRegistryAdapter, RegistryError
    from .runtime_gateway import RuntimeEntryGateway
    from .state_adapter import (
        ApprovalRequiredError,
        ProjectStateNotFoundError,
        StateAdapter,
        StateAdapterError,
        ValidationError,
        VersionConflictError,
    )
except ImportError:  # Supports direct test-module execution.
    from bootstrap_handler import BootstrapRequest, ProjectInstanceBootstrapHandler
    from orchestrator import ProjectOrchestrator
    from project_resolver import ProjectResolver
    from registry_adapter import DuplicateProjectError, ProjectRegistryAdapter, RegistryError
    from runtime_gateway import RuntimeEntryGateway
    from state_adapter import (
        ApprovalRequiredError,
        ProjectStateNotFoundError,
        StateAdapter,
        StateAdapterError,
        ValidationError,
        VersionConflictError,
    )


class RuntimeAPIError(Exception):
    """Expected API-level error with an HTTP response."""

    def __init__(
        self,
        status_code: int,
        error_type: str,
        message: str,
        recovery: str,
        details: dict[str, Any] | None = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.error_type = error_type
        self.message = message
        self.recovery = recovery
        self.details = details or {}


class RuntimeAPIApplication:
    """Route API requests through the existing Runtime Control Plane."""

    def __init__(self, database: str | None = None):
        self.gateway = RuntimeEntryGateway()
        self.registry = ProjectRegistryAdapter(database)
        self.state = StateAdapter(database or self.registry.database)
        self.bootstrap = ProjectInstanceBootstrapHandler(self.registry, self.state)
        self.resolver = ProjectResolver(self.registry)
        self.orchestrator = ProjectOrchestrator(self.bootstrap, self.state)

    def close(self) -> None:
        self.state.close()
        self.registry.close()

    def handle(self, method: str, path: str, body: dict[str, Any] | None = None) -> tuple[int, dict[str, Any]]:
        parsed_path = urlparse(path).path
        body = body or {}
        try:
            if method == "POST" and parsed_path == "/projects/start":
                return 201, self._start_project(body)
            if method == "POST" and parsed_path == "/projects/continue":
                return 200, self._continue_project_by_identifier(body)
            if method == "POST" and parsed_path == "/projects/status":
                return 200, self._status_by_identifier(body)
            if method == "POST" and parsed_path == "/projects/navigator":
                return 200, self._navigator_by_identifier(body)
            if method == "POST" and parsed_path == "/projects/knowledge-summary":
                return 200, self._knowledge_summary_by_identifier(body)
            if method == "POST" and parsed_path == "/projects/checkpoint":
                return 200, self._checkpoint_by_identifier(body)
            if method == "GET" and parsed_path.startswith("/projects/") and parsed_path.endswith("/proposals"):
                project_id = parsed_path[len("/projects/") : -len("/proposals")].strip("/")
                if not project_id:
                    raise RuntimeAPIError(400, "INVALID_REQUEST", "Project ID is required", "Provide a valid Project ID.")
                return 200, self._pending_proposals(project_id)
            if method == "POST" and parsed_path.startswith("/proposals/") and parsed_path.endswith("/approve"):
                proposal_id = parsed_path[len("/proposals/") : -len("/approve")].strip("/")
                if not proposal_id:
                    raise RuntimeAPIError(400, "INVALID_REQUEST", "Proposal ID is required", "Provide a valid Proposal ID.")
                return 200, self._approve_proposal(proposal_id, body)
            if method == "POST" and parsed_path.startswith("/proposals/") and parsed_path.endswith("/commit"):
                proposal_id = parsed_path[len("/proposals/") : -len("/commit")].strip("/")
                if not proposal_id:
                    raise RuntimeAPIError(400, "INVALID_REQUEST", "Proposal ID is required", "Provide a valid Proposal ID.")
                return 200, self._commit_proposal(proposal_id, body)
            if method == "POST" and parsed_path.startswith("/projects/") and parsed_path.endswith("/discovery"):
                project_id = parsed_path[len("/projects/") : -len("/discovery")].strip("/")
                if not project_id:
                    raise RuntimeAPIError(400, "INVALID_REQUEST", "Project ID is required", "Provide a valid Project ID.")
                return 200, self._run_discovery(project_id, body)
            if method == "POST" and parsed_path.startswith("/projects/") and parsed_path.endswith("/continue"):
                project_id = parsed_path[len("/projects/") : -len("/continue")].strip("/")
                if not project_id:
                    raise RuntimeAPIError(400, "INVALID_REQUEST", "Project ID is required", "Provide a valid Project ID.")
                return 200, self._continue_project(project_id)
            if method == "GET" and parsed_path.startswith("/projects/") and parsed_path.endswith("/status"):
                project_id = parsed_path[len("/projects/") : -len("/status")].strip("/")
                if not project_id:
                    raise RuntimeAPIError(400, "INVALID_REQUEST", "Project ID is required", "Provide a valid Project ID.")
                return 200, self._status(project_id)
            if method == "GET" and parsed_path.startswith("/projects/") and parsed_path.endswith("/navigator"):
                project_id = parsed_path[len("/projects/") : -len("/navigator")].strip("/")
                if not project_id:
                    raise RuntimeAPIError(400, "INVALID_REQUEST", "Project ID is required", "Provide a valid Project ID.")
                return 200, self._navigator(project_id)
            if method == "PUT" and "/knowledge-items/" in parsed_path:
                prefix, item_id = parsed_path.split("/knowledge-items/", 1)
                project_id = prefix[len("/projects/") :].strip("/")
                if not project_id or not item_id:
                    raise RuntimeAPIError(400, "INVALID_REQUEST", "Project ID and item ID are required", "Provide both identifiers.")
                return 200, self._update_knowledge_item(project_id, item_id, body)
            raise RuntimeAPIError(404, "NOT_FOUND", "Endpoint not found", "Use the documented Runtime API endpoints.")
        except RuntimeAPIError as exc:
            return exc.status_code, self._error_payload(exc)
        except DuplicateProjectError as exc:
            return 409, self._error_payload(
                RuntimeAPIError(409, "DUPLICATE_PROJECT", str(exc), "Continue the existing project or choose a different name.")
            )
        except VersionConflictError as exc:
            return 409, self._error_payload(
                RuntimeAPIError(409, "VERSION_CONFLICT", str(exc), "Reload the proposal and current Project State before retrying.")
            )
        except ApprovalRequiredError as exc:
            return 409, self._error_payload(
                RuntimeAPIError(409, "APPROVAL_REQUIRED", str(exc), "Approve the proposal before committing it.")
            )
        except (ProjectStateNotFoundError,) as exc:
            return 404, self._error_payload(
                RuntimeAPIError(404, "PROJECT_NOT_FOUND", str(exc), "Verify the Project ID and try again.")
            )
        except ValidationError as exc:
            return 400, self._error_payload(
                RuntimeAPIError(400, "INVALID_REQUEST", str(exc), "Correct the request and try again.")
            )
        except (RegistryError, StateAdapterError) as exc:
            return 500, self._error_payload(
                RuntimeAPIError(500, "RUNTIME_FAILURE", str(exc), "No project action was completed; inspect runtime storage and retry.")
            )
        except Exception as exc:  # Fail closed at the client boundary.
            return 500, self._error_payload(
                RuntimeAPIError(500, "RUNTIME_FAILURE", "Runtime operation failed", "No project action was completed; retry after checking the runtime.")
            )

    def _start_project(self, body: dict[str, Any]) -> dict[str, Any]:
        project_name = body.get("project_name")
        owner = body.get("owner")
        description = body.get("description", "")
        if not isinstance(project_name, str) or not project_name.strip():
            raise RuntimeAPIError(400, "INVALID_REQUEST", "project_name is required", "Provide a project_name.")
        if not isinstance(owner, str) or not owner.strip():
            raise RuntimeAPIError(400, "INVALID_REQUEST", "owner is required", "Provide an owner.")
        if not isinstance(description, str):
            raise RuntimeAPIError(400, "INVALID_REQUEST", "description must be a string", "Remove description or provide text.")

        context_fields = {
            "project_type": body.get("project_type"),
            "project_goal": body.get("project_goal"),
            "expected_outcome": body.get("expected_outcome"),
            "current_stage": body.get("current_stage"),
        }
        invalid_context = [
            field for field, value in context_fields.items()
            if not isinstance(value, str) or not value.strip()
        ]
        if invalid_context:
            question = (
                "What type of project is this? Choose: Product, Research, Test, "
                "Process Improvement, or Other."
            )
            raise RuntimeAPIError(
                422,
                "PROJECT_CONTEXT_REQUIRED",
                "Explicit project context is required before Discovery starts.",
                "Provide the missing project context and retry.",
                details={
                    "missing_context": invalid_context,
                    "clarification_question": question,
                    "allowed_project_types": ["Product", "Research", "Test", "Process Improvement", "Other"],
                },
            )
        project_context = {key: value.strip() for key, value in context_fields.items()}

        request = self.gateway.receive(
            f"Start Project:{project_name.strip()}",
            user_id=owner.strip(),
            source_client="runtime-api",
        )
        if request.intent != "START_PROJECT":
            raise RuntimeAPIError(400, "INVALID_REQUEST", "Request was not classified as START_PROJECT", "Provide a project creation request.")
        existing = self.resolver.resolve(request)
        if existing.status == "RESOLVED":
            raise RuntimeAPIError(
                409,
                "DUPLICATE_PROJECT",
                f"Project already exists: {existing.project_name}",
                f"Continue project {existing.project_id} or choose a different name.",
            )
        if existing.status == "AMBIGUOUS":
            raise RuntimeAPIError(409, "AMBIGUOUS_PROJECT", "Multiple matching projects exist", "Choose the intended existing project.")

        orchestration = self.orchestrator.start_project(
            BootstrapRequest(
                project_name=project_name.strip(),
                owner=owner.strip(),
                description=description,
                os_version=body.get("os_version", "v1.0"),
                workspace_location=body.get("workspace_location"),
                project_context=project_context,
                actor="runtime-api",
            ),
            activate_skill=True,
        )
        response = self._guidance_response(request, orchestration, orchestration.get("initialized"))
        response["knowledge_summary"] = {
            "project_id": response["project_id"],
            "state_version": response.get("state_version", 1),
            "items": (orchestration.get("state_update_proposal") or {}).get("changes", {}).get("knowledge_items", []),
        }
        return response

    def _continue_project(self, project_id: str) -> dict[str, Any]:
        request = self.gateway.receive(
            "Continue Project",
            user_id="runtime-api-user",
            source_client="runtime-api",
            project_id=project_id,
        )
        if request.intent != "CONTINUE_PROJECT":
            raise RuntimeAPIError(400, "INVALID_REQUEST", "Request was not classified as CONTINUE_PROJECT", "Provide a continuation request.")
        resolved = self.resolver.resolve(request)
        if resolved.status != "RESOLVED":
            raise RuntimeAPIError(404, "PROJECT_NOT_FOUND", "Project was not found", "Verify the Project ID and try again.")
        response = self._guidance_response(request, self.orchestrator.orchestrate(resolved))
        response["knowledge_summary"] = self._knowledge_summary(project_id)
        return response

    def _continue_project_by_identifier(self, body: dict[str, Any]) -> dict[str, Any]:
        request, resolved = self._resolve_by_identifier(body, "Continue Project", "CONTINUE_PROJECT")
        response = self._guidance_response(request, self.orchestrator.orchestrate(resolved))
        response["knowledge_summary"] = self._knowledge_summary(resolved.project_id or "")
        return response

    def _status_by_identifier(self, body: dict[str, Any]) -> dict[str, Any]:
        request, resolved = self._resolve_by_identifier(body, "Project Status", "STATUS")
        state = self.state.get_state(resolved.project_id or "")
        response = self._guidance_response(request, self.orchestrator.orchestrate(resolved))
        response["project"] = resolved.to_dict()
        response["state"] = state
        response["knowledge_summary"] = self._knowledge_summary(resolved.project_id or "", state=state)
        return response

    def _navigator_by_identifier(self, body: dict[str, Any]) -> dict[str, Any]:
        _, resolved = self._resolve_by_identifier(body, "Project Status", "STATUS")
        return self.orchestrator.project_navigator(resolved)

    def _navigator(self, project_id: str) -> dict[str, Any]:
        request = self.gateway.receive("Project Status", user_id="runtime-api-user", source_client="runtime-api", project_id=project_id)
        resolved = self.resolver.resolve(request)
        if resolved.status != "RESOLVED":
            raise RuntimeAPIError(404, "PROJECT_NOT_FOUND", "Project was not found", "Verify the Project ID and try again.")
        return self.orchestrator.project_navigator(resolved)

    def _knowledge_summary_by_identifier(self, body: dict[str, Any]) -> dict[str, Any]:
        _, resolved = self._resolve_by_identifier(body, "Project Status", "STATUS")
        return self._knowledge_summary(resolved.project_id or "")

    def _knowledge_summary(self, project_id: str, *, state: dict[str, Any] | None = None) -> dict[str, Any]:
        state = state or self.state.get_state(project_id)
        items = list(state.get("knowledge_items") or [])
        # A newly activated Skill is proposal-only. Expose its proposed items so
        # the UI can edit them before the first checkpoint without owning state.
        if not items:
            for proposal in reversed(self.state.list_proposals(project_id, status="pending")):
                proposed = proposal.get("changes", {}).get("knowledge_items")
                if isinstance(proposed, list):
                    items = proposed
                    break
        counts = {status: sum(1 for item in items if item.get("status") == status) for status in ("open", "approved", "needs_update")}
        return {
            "project_id": project_id,
            "state_version": state["version"],
            "items": items,
            "counts": counts,
            "completed": [item["question"] for item in items if item.get("status") == "approved"],
            "open": [item["question"] for item in items if item.get("status") == "open"],
            "needs_update": [item["question"] for item in items if item.get("status") == "needs_update"],
            "next_step": "ענה על השאלות הפתוחות או אשר תשובות מוכנות." if counts["open"] or counts["needs_update"] else "סיכום הידע מאושר; אפשר להמשיך לשלב הבא.",
        }

    def _update_knowledge_item(self, project_id: str, item_id: str, body: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(body, dict):
            raise RuntimeAPIError(400, "INVALID_REQUEST", "Request body must be an object", "Provide an answer and status.")
        answer = body.get("answer")
        status = body.get("status", "open")
        actor = body.get("actor", "local-user")
        if not isinstance(answer, str):
            raise RuntimeAPIError(400, "INVALID_REQUEST", "answer must be a string", "Provide the updated answer text.")
        if status not in {"open", "approved", "needs_update"}:
            raise RuntimeAPIError(400, "INVALID_REQUEST", "Unsupported knowledge status", "Use open, approved, or needs_update.")
        state = self.state.get_state(project_id)
        items = self._knowledge_summary(project_id, state=state)["items"]
        target = next((item for item in items if item.get("id") == item_id), None)
        if target is None:
            raise RuntimeAPIError(404, "KNOWLEDGE_ITEM_NOT_FOUND", "Knowledge item was not found", "Reload the project summary and choose an existing question.")
        from datetime import datetime, timezone
        updated = [dict(item) for item in items]
        for item in updated:
            if item["id"] == item_id:
                item.update({"answer": answer.strip(), "status": status, "updated_at": datetime.now(timezone.utc).isoformat()})
        proposal = self.state.propose_state_update(project_id, {"knowledge_items": updated}, actor=actor)
        self.state.approve_state_proposal(proposal["proposal_id"], approver=actor)
        committed = self.state.commit_state_update(proposal["proposal_id"], expected_version=proposal["expected_version"], approved_by=actor, require_approval=True)
        return {"project_id": project_id, "item": next(item for item in committed["knowledge_items"] if item["id"] == item_id), "state_version": committed["version"], "knowledge_summary": self._knowledge_summary(project_id, state=committed)}

    def _checkpoint_by_identifier(self, body: dict[str, Any]) -> dict[str, Any]:
        request, resolved = self._resolve_by_identifier(body, "Project Status", "STATUS")
        state = self.state.get_state(resolved.project_id or "")
        summary = self._knowledge_summary(resolved.project_id or "", state=state)
        items = body.get("items", summary["items"])
        if not isinstance(items, list):
            raise RuntimeAPIError(400, "INVALID_REQUEST", "items must be a list", "Provide the knowledge summary items.")
        actor = body.get("actor", "local-user")
        proposal = self.state.propose_state_update(resolved.project_id or "", {"knowledge_items": items}, actor=actor)
        self.state.approve_state_proposal(proposal["proposal_id"], approver=actor)
        committed = self.state.commit_state_update(proposal["proposal_id"], expected_version=proposal["expected_version"], approved_by=actor, require_approval=True)
        return {"project_id": resolved.project_id, "saved": True, "state_version": committed["version"], "knowledge_summary": self._knowledge_summary(resolved.project_id or "", state=committed)}

    def _resolve_by_identifier(
        self,
        body: dict[str, Any],
        user_request: str,
        expected_intent: str,
    ) -> tuple[Any, Any]:
        if not isinstance(body, dict):
            raise RuntimeAPIError(400, "INVALID_REQUEST", "Request body must be an object", "Provide project_name or project_id.")

        project_name = body.get("project_name")
        project_id = body.get("project_id")
        message = body.get("message")
        if project_name is not None and (not isinstance(project_name, str) or not project_name.strip()):
            raise RuntimeAPIError(400, "INVALID_REQUEST", "project_name must be a non-empty string", "Provide a valid project_name.")
        if project_id is not None and (not isinstance(project_id, str) or not project_id.strip()):
            raise RuntimeAPIError(400, "INVALID_REQUEST", "project_id must be a non-empty string", "Provide a valid project_id.")
        if message is not None and (not isinstance(message, str) or not message.strip()):
            raise RuntimeAPIError(400, "INVALID_REQUEST", "message must be a non-empty string", "Provide the user's project message.")
        if not project_name and not project_id:
            raise RuntimeAPIError(400, "INVALID_REQUEST", "project_name or project_id is required", "Provide a project identifier.")

        # Keep the canonical intent prefix so the Runtime Gateway can classify
        # the request. The free-form message travels as conversation_input so
        # it cannot be mistaken for a project name during resolution.
        request_text = user_request
        if project_name:
            request_text = f"{request_text}: {project_name.strip()}"
        request = self.gateway.receive(
            request_text,
            user_id=body.get("owner", "runtime-api-user"),
            source_client="runtime-api",
            project_id=project_id.strip() if project_id else None,
            conversation_input=message.strip() if message else None,
        )
        if request.intent != expected_intent:
            raise RuntimeAPIError(400, "INVALID_REQUEST", f"Request was not classified as {expected_intent}", "Provide a valid project request.")
        resolved = self.resolver.resolve(request)
        if resolved.status == "NOT_FOUND":
            raise RuntimeAPIError(404, "PROJECT_NOT_FOUND", "Project was not found", "Verify the project name or ID and try again.")
        if resolved.status == "AMBIGUOUS":
            raise RuntimeAPIError(
                409,
                "AMBIGUOUS_PROJECT",
                "Multiple projects match the request",
                "Choose one of the matching Project Instances.",
                details={"matches": resolved.matches},
            )
        return request, resolved

    def _run_discovery(self, project_id: str, body: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(body, dict):
            raise RuntimeAPIError(400, "INVALID_REQUEST", "Discovery context must be an object", "Provide a JSON object.")
        request = self.gateway.receive(
            "Continue Discovery",
            user_id=body.get("owner", "runtime-api-user"),
            source_client="runtime-api",
            project_id=project_id,
        )
        if request.intent != "VALIDATION_REQUEST":
            raise RuntimeAPIError(400, "INVALID_REQUEST", "Request was not classified as a Discovery request", "Request Discovery explicitly.")
        resolved = self.resolver.resolve(request)
        if resolved.status != "RESOLVED":
            raise RuntimeAPIError(404, "PROJECT_NOT_FOUND", "Project was not found", "Verify the Project ID and try again.")
        result = self.orchestrator.activate_current_phase(resolved, body, actor="runtime-api")
        if result.get("discovery_status") == "FAILED":
            raise RuntimeAPIError(409, "DISCOVERY_BLOCKED", result.get("error", "Discovery was blocked"), "Resolve the blocking condition and retry.")
        return self._guidance_response(request, result)

    def _pending_proposals(self, project_id: str) -> dict[str, Any]:
        self.state.get_state(project_id)
        return {
            "project_id": project_id,
            "proposals": self.state.list_proposals(project_id, status="pending"),
        }

    def _approve_proposal(self, proposal_id: str, body: dict[str, Any]) -> dict[str, Any]:
        approver = body.get("approver") if isinstance(body, dict) else None
        if not isinstance(approver, str) or not approver.strip():
            raise RuntimeAPIError(400, "INVALID_REQUEST", "approver is required", "Provide an approver.")
        proposal = self.state.approve_state_proposal(proposal_id, approver=approver.strip())
        return {"proposal": proposal, "status": proposal["status"]}

    def _commit_proposal(self, proposal_id: str, body: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(body, dict):
            body = {}
        proposal = self.state.get_proposal(proposal_id)
        approver = body.get("approver") or proposal.get("approved_by")
        if not isinstance(approver, str) or not approver.strip():
            raise RuntimeAPIError(400, "INVALID_REQUEST", "approver is required", "Provide the approver used for approval.")
        expected_version = body.get("expected_version", proposal["expected_version"])
        if not isinstance(expected_version, int):
            raise RuntimeAPIError(400, "INVALID_REQUEST", "expected_version must be an integer", "Provide the proposal version.")
        state = self.state.commit_state_update(
            proposal_id,
            expected_version=expected_version,
            approved_by=approver.strip(),
            require_approval=True,
        )
        committed = self.state.get_proposal(proposal_id)
        return {"proposal": committed, "state": state, "status": committed["status"]}

    def _status(self, project_id: str) -> dict[str, Any]:
        request = self.gateway.receive(
            "Project Status",
            user_id="runtime-api-user",
            source_client="runtime-api",
            project_id=project_id,
        )
        resolved = self.resolver.resolve(request)
        if resolved.status != "RESOLVED":
            raise RuntimeAPIError(404, "PROJECT_NOT_FOUND", "Project was not found", "Verify the Project ID and try again.")
        orchestration = self.orchestrator.orchestrate(resolved)
        state = self.state.get_state(project_id)
        response = self._guidance_response(request, orchestration)
        response["project"] = resolved.to_dict()
        response["state"] = state
        response["knowledge_summary"] = self._knowledge_summary(project_id, state=state)
        return response

    @staticmethod
    def _guidance_response(
        request: Any,
        orchestration: dict[str, Any],
        initialized: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        guidance = orchestration["phase_guidance"]
        return {
            "request_id": request.request_id,
            "correlation_id": request.correlation_id,
            "project_id": orchestration.get("project_id"),
            "current_phase": orchestration.get("current_phase"),
            "status": orchestration.get("status"),
            "completed": guidance["completed"],
            "missing": guidance["missing"],
            "required_user_action": guidance["required_user_action"],
            "expected_output": guidance["expected_output"],
            "completion_criteria": guidance["completion_criteria"],
            "next_recommended_action": guidance["next_recommended_action"],
            "phase_guidance": guidance,
            "state_update_proposal": orchestration.get("state_update_proposal"),
            "initialized": initialized is not None,
            "discovery_status": orchestration.get("discovery_status"),
            "discovery_output": orchestration.get("discovery_output"),
            "state_committed": orchestration.get("state_committed", False),
        }

    @staticmethod
    def _error_payload(error: RuntimeAPIError) -> dict[str, Any]:
        return {
            "error_type": error.error_type,
            "message": error.message,
            "recovery_suggestion": error.recovery,
            "fail_closed": True,
            **error.details,
        }


class RuntimeAPIHandler(BaseHTTPRequestHandler):
    """HTTP adapter for RuntimeAPIApplication."""

    application: RuntimeAPIApplication | None = None

    def _dispatch(self, method: str) -> None:
        if self.application is None:
            self._write_json(500, {"error_type": "RUNTIME_FAILURE", "message": "API is not configured", "fail_closed": True})
            return
        body: dict[str, Any] | None = None
        if method in {"POST", "PUT"}:
            try:
                length = int(self.headers.get("Content-Length", "0"))
                raw = self.rfile.read(length) if length else b"{}"
                body = json.loads(raw.decode("utf-8"))
                if not isinstance(body, dict):
                    raise ValueError("JSON body must be an object")
            except (ValueError, json.JSONDecodeError) as exc:
                self._write_json(400, {"error_type": "INVALID_REQUEST", "message": str(exc), "fail_closed": True})
                return
        status_code, payload = self.application.handle(method, self.path, body)
        self._write_json(status_code, payload)

    def _write_json(self, status_code: int, payload: dict[str, Any]) -> None:
        encoded = json.dumps(payload, ensure_ascii=False, default=str).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_POST(self) -> None:  # noqa: N802
        self._dispatch("POST")

    def do_PUT(self) -> None:  # noqa: N802
        self._dispatch("PUT")

    def do_GET(self) -> None:  # noqa: N802
        self._dispatch("GET")

    def log_message(self, format: str, *args: Any) -> None:
        return


def serve(host: str = "127.0.0.1", port: int = 8765, database: str | None = None) -> None:
    """Run the minimal Runtime API server."""

    application = RuntimeAPIApplication(database)
    RuntimeAPIHandler.application = application
    server = ThreadingHTTPServer((host, port), RuntimeAPIHandler)
    try:
        server.serve_forever()
    finally:
        server.server_close()
        application.close()


if __name__ == "__main__":
    serve()
