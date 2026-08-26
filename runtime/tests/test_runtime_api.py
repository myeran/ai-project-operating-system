import json
import sys
import tempfile
import threading
import unittest
import urllib.request
from pathlib import Path
from http.server import ThreadingHTTPServer

sys.path.insert(0, str(Path(__file__).parents[1]))

from runtime_api import RuntimeAPIApplication, RuntimeAPIHandler  # noqa: E402


class RuntimeAPIMVPTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database = str(Path(self.temp_dir.name) / "api.sqlite3")
        self.api = RuntimeAPIApplication(self.database)

    @staticmethod
    def project_context(name, description=None):
        body = {
            "project_name": name,
            "owner": "api-user",
            "project_type": "Product",
            "project_goal": "Validate the Runtime project flow",
            "expected_outcome": "A structured project foundation",
            "current_stage": "Idea",
        }
        if description is not None:
            body["description"] = description
        return body

    def tearDown(self):
        self.api.close()
        self.temp_dir.cleanup()

    def test_1_start_project(self):
        status, response = self.api.handle(
            "POST",
            "/projects/start",
            self.project_context("API Habit Tracker", "Created through the API."),
        )

        self.assertEqual(status, 201)
        self.assertTrue(response["request_id"])
        self.assertTrue(response["correlation_id"])
        self.assertTrue(response["project_id"])
        self.assertEqual(response["current_phase"], "Discovery")
        self.assertEqual(response["status"], "proposed")
        self.assertEqual(response["discovery_status"], "COMPLETED")
        self.assertTrue(response["state_update_proposal"])
        self.assertFalse(response["state_committed"])
        self.assertTrue(Path(response["lifecycle_artifacts"]["mermaid"]).exists())
        self.assertTrue(Path(response["lifecycle_artifacts"]["html"]).exists())
        project_state = self.api.state.get_state(response["project_id"])
        self.assertEqual(
            project_state["canonical_state"]["project_identity"]["project_context"]["project_type"],
            "Product",
        )
        for field in (
            "completed",
            "missing",
            "required_user_action",
            "expected_output",
            "completion_criteria",
            "next_recommended_action",
        ):
            self.assertIn(field, response)

    def test_2_continue_project(self):
        _, created = self.api.handle(
            "POST",
            "/projects/start",
            self.project_context("API Continue Project"),
        )
        before = self.api.state.list_proposals(created["project_id"])
        self.assertEqual(len(before), 1)

        status, response = self.api.handle(
            "POST", f"/projects/{created['project_id']}/continue", {}
        )

        self.assertEqual(status, 200)
        self.assertEqual(response["project_id"], created["project_id"])
        self.assertEqual(response["current_phase"], "Discovery")
        after = self.api.state.list_proposals(created["project_id"])
        self.assertEqual([item["proposal_id"] for item in after], [item["proposal_id"] for item in before])

    def test_continue_project_by_name(self):
        _, created = self.api.handle(
            "POST", "/projects/start", self.project_context("Name Resolved Project")
        )
        status, response = self.api.handle(
            "POST", "/projects/continue", {"project_name": "Name Resolved Project"}
        )
        self.assertEqual(status, 200)
        self.assertEqual(response["project_id"], created["project_id"])
        self.assertEqual(response["current_phase"], "Discovery")
        self.assertIn("required_user_action", response)

    def test_status_by_name(self):
        _, created = self.api.handle(
            "POST", "/projects/start", self.project_context("Status Name Project")
        )
        status, response = self.api.handle(
            "POST", "/projects/status", {"project_name": "Status Name Project"}
        )
        self.assertEqual(status, 200)
        self.assertEqual(response["project"]["project_id"], created["project_id"])
        self.assertEqual(response["state"]["phase"], "Discovery")

    def test_name_resolution_errors(self):
        status, response = self.api.handle(
            "POST", "/projects/continue", {"project_name": "Missing Name"}
        )
        self.assertEqual(status, 404)
        self.assertEqual(response["error_type"], "PROJECT_NOT_FOUND")

    def test_discovery_creates_proposal_and_guidance(self):
        _, created = self.api.handle(
            "POST",
            "/projects/start",
            self.project_context("API Discovery Project"),
        )

        status, response = self.api.handle(
            "POST",
            f"/projects/{created['project_id']}/discovery",
            {
                "problem_statement": "The project context is fragmented.",
                "confirmed_findings": ["Context is spread across files"],
                "validation_required": ["Validate the primary user"],
            },
        )

        self.assertEqual(status, 200)
        self.assertEqual(response["discovery_status"], "COMPLETED")
        self.assertEqual(response["current_phase"], "Discovery")
        self.assertFalse(response["state_committed"])
        self.assertEqual(response["missing"], ["Validate the primary user"])
        self.assertTrue(response["state_update_proposal"])

    def _create_discovery_proposal(self, name):
        _, created = self.api.handle(
            "POST", "/projects/start", self.project_context(name)
        )
        _, discovery = self.api.handle(
            "POST",
            f"/projects/{created['project_id']}/discovery",
            {"validation_required": ["Validate the primary user"]},
        )
        return created["project_id"], discovery["state_update_proposal"]["proposal_id"]

    def test_proposal_list_approve_and_commit(self):
        project_id, proposal_id = self._create_discovery_proposal("API Approval Project")

        status, pending = self.api.handle("GET", f"/projects/{project_id}/proposals")
        self.assertEqual(status, 200)
        self.assertEqual(pending["proposals"][0]["status"], "pending")

        status, approved = self.api.handle(
            "POST", f"/proposals/{proposal_id}/approve", {"approver": "project-owner"}
        )
        self.assertEqual(status, 200)
        self.assertEqual(approved["status"], "approved")

        status, committed = self.api.handle(
            "POST", f"/proposals/{proposal_id}/commit", {"approver": "project-owner"}
        )
        self.assertEqual(status, 200)
        self.assertEqual(committed["status"], "committed")
        self.assertEqual(committed["state"]["version"], 2)
        self.assertIn("Discovery Output", committed["state"]["completed_outputs"])

    def test_commit_rejects_version_conflict(self):
        project_id, proposal_id = self._create_discovery_proposal("API Conflict Project")
        self.assertEqual(
            self.api.handle("POST", f"/proposals/{proposal_id}/approve", {"approver": "owner"})[0],
            200,
        )
        other = self.api.state.propose_state_update(
            project_id, {"status": "active"}, actor="other-update"
        )
        self.api.state.commit_state_update(other["proposal_id"], expected_version=1)

        status, response = self.api.handle(
            "POST", f"/proposals/{proposal_id}/commit", {"approver": "owner"}
        )
        self.assertEqual(status, 409)
        self.assertEqual(response["error_type"], "VERSION_CONFLICT")

    def test_rejected_proposal_does_not_change_state(self):
        project_id, proposal_id = self._create_discovery_proposal("API Rejection Project")
        before = self.api.state.get_state(project_id)
        rejected = self.api.state.reject_state_proposal(
            proposal_id, rejector="owner", reason="Needs more evidence"
        )
        after = self.api.state.get_state(project_id)

        self.assertEqual(rejected["status"], "rejected")
        self.assertEqual(before["version"], after["version"])
        self.assertEqual(after["completed_outputs"], before["completed_outputs"])

    def test_3_status(self):
        _, created = self.api.handle(
            "POST",
            "/projects/start",
            self.project_context("API Status Project"),
        )

        status, response = self.api.handle(
            "GET", f"/projects/{created['project_id']}/status"
        )

        self.assertEqual(status, 200)
        self.assertEqual(response["project"]["status"], "RESOLVED")
        self.assertEqual(response["state"]["phase"], "Discovery")

    def test_4_duplicate_start(self):
        body = self.project_context("API Duplicate Project")
        self.assertEqual(self.api.handle("POST", "/projects/start", body)[0], 201)

        status, response = self.api.handle("POST", "/projects/start", body)

        self.assertEqual(status, 409)
        self.assertEqual(response["error_type"], "DUPLICATE_PROJECT")
        self.assertTrue(response["fail_closed"])

    def test_5_invalid_request(self):
        status, response = self.api.handle(
            "POST", "/projects/start", {"project_name": "Missing Owner"}
        )

        self.assertEqual(status, 400)
        self.assertEqual(response["error_type"], "INVALID_REQUEST")

    def test_missing_project_context_returns_one_clarification(self):
        status, response = self.api.handle(
            "POST",
            "/projects/start",
            {"project_name": "Ambiguous Project", "owner": "api-user"},
        )

        self.assertEqual(status, 422)
        self.assertEqual(response["error_type"], "PROJECT_CONTEXT_REQUIRED")
        self.assertIn("clarification_question", response)
        self.assertFalse(self.api.registry.find_projects(project_name="Ambiguous Project"))

    def test_project_not_found(self):
        status, response = self.api.handle(
            "POST", "/projects/missing-project/continue", {}
        )

        self.assertEqual(status, 404)
        self.assertEqual(response["error_type"], "PROJECT_NOT_FOUND")

    def test_unknown_endpoint(self):
        status, response = self.api.handle("GET", "/unknown")

        self.assertEqual(status, 404)

    def test_knowledge_edit_updates_existing_item_without_duplicate(self):
        _, created = self.api.handle("POST", "/projects/start", self.project_context("Knowledge Project"))
        project_id = created["project_id"]
        summary = self.api.handle("POST", "/projects/knowledge-summary", {"project_id": project_id})[1]
        self.assertGreaterEqual(len(summary["items"]), 1)
        item_id = summary["items"][0]["id"]
        status, updated = self.api.handle("PUT", f"/projects/{project_id}/knowledge-items/{item_id}", {"answer": "משתמשים מאבדים מידע בין כלים.", "status": "approved", "actor": "owner"})
        self.assertEqual(status, 200)
        self.assertEqual(updated["item"]["id"], item_id)
        self.assertEqual(updated["item"]["status"], "approved")
        self.assertEqual(len(updated["knowledge_summary"]["items"]), len(summary["items"]))
        self.assertEqual(updated["knowledge_summary"]["counts"]["approved"], 1)

    def test_checkpoint_persists_and_status_exposes_knowledge_summary(self):
        _, created = self.api.handle("POST", "/projects/start", self.project_context("Checkpoint Project"))
        project_id = created["project_id"]
        summary = self.api.handle("POST", "/projects/knowledge-summary", {"project_id": project_id})[1]
        items = summary["items"]
        items[0]["answer"] = "תשובת ביניים"
        items[0]["status"] = "needs_update"
        status, saved = self.api.handle("POST", "/projects/checkpoint", {"project_id": project_id, "items": items, "actor": "owner"})
        self.assertEqual(status, 200)
        self.assertTrue(saved["saved"])
        status, current = self.api.handle("GET", f"/projects/{project_id}/status")
        self.assertEqual(status, 200)
        self.assertEqual(current["knowledge_summary"]["items"][0]["answer"], "תשובת ביניים")
        self.assertEqual(current["knowledge_summary"]["counts"]["needs_update"], 1)

    def test_http_server_dispatches_to_runtime_api(self):
        class TestHandler(RuntimeAPIHandler):
            application = self.api

        server = ThreadingHTTPServer(("127.0.0.1", 0), TestHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            payload = json.dumps(self.project_context("HTTP API Project")).encode("utf-8")
            request = urllib.request.Request(
                f"http://127.0.0.1:{server.server_port}/projects/start",
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(request, timeout=2) as response:
                body = json.loads(response.read().decode("utf-8"))
                self.assertEqual(response.status, 201)
                self.assertTrue(body["project_id"])
                self.assertEqual(body["current_phase"], "Discovery")
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)


if __name__ == "__main__":
    unittest.main()
