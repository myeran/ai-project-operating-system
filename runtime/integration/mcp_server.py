"""Small MCP-over-HTTP adapter for the existing Runtime API.

This module deliberately contains no project or lifecycle logic. Every tool
call is translated into one request to the Runtime HTTP API.
"""

from __future__ import annotations

import json
import os
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


RUNTIME_API_URL = os.environ.get("RUNTIME_API_URL", "http://127.0.0.1:8765").rstrip("/")


class RuntimeAPIClient:
    def __init__(self, base_url: str = RUNTIME_API_URL):
        self.base_url = base_url.rstrip("/")

    def post(self, path: str, payload: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        return self.request("POST", path, payload)

    def request(self, method: str, path: str, payload: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        request = Request(
            f"{self.base_url}{path}",
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method=method,
        )
        try:
            with urlopen(request, timeout=15) as response:
                return response.status, json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            return exc.code, json.loads(exc.read().decode("utf-8"))
        except (URLError, TimeoutError) as exc:
            return 503, {
                "error_type": "RUNTIME_UNAVAILABLE",
                "message": "The Runtime API is unavailable.",
                "recovery_suggestion": "Start the verified Runtime API and retry.",
                "fail_closed": True,
                "details": str(exc),
            }


TOOLS = [
    {
        "name": "project_navigator",
        "description": "Read-only roadmap of all lifecycle phases, current progress, missing items, responsible Skills, and the next Skill through the verified Runtime.",
        "inputSchema": {"type": "object", "properties": {"project_id": {"type": "string"}, "project_name": {"type": "string"}}, "additionalProperties": False},
    },
    {
        "name": "start_project",
        "description": "Start a new project through the verified AI Project Operating System Runtime. This creates the canonical project state and returns Discovery guidance; it does not commit proposals automatically.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_name": {"type": "string", "description": "Unique project name."},
                "owner": {"type": "string", "description": "Project owner."},
                "description": {"type": "string"},
                "project_type": {"type": "string", "description": "Product, Research, Test, Process Improvement, or Other."},
                "project_goal": {"type": "string"},
                "expected_outcome": {"type": "string"},
                "current_stage": {"type": "string"},
            },
            "required": ["project_name", "owner", "project_type", "project_goal", "expected_outcome", "current_stage"],
            "additionalProperties": False,
        },
    },
    {
        "name": "continue_project",
        "description": "Continue an existing project through the verified Runtime. Use either project_name or project_id.",
        "inputSchema": {
            "type": "object",
                "properties": {
                    "project_name": {"type": "string"},
                    "project_id": {"type": "string"},
                    "message": {"type": "string", "description": "The user's free-form message for the current project."},
                },
            "additionalProperties": False,
        },
    },
    {
        "name": "project_status",
        "description": "Get the canonical status, phase guidance, and persisted state for an existing project through the verified Runtime.",
        "inputSchema": {
            "type": "object",
                "properties": {
                    "project_name": {"type": "string"},
                    "project_id": {"type": "string"},
                    "message": {"type": "string", "description": "The user's free-form message for the current project."},
                },
            "additionalProperties": False,
        },
    },
    {
        "name": "project_knowledge_summary",
        "description": "Read the structured project questions, answers, statuses, and next step through the Runtime.",
        "inputSchema": {"type": "object", "properties": {"project_id": {"type": "string"}, "project_name": {"type": "string"}}, "additionalProperties": False},
    },
    {
        "name": "update_knowledge_item",
        "description": "Replace one existing project answer and status through the Runtime; never creates a duplicate question.",
        "inputSchema": {"type": "object", "required": ["project_id", "item_id", "answer", "status"], "properties": {"project_id": {"type": "string"}, "item_id": {"type": "string"}, "answer": {"type": "string"}, "status": {"type": "string", "enum": ["open", "approved", "needs_update"]}, "actor": {"type": "string"}}, "additionalProperties": False},
    },
    {
        "name": "save_project_checkpoint",
        "description": "Persist the current structured project knowledge checkpoint and return the next step.",
        "inputSchema": {"type": "object", "required": ["project_id"], "properties": {"project_id": {"type": "string"}, "project_name": {"type": "string"}, "items": {"type": "array"}, "actor": {"type": "string"}}, "additionalProperties": False},
    },
]


class MCPApplication:
    def __init__(self, runtime_api_url: str = RUNTIME_API_URL):
        self.runtime = RuntimeAPIClient(runtime_api_url)

    def handle(self, message: dict[str, Any]) -> dict[str, Any] | None:
        method = message.get("method")
        request_id = message.get("id")
        if method == "notifications/initialized":
            return None
        if method == "initialize":
            return self._result(request_id, {
                "protocolVersion": "2025-06-18",
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "ai-project-operating-system-runtime", "version": "0.1.0"},
            })
        if method == "tools/list":
            return self._result(request_id, {"tools": TOOLS})
        if method == "tools/call":
            params = message.get("params") or {}
            return self._call(request_id, params.get("name"), params.get("arguments") or {})
        return self._error(request_id, -32601, f"Method not found: {method}")

    def _call(self, request_id: Any, name: str | None, arguments: dict[str, Any]) -> dict[str, Any]:
        routes = {
            "start_project": "/projects/start", "continue_project": "/projects/continue", "project_status": "/projects/status",
            "project_knowledge_summary": "/projects/knowledge-summary", "project_navigator": "/projects/navigator", "save_project_checkpoint": "/projects/checkpoint", "update_knowledge_item": None,
        }
        if name not in routes:
            return self._error(request_id, -32602, f"Unknown tool: {name}")
        if name == "update_knowledge_item":
            project_id = arguments.get("project_id")
            item_id = arguments.get("item_id")
            status, payload = self.runtime.request("PUT", f"/projects/{project_id}/knowledge-items/{item_id}", arguments)
        else:
            status, payload = self.runtime.post(routes[name], arguments)
        text = json.dumps(payload, ensure_ascii=False, indent=2)
        result = {"content": [{"type": "text", "text": text}], "structuredContent": payload}
        if status >= 400:
            result["isError"] = True
        return self._result(request_id, result)

    @staticmethod
    def _result(request_id: Any, result: dict[str, Any]) -> dict[str, Any]:
        return {"jsonrpc": "2.0", "id": request_id, "result": result}

    @staticmethod
    def _error(request_id: Any, code: int, message: str) -> dict[str, Any]:
        return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


class MCPHandler(BaseHTTPRequestHandler):
    application: MCPApplication | None = None

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._write(200, {"status": "ok", "runtime_api": RUNTIME_API_URL})
        else:
            self._write(404, {"error": "Not found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/mcp" or self.application is None:
            self._write(404, {"error": "Not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            message = json.loads(self.rfile.read(length).decode("utf-8"))
            response = self.application.handle(message)
        except (ValueError, json.JSONDecodeError) as exc:
            self._write(400, {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(exc)}})
            return
        if response is None:
            self.send_response(202)
            self.end_headers()
            return
        self._write(200, response)

    def _write(self, status: int, payload: dict[str, Any]) -> None:
        encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format: str, *args: Any) -> None:
        return


def serve(host: str = "127.0.0.1", port: int = 8787, runtime_api_url: str = RUNTIME_API_URL) -> None:
    MCPHandler.application = MCPApplication(runtime_api_url)
    server = ThreadingHTTPServer((host, port), MCPHandler)
    try:
        server.serve_forever()
    finally:
        server.server_close()


if __name__ == "__main__":
    serve()
