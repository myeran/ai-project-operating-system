import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from local_client import LocalClientError, LocalProjectClient  # noqa: E402


class LocalProjectClientTests(unittest.TestCase):
    def test_parse_supported_commands(self):
        self.assertEqual(LocalProjectClient.parse("Continue Project: Personal Habit Tracker").intent, "CONTINUE_PROJECT")
        self.assertEqual(LocalProjectClient.parse("Project Status: Personal Habit Tracker").intent, "PROJECT_STATUS")
        self.assertEqual(LocalProjectClient.parse("Start Project: Personal Habit Tracker").project_name, "Personal Habit Tracker")

    def test_routes_by_name_without_storage_access(self):
        calls = []

        def transport(method, path, payload):
            calls.append((method, path, payload))
            return {"project_id": "p1", "current_phase": "Discovery", "status": "proposed"}

        client = LocalProjectClient(transport=transport)
        response = client.execute("Continue Project: Personal Habit Tracker")
        self.assertEqual(response["project_id"], "p1")
        self.assertEqual(calls, [("POST", "/projects/continue", {"project_name": "Personal Habit Tracker"})])

    def test_unknown_command_fails_closed(self):
        with self.assertRaises(LocalClientError):
            LocalProjectClient.parse("Do something with my project")


if __name__ == "__main__":
    unittest.main()
