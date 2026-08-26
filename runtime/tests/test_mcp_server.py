import json
import sys
import tempfile
import threading
import unittest
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from runtime_api import RuntimeAPIApplication, RuntimeAPIHandler  # noqa: E402
from integration.mcp_server import MCPApplication, MCPHandler  # noqa: E402
from integration.local_chat import LocalChatSession, MCPClient  # noqa: E402


class MCPIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.runtime_app = RuntimeAPIApplication(str(Path(self.temp_dir.name) / "runtime.sqlite3"))
        RuntimeAPIHandler.application = self.runtime_app
        self.runtime_server = ThreadingHTTPServer(("127.0.0.1", 0), RuntimeAPIHandler)
        self.runtime_thread = threading.Thread(target=self.runtime_server.serve_forever, daemon=True)
        self.runtime_thread.start()
        self.mcp_app = MCPApplication(f"http://127.0.0.1:{self.runtime_server.server_port}")

    def tearDown(self):
        self.runtime_server.shutdown()
        self.runtime_server.server_close()
        self.runtime_app.close()
        self.temp_dir.cleanup()

    def test_tools_are_narrow_and_mcp_call_reaches_runtime_api(self):
        listed = self.mcp_app.handle({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
        self.assertEqual(
            [tool["name"] for tool in listed["result"]["tools"]],
            ["project_navigator", "start_project", "continue_project", "project_status", "project_knowledge_summary", "update_knowledge_item", "save_project_checkpoint"],
        )
        args = {
            "project_name": "MCP E2E Project",
            "owner": "mcp-user",
            "project_type": "Product",
            "project_goal": "Verify ChatGPT integration",
            "expected_outcome": "Runtime response through MCP",
            "current_stage": "Idea / Discovery",
        }
        created = self.mcp_app.handle({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "start_project", "arguments": args}})
        payload = created["result"]["structuredContent"]
        self.assertTrue(payload["project_id"])
        self.assertEqual(payload["current_phase"], "Discovery")
        self.assertFalse(payload["state_committed"])

        navigator = self.mcp_app.handle({"jsonrpc": "2.0", "id": 25, "method": "tools/call", "params": {"name": "project_navigator", "arguments": {"project_id": payload["project_id"]}}})
        navigator_payload = navigator["result"]["structuredContent"]
        self.assertEqual(navigator_payload["current_phase"], "Discovery")
        self.assertTrue(navigator_payload["read_only"])
        self.assertTrue(Path(navigator_payload["lifecycle_artifacts"]["html"]).exists())

        status = self.mcp_app.handle({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "project_status", "arguments": {"project_id": payload["project_id"]}}})
        status_payload = status["result"]["structuredContent"]
        self.assertEqual(status_payload["project"]["project_id"], payload["project_id"])
        self.assertEqual(status_payload["state"]["version"], 1)

    def test_unknown_tool_fails_without_runtime_call(self):
        response = self.mcp_app.handle({"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "commit_state", "arguments": {}}})
        self.assertEqual(response["error"]["code"], -32602)

    def test_knowledge_management_round_trip_through_mcp(self):
        args = {
            "project_name": "MCP Knowledge Project", "owner": "mcp-user", "project_type": "Product",
            "project_goal": "Keep project knowledge editable", "expected_outcome": "A reusable summary", "current_stage": "Discovery",
        }
        created = self.mcp_app.handle({"jsonrpc": "2.0", "id": 20, "method": "tools/call", "params": {"name": "start_project", "arguments": args}})["result"]["structuredContent"]
        project_id = created["project_id"]
        summary = self.mcp_app.handle({"jsonrpc": "2.0", "id": 21, "method": "tools/call", "params": {"name": "project_knowledge_summary", "arguments": {"project_id": project_id}}})["result"]["structuredContent"]
        item = summary["items"][0]
        updated = self.mcp_app.handle({"jsonrpc": "2.0", "id": 22, "method": "tools/call", "params": {"name": "update_knowledge_item", "arguments": {"project_id": project_id, "item_id": item["id"], "answer": "תשובה דרך MCP", "status": "approved"}}})["result"]["structuredContent"]
        self.assertEqual(updated["item"]["id"], item["id"])
        self.assertEqual(updated["knowledge_summary"]["counts"]["approved"], 1)

    def test_http_mcp_endpoint_is_end_to_end(self):
        MCPHandler.application = self.mcp_app
        mcp_server = ThreadingHTTPServer(("127.0.0.1", 0), MCPHandler)
        thread = threading.Thread(target=mcp_server.serve_forever, daemon=True)
        thread.start()
        try:
            request = urllib.request.Request(
                f"http://127.0.0.1:{mcp_server.server_port}/mcp",
                data=json.dumps({"jsonrpc": "2.0", "id": 10, "method": "tools/list"}).encode(),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(request) as response:
                body = json.loads(response.read().decode())
            self.assertEqual(response.status, 200)
            self.assertEqual(len(body["result"]["tools"]), 7)
        finally:
            mcp_server.shutdown()
            mcp_server.server_close()

    def test_local_chat_start_continue_status_through_http_mcp(self):
        MCPHandler.application = self.mcp_app
        mcp_server = ThreadingHTTPServer(("127.0.0.1", 0), MCPHandler)
        thread = threading.Thread(target=mcp_server.serve_forever, daemon=True)
        thread.start()
        try:
            chat = LocalChatSession(MCPClient(f"http://127.0.0.1:{mcp_server.server_port}/mcp"), debug=True)
            start = chat.handle("אני רוצה להתחיל פרויקט חדש")
            continue_result = chat.handle("אני רוצה לבנות מערכת לניהול לקוחות")
            status = chat.handle("מה הסטטוס של הפרויקט?")
            self.assertEqual(start["debug"]["tool"], "start_project")
            self.assertEqual(continue_result["debug"]["tool"], "continue_project")
            self.assertEqual(status["debug"]["tool"], "project_status")
            self.assertEqual(continue_result["debug"]["project_id"], start["debug"]["project_id"])
            self.assertEqual(status["debug"]["raw_response"]["project"]["project_id"], start["debug"]["project_id"])
            self.assertNotIn("project_id", continue_result)
        finally:
            mcp_server.shutdown()
            mcp_server.server_close()


if __name__ == "__main__":
    unittest.main()
