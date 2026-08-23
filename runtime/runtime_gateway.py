"""Runtime Entry Gateway MVP.

The Gateway validates the request envelope and performs initial intent
classification only. It does not resolve projects, load state, or execute work.
"""

from __future__ import annotations

import re
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


class GatewayError(Exception):
    """Base error for Runtime Entry Gateway failures."""


class InvalidRuntimeRequestError(GatewayError):
    """The request envelope is invalid."""


INTENTS = {
    "START_PROJECT",
    "CONTINUE_PROJECT",
    "STATUS",
    "VALIDATION_REQUEST",
    "EXECUTION_REQUEST",
    "AMBIGUOUS",
}


@dataclass(frozen=True)
class RuntimeRequest:
    request_id: str
    correlation_id: str
    user_id: str
    user_request: str
    timestamp: str
    source_client: str
    project_id: str | None = None
    project_name: str | None = None
    conversation_input: str | None = None
    intent: str = "AMBIGUOUS"
    request_type: str = "PROJECT_REQUEST"
    workspace_context: str | None = None


class RuntimeEntryGateway:
    """Validate and classify project-related user requests."""

    def receive(
        self,
        user_request: str,
        *,
        user_id: str = "local-user",
        source_client: str = "local-runtime",
        correlation_id: str | None = None,
        project_id: str | None = None,
        conversation_input: str | None = None,
        workspace_context: str | None = None,
    ) -> RuntimeRequest:
        self._validate_text(user_request, "user_request")
        self._validate_text(user_id, "user_id")
        self._validate_text(source_client, "source_client")
        if correlation_id is not None:
            self._validate_text(correlation_id, "correlation_id")
        if project_id is not None:
            self._validate_text(project_id, "project_id")
        if conversation_input is not None:
            self._validate_text(conversation_input, "conversation_input")

        intent, project_name, request_type = self._classify(user_request)
        return RuntimeRequest(
            request_id=str(uuid.uuid4()),
            correlation_id=correlation_id or str(uuid.uuid4()),
            user_id=user_id.strip(),
            user_request=user_request.strip(),
            timestamp=datetime.now(timezone.utc).isoformat(),
            source_client=source_client.strip(),
            project_id=project_id.strip() if project_id else None,
            conversation_input=conversation_input.strip() if conversation_input else None,
            project_name=project_name,
            intent=intent,
            request_type=request_type,
            workspace_context=workspace_context,
        )

    @staticmethod
    def _validate_text(value: str, field_name: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise InvalidRuntimeRequestError(f"{field_name} is required")

    @classmethod
    def _classify(cls, user_request: str) -> tuple[str, str | None, str]:
        text = " ".join(user_request.casefold().split())

        project_name = cls._extract_project_name(
            user_request,
            patterns=(r"^start\s+project\s*:\s*(.+)$", r"^continue\s+project\s*:\s*(.+)$"),
        )
        if cls._matches(text, "start new project") or cls._matches(text, "start project"):
            return "START_PROJECT", project_name, "PROJECT_START"
        if cls._matches(text, "i have a new project idea") or cls._matches(
            text, "help me start a new project"
        ):
            return "START_PROJECT", project_name, "PROJECT_START"

        continue_name = cls._extract_project_name(
            user_request,
            patterns=(r"^resume\s+project\s*:\s*(.+)$", r"^continue\s+project\s*:\s*(.+)$"),
        )
        if cls._matches(text, "continue project") or cls._matches(text, "resume project"):
            return "CONTINUE_PROJECT", continue_name, "PROJECT_CONTINUE"

        if any(token in text for token in ("project status", "current phase", "what is next", "status")):
            status_name = cls._extract_project_name(
                user_request,
                patterns=(r"^project\s+status\s*:\s*(.+)$", r"^status\s*:\s*(.+)$"),
            )
            return "STATUS", status_name, "PROJECT_STATUS"

        if any(token in text for token in ("validate progress", "run validation", "check open questions", "continue discovery")):
            return "VALIDATION_REQUEST", None, "PROJECT_VALIDATION"

        if any(token in text for token in ("execute", "run code", "write code", "implement", "build")):
            return "EXECUTION_REQUEST", None, "PROJECT_EXECUTION"

        return "AMBIGUOUS", None, "PROJECT_REQUEST"

    @staticmethod
    def _matches(text: str, phrase: str) -> bool:
        return text == phrase or text.startswith(f"{phrase}:")

    @staticmethod
    def _extract_project_name(user_request: str, *, patterns: tuple[str, ...]) -> str | None:
        for pattern in patterns:
            match = re.match(pattern, user_request.strip(), flags=re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                return name or None
        return None

    @staticmethod
    def to_dict(request: RuntimeRequest) -> dict[str, Any]:
        """Return the canonical request payload for downstream components."""

        return asdict(request)
