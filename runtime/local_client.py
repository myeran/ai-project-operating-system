"""Local natural-language client for the Runtime API.

The client only translates user text into Runtime API requests. It never reads
project storage or performs lifecycle decisions itself.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class LocalClientError(Exception):
    """A local client request could not be completed."""


@dataclass(frozen=True)
class ParsedCommand:
    intent: str
    project_name: str | None = None


class LocalProjectClient:
    """Translate natural-language commands into calls to the local Runtime API."""

    def __init__(self, base_url: str = "http://127.0.0.1:8765", transport: Callable[..., dict[str, Any]] | None = None):
        self.base_url = base_url.rstrip("/")
        self._transport = transport or self._request

    def execute(self, command: str, *, context: dict[str, Any] | None = None) -> dict[str, Any]:
        parsed = self.parse(command)
        if parsed.intent == "START_PROJECT":
            payload = {"project_name": parsed.project_name, "owner": "local-user"}
            if context:
                payload.update(context)
            return self._transport("POST", "/projects/start", payload)
        if parsed.intent == "CONTINUE_PROJECT":
            return self._transport("POST", "/projects/continue", {"project_name": parsed.project_name})
        if parsed.intent == "PROJECT_STATUS":
            return self._transport("POST", "/projects/status", {"project_name": parsed.project_name})
        raise LocalClientError("The request is unclear. Use Start Project, Continue Project, or Project Status.")

    @staticmethod
    def parse(command: str) -> ParsedCommand:
        if not isinstance(command, str) or not command.strip():
            raise LocalClientError("A project request is required.")
        text = command.strip()
        patterns = (
            ("START_PROJECT", r"^start(?:\s+new)?\s+project\s*:\s*(.+)$"),
            ("CONTINUE_PROJECT", r"^(?:continue|resume)\s+project\s*:\s*(.+)$"),
            ("PROJECT_STATUS", r"^project\s+status\s*:\s*(.+)$"),
        )
        for intent, pattern in patterns:
            match = re.match(pattern, text, flags=re.IGNORECASE)
            if match and match.group(1).strip():
                return ParsedCommand(intent, match.group(1).strip())
        raise LocalClientError("Unrecognized project request.")

    def _request(self, method: str, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        request = Request(
            f"{self.base_url}{path}",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method=method,
        )
        try:
            with urlopen(request, timeout=10) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            try:
                return json.loads(exc.read().decode("utf-8"))
            except json.JSONDecodeError:
                raise LocalClientError(f"Runtime API returned HTTP {exc.code}") from exc
        except URLError as exc:
            raise LocalClientError(f"Local Runtime API is unavailable: {exc.reason}") from exc


def format_response(response: dict[str, Any]) -> str:
    """Render the canonical guidance fields without changing their meaning."""

    fields = (
        ("Project", response.get("project_id")),
        ("Phase", response.get("current_phase")),
        ("Status", response.get("status")),
        ("Completed", response.get("completed")),
        ("Missing", response.get("missing")),
        ("Required User Action", response.get("required_user_action")),
        ("Expected Output", response.get("expected_output")),
        ("Completion Criteria", response.get("completion_criteria")),
        ("Next Recommended Action", response.get("next_recommended_action")),
    )
    return "\n".join(f"{label}: {value}" for label, value in fields)


def main() -> int:
    command = " ".join(sys.argv[1:]).strip()
    if not command:
        command = input("Project command: ").strip()
    try:
        result = LocalProjectClient().execute(command)
    except LocalClientError as exc:
        print(str(exc))
        return 1
    print(format_response(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
