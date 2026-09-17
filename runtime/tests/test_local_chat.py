import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from integration.local_chat import LocalChatError, LocalChatSession, MCPClient  # noqa: E402


class FakeMCP:
    def __init__(self):
        self.calls = []

    def call_tool(self, name, arguments):
        self.calls.append((name, arguments))
        if name == "start_project":
            return {
                "project_id": "project-123",
                "project": {"project_id": "project-123", "project_name": "Local Chat Project"},
                "current_phase": "Discovery",
                "status": "proposed",
                "next_recommended_action": "Answer the Discovery questions and provide evidence before defining product direction.",
                "discovery_output": {"open_questions": [{"question": "What problem are we trying to solve?"}, {"question": "Who experiences this problem first?"}]},
            }
        if name == "update_knowledge_item":
            return {"project_id": "project-123", "knowledge_summary": {"items": [{"id": arguments["item_id"], "question": "What problem are we trying to solve?", "answer": arguments["answer"], "status": arguments["status"]}], "counts": {"open": 1, "approved": 0, "needs_update": 0}}}
        if name == "project_navigator":
            return {"project_id": "project-123", "current_phase": "Discovery", "current_skill": "Discovery Skill", "steps": [{"phase": "Discovery", "status": "current", "responsible_skill": "Discovery Skill"}, {"phase": "Strategy", "status": "pending", "responsible_skill": "Product Strategy Skill"}], "missing": ["Problem and user need"], "next_action": "Complete Discovery"}
        return {
            "project_id": "project-123",
            "project": {"project_id": "project-123", "project_name": "Local Chat Project"},
            "current_phase": "Discovery",
            "status": "proposed",
            "next_recommended_action": "Answer the Discovery questions and provide evidence before defining product direction.",
        }


class LocalChatTests(unittest.TestCase):
    def test_free_form_conversation_routes_with_hidden_project_context(self):
        fake = FakeMCP()
        chat = LocalChatSession(fake)

        chat.handle("אני רוצה להתחיל פרויקט חדש")
        chat.handle("אני רוצה לבנות מערכת לניהול לקוחות")
        chat.handle("מה הסטטוס של הפרויקט?")

        self.assertEqual([call[0] for call in fake.calls], ["start_project", "continue_project", "update_knowledge_item", "project_status"])
        self.assertEqual(fake.calls[1][1], {"project_id": "project-123", "message": "אני רוצה לבנות מערכת לניהול לקוחות"})
        self.assertEqual(fake.calls[2][1]["answer"], "אני רוצה לבנות מערכת לניהול לקוחות")
        self.assertEqual(fake.calls[3][1], {"project_id": "project-123", "message": "מה הסטטוס של הפרויקט?"})

    def test_short_new_project_phrase_starts_conversation(self):
        chat = LocalChatSession(FakeMCP())
        result = chat.handle("פרויקט חדש")
        self.assertIn("נתחיל בהבנת הפרויקט", result["reply"])

    def test_natural_project_proposal_starts_without_command(self):
        chat = LocalChatSession(FakeMCP())
        result = chat.handle("אני רוצה לבנות מערכת עזרה במשימות שיש לי")
        self.assertIn("נתחיל בהבנת הפרויקט", result["reply"])

    def test_user_does_not_see_internal_fields_by_default(self):
        chat = LocalChatSession(FakeMCP())
        result = chat.handle("אני רוצה להתחיל פרויקט חדש")
        self.assertEqual(set(result), {"reply"})
        self.assertTrue(result["reply"].startswith("שלום ובהצלחה בפרוייקט"))
        self.assertNotIn("project-123", result["reply"])
        self.assertNotIn("tool", result["reply"])

    def test_debug_is_opt_in(self):
        chat = LocalChatSession(FakeMCP(), debug=True)
        result = chat.handle("אני רוצה להתחיל פרויקט חדש")
        self.assertEqual(result["debug"]["tool"], "start_project")
        self.assertEqual(result["debug"]["project_id"], "project-123")

    def test_natural_help_messages_keep_the_current_question(self):
        chat = LocalChatSession(FakeMCP())
        chat.handle("אני רוצה להתחיל פרויקט חדש")
        reply = chat.handle("מה לעשות?")["reply"]
        self.assertIn("איזו בעיה אנחנו מנסים לפתור?", reply)

    def test_project_navigator_command_returns_skill_roadmap(self):
        fake = FakeMCP()
        chat = LocalChatSession(fake)
        chat.handle("אני רוצה להתחיל פרויקט חדש")
        result = chat.handle("project_navigator_skill")
        self.assertEqual(fake.calls[-1][0], "project_navigator")
        self.assertIn("Discovery Skill", result["reply"])
        self.assertIn("Product Strategy Skill", result["reply"])

    def test_project_navigator_requires_active_project(self):
        result = LocalChatSession(FakeMCP()).handle("project_navigator_skill")
        self.assertIn("התחל או טען קודם פרויקט", result["reply"])

    def test_continue_without_active_project_is_clear(self):
        result = LocalChatSession(FakeMCP()).handle("מה לעשות?")
        self.assertIn("כדי להתחיל", result["reply"])

    def test_mcp_server_unavailable_is_reported(self):
        def unavailable(_message):
            raise LocalChatError("MCP Server is unavailable")

        chat = LocalChatSession(MCPClient(transport=unavailable))
        chat.active_project_id = "project-123"
        with self.assertRaisesRegex(LocalChatError, "MCP Server"):
            chat.handle("מה הסטטוס של הפרויקט?")

    def test_runtime_unavailable_response_is_reported(self):
        response = {"jsonrpc": "2.0", "id": "1", "result": {"isError": True, "structuredContent": {"message": "Runtime API is unavailable"}}}
        chat = LocalChatSession(MCPClient(transport=lambda _message: response))
        chat.active_project_id = "project-123"
        with self.assertRaisesRegex(LocalChatError, "Runtime API"):
            chat.handle("מה הסטטוס של הפרויקט?")


if __name__ == "__main__":
    unittest.main()
