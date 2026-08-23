import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from runtime_gateway import (  # noqa: E402
    InvalidRuntimeRequestError,
    RuntimeEntryGateway,
)


class RuntimeEntryGatewayTests(unittest.TestCase):
    def setUp(self):
        self.gateway = RuntimeEntryGateway()

    def test_start_project_is_classified_and_name_extracted(self):
        request = self.gateway.receive("Start Project: Personal Habit Tracker")

        self.assertEqual(request.intent, "START_PROJECT")
        self.assertEqual(request.request_type, "PROJECT_START")
        self.assertEqual(request.project_name, "Personal Habit Tracker")
        self.assertTrue(request.request_id)
        self.assertTrue(request.correlation_id)

    def test_continue_project_is_classified(self):
        request = self.gateway.receive("Continue Project: Habit Tracker")

        self.assertEqual(request.intent, "CONTINUE_PROJECT")
        self.assertEqual(request.project_name, "Habit Tracker")

    def test_status_is_classified(self):
        request = self.gateway.receive("What is the current phase?")

        self.assertEqual(request.intent, "STATUS")
        self.assertEqual(request.request_type, "PROJECT_STATUS")

    def test_validation_is_classified(self):
        request = self.gateway.receive("Continue Discovery")

        self.assertEqual(request.intent, "VALIDATION_REQUEST")

    def test_execution_is_classified_without_execution(self):
        request = self.gateway.receive("Implement the feature")

        self.assertEqual(request.intent, "EXECUTION_REQUEST")
        self.assertEqual(request.request_type, "PROJECT_EXECUTION")

    def test_unknown_request_is_ambiguous(self):
        request = self.gateway.receive("Tell me something about the project")

        self.assertEqual(request.intent, "AMBIGUOUS")

    def test_explicit_context_is_preserved(self):
        request = self.gateway.receive(
            "Start New Project",
            user_id="user-7",
            source_client="codex",
            correlation_id="conversation-1",
            project_id="project-1",
            workspace_context="workspace-1",
        )

        self.assertEqual(request.user_id, "user-7")
        self.assertEqual(request.source_client, "codex")
        self.assertEqual(request.correlation_id, "conversation-1")
        self.assertEqual(request.project_id, "project-1")
        self.assertEqual(request.workspace_context, "workspace-1")

    def test_empty_request_is_rejected(self):
        with self.assertRaises(InvalidRuntimeRequestError):
            self.gateway.receive("   ")

    def test_request_can_be_serialized_for_downstream_routing(self):
        request = self.gateway.receive("Start Project: Demo")
        payload = self.gateway.to_dict(request)

        self.assertEqual(payload["intent"], "START_PROJECT")
        self.assertEqual(payload["project_name"], "Demo")


if __name__ == "__main__":
    unittest.main()
