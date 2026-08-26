"""Local browser chat that routes every project action through MCP."""

from __future__ import annotations

import json
import os
import re
import uuid
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

try:
    from .conversation import ConversationIntent, ConversationIntentHandler, ConversationState, ResponsePresentation
except ImportError:  # Supports direct test-module execution.
    from conversation import ConversationIntent, ConversationIntentHandler, ConversationState, ResponsePresentation


MCP_URL = "http://127.0.0.1:8787/mcp"
CHAT_PORT = 8790
HTML_PATH = Path(__file__).with_name("local_chat.html")


class LocalChatError(Exception):
    def __init__(self, message: str, *, payload: dict[str, Any] | None = None):
        super().__init__(message)
        self.payload = payload


class MCPClient:
    """Client for the existing MCP HTTP endpoint; no Runtime internals here."""

    def __init__(self, mcp_url: str = MCP_URL, transport: Callable[[dict[str, Any]], dict[str, Any]] | None = None):
        self.mcp_url = mcp_url
        self.transport = transport or self._post

    def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        response = self.transport({
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments},
        })
        if "error" in response:
            raise LocalChatError(response["error"].get("message", "MCP request failed"))
        result = response.get("result") or {}
        payload = result.get("structuredContent")
        if not isinstance(payload, dict):
            raise LocalChatError("MCP returned an invalid response")
        if result.get("isError"):
            raise LocalChatError(payload.get("message", "Runtime request failed"), payload=payload)
        return payload

    def _post(self, message: dict[str, Any]) -> dict[str, Any]:
        request = Request(
            self.mcp_url,
            data=json.dumps(message, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=10) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            raise LocalChatError(f"MCP Server returned HTTP {exc.code}") from exc
        except (URLError, TimeoutError) as exc:
            raise LocalChatError("MCP Server is unavailable. Start it on http://127.0.0.1:8787.") from exc


class LocalChatSession:
    """State-aware conversational boundary over the existing MCP tools."""

    def __init__(self, mcp: MCPClient | None = None, *, debug: bool = False):
        self.mcp = mcp or MCPClient()
        self.state = ConversationState()
        self.intent_handler = ConversationIntentHandler()
        self.presentation = ResponsePresentation()
        self.debug = debug

    @property
    def active_project_id(self) -> str | None:
        return self.state.active_project_id

    @active_project_id.setter
    def active_project_id(self, value: str | None) -> None:
        self.state.active_project_id = value

    @property
    def active_project_name(self) -> str | None:
        return self.state.active_project_name

    @active_project_name.setter
    def active_project_name(self, value: str | None) -> None:
        self.state.active_project_name = value

    def handle(self, message: str) -> dict[str, Any]:
        if not isinstance(message, str) or not message.strip():
            raise LocalChatError("כתוב הודעה כדי להתחיל.")
        text = message.strip()
        intent = self.intent_handler.classify(text, self.state)
        if intent == ConversationIntent.PROJECT_NAVIGATOR:
            if not self.active_project_id:
                return {"reply": "כדי להציג את רשימת ה־Skills, התחל או טען קודם פרויקט."}
            payload = self.project_navigator()
        elif intent == ConversationIntent.START_PROJECT:
            self.state.question_index = 0
            self.state.discovery_questions = []
            name = self._project_name(text)
            payload = self.mcp.call_tool("start_project", {
                "project_name": name,
                "owner": "local-user",
                "project_type": "Product",
                "project_goal": text,
                "expected_outcome": "Structured project foundation and Discovery guidance",
                "current_stage": "Idea / Discovery",
            })
        elif intent in {ConversationIntent.CONTINUE_PROJECT, ConversationIntent.PROJECT_STATUS}:
            arguments = {"message": text}
            if self.active_project_id:
                arguments["project_id"] = self.active_project_id
            else:
                arguments["project_name"] = self.active_project_name
            payload = self.mcp.call_tool(intent.value, arguments)
            if intent == ConversationIntent.CONTINUE_PROJECT and not ConversationIntentHandler.is_help_request(text):
                captured = self._capture_answer(text)
                if captured:
                    payload = {**payload, "knowledge_summary": captured.get("knowledge_summary")}
        elif intent == ConversationIntent.NEEDS_START:
            return {"reply": self.presentation.present(intent, {}, self.state, text)}
        else:
            raise LocalChatError("לא הצלחתי להבין את הבקשה.")

        project = payload.get("project") or {}
        self.active_project_id = payload.get("project_id") or project.get("project_id") or self.active_project_id
        self.active_project_name = project.get("project_name") or self.active_project_name
        reply = self.presentation.present(intent, payload, self.state, text)
        result: dict[str, Any] = {"reply": reply}
        if isinstance(payload.get("knowledge_summary"), dict):
            result["knowledge_summary"] = payload["knowledge_summary"]
        if self.debug:
            result["debug"] = {
                "tool": intent.value,
                "project_id": self.active_project_id,
                "raw_response": payload,
            }
        return result

    def _capture_answer(self, text: str) -> dict[str, Any] | None:
        """Persist the user's current chat answer on its existing question item."""
        if not self.state.discovery_questions:
            return None
        index = min(self.state.question_index, len(self.state.discovery_questions) - 1)
        item_id = f"discovery-question-{index + 1}"
        return self.mcp.call_tool("update_knowledge_item", {
            "project_id": self.active_project_id,
            "item_id": item_id,
            "answer": text,
            "status": "open",
            "actor": "local-user",
        })

    def knowledge_summary(self) -> dict[str, Any]:
        if not self.active_project_id:
            raise LocalChatError("אין פרויקט פעיל עדיין.")
        return self.mcp.call_tool("project_knowledge_summary", {"project_id": self.active_project_id})

    def update_knowledge_item(self, item_id: str, answer: str, status: str) -> dict[str, Any]:
        if not self.active_project_id:
            raise LocalChatError("אין פרויקט פעיל עדיין.")
        return self.mcp.call_tool("update_knowledge_item", {"project_id": self.active_project_id, "item_id": item_id, "answer": answer, "status": status, "actor": "local-user"})

    def save_checkpoint(self, items: list[dict[str, Any]] | None = None) -> dict[str, Any]:
        if not self.active_project_id:
            raise LocalChatError("אין פרויקט פעיל עדיין.")
        payload = {"project_id": self.active_project_id, "actor": "local-user"}
        if items is not None:
            payload["items"] = items
        return self.mcp.call_tool("save_project_checkpoint", payload)

    def project_navigator(self) -> dict[str, Any]:
        if not self.active_project_id:
            raise LocalChatError("אין פרויקט פעיל עדיין.")
        return self.mcp.call_tool("project_navigator", {"project_id": self.active_project_id})

    @staticmethod
    def _project_name(text: str) -> str:
        match = re.search(r"(?:project|פרויקט)\s*[:\-]?\s+(.+)$", text, flags=re.IGNORECASE)
        suffix = match.group(1).strip() if match else "Local Chat Project"
        if suffix in {"חדש", "new", "a new project"}:
            suffix = "Local Chat Project"
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        return f"{suffix[:80]} {stamp}".strip()


class LocalChatHandler(BaseHTTPRequestHandler):
    session: LocalChatSession | None = None

    def do_GET(self) -> None:  # noqa: N802
        if self.path in {"/", "/index.html"}:
            body = HTML_PATH.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self._json(404, {"error": "Not found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.session is None:
            self._json(404, {"error": "Not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(length).decode("utf-8"))
            if self.path == "/api/chat":
                result = self.session.handle(body.get("message", ""))
                # Refresh the side navigator immediately after a project starts
                # or the conversation advances. The navigator remains a
                # read-only projection of canonical Runtime state.
                if self.session.active_project_id:
                    try:
                        result["navigator"] = self.session.project_navigator()
                    except LocalChatError:
                        # Do not hide a successful chat response if the optional
                        # side-panel refresh is temporarily unavailable.
                        pass
            elif self.path == "/api/knowledge-summary":
                result = self.session.knowledge_summary()
            elif self.path == "/api/save-checkpoint":
                result = self.session.save_checkpoint(body.get("items"))
            elif self.path == "/api/project-navigator":
                result = self.session.project_navigator()
            elif self.path == "/api/update-knowledge":
                result = self.session.update_knowledge_item(body.get("item_id", ""), body.get("answer", ""), body.get("status", "open"))
            else:
                self._json(404, {"error": "Not found"})
                return
            self._json(200, result)
        except (ValueError, json.JSONDecodeError):
            self._json(400, {"error": "Invalid JSON request"})
        except LocalChatError as exc:
            error = ResponsePresentation.present_error(exc.payload) if exc.payload else "כרגע השירות אינו זמין. נסה שוב בעוד רגע."
            self._json(503, {"error": error})

    def _json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:
        return


def serve(host: str = "127.0.0.1", port: int = CHAT_PORT, mcp_url: str = MCP_URL, debug: bool = False) -> None:
    LocalChatHandler.session = LocalChatSession(MCPClient(mcp_url), debug=debug)
    server = ThreadingHTTPServer((host, port), LocalChatHandler)
    try:
        server.serve_forever()
    finally:
        server.server_close()


if __name__ == "__main__":
    serve(debug=os.environ.get("LOCAL_CHAT_DEBUG", "").lower() in {"1", "true", "yes"})
