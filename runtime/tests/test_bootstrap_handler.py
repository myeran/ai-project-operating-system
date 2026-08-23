import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from bootstrap_handler import (  # noqa: E402
    BootstrapError,
    BootstrapRequest,
    ProjectInstanceBootstrapHandler,
)
from registry_adapter import (  # noqa: E402
    DuplicateProjectError,
    ProjectRegistryAdapter,
)
from state_adapter import StateAdapter, StateAdapterError  # noqa: E402


class BootstrapHandlerMVPTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database = str(Path(self.temp_dir.name) / "runtime.sqlite3")
        self.registry = ProjectRegistryAdapter(self.database)
        self.state = StateAdapter(self.database)
        self.handler = ProjectInstanceBootstrapHandler(self.registry, self.state)

    def tearDown(self):
        self.state.close()
        self.registry.close()
        self.temp_dir.cleanup()

    def request(self, **overrides):
        values = {
            "project_name": "Personal Habit Tracker",
            "owner": "owner-1",
            "os_version": "v1.0",
            "description": "Track daily habits.",
            "actor": "bootstrap",
        }
        values.update(overrides)
        return BootstrapRequest(**values)

    def test_bootstrap_creates_registry_and_initial_state(self):
        result = self.handler.initialize(self.request())

        self.assertEqual(result["status"], "initialized")
        self.assertEqual(result["registry"]["current_phase"], "Discovery")
        self.assertEqual(result["registry"]["status"], "proposed")
        self.assertEqual(result["state"]["phase"], "Discovery")
        self.assertEqual(result["state"]["status"], "proposed")
        self.assertEqual(
            result["state"]["canonical_state"]["project_identity"]["description"],
            "Track daily habits.",
        )
        self.assertEqual(result["os_version"], "v1.0")

    def test_optional_workspace_location_gets_default(self):
        result = self.handler.initialize(self.request())

        self.assertEqual(result["workspace_location"], "projects/personal-habit-tracker")

    def test_custom_workspace_location_is_preserved(self):
        result = self.handler.initialize(
            self.request(workspace_location="workspaces/habits")
        )

        self.assertEqual(result["workspace_location"], "workspaces/habits")

    def test_duplicate_project_is_rejected_before_state_creation(self):
        first = self.handler.initialize(self.request())

        with self.assertRaises(DuplicateProjectError):
            self.handler.initialize(self.request())

        self.assertEqual(
            self.state.get_state(first["project_id"])["version"],
            1,
        )

    def test_invalid_request_does_not_create_registry_entry(self):
        with self.assertRaises(BootstrapError):
            self.handler.initialize(self.request(project_name=""))


    def test_state_failure_marks_partial_instance_blocked(self):
        original = self.state.create_initial_state

        def fail_once(*args, **kwargs):
            raise StateAdapterError("simulated state failure")

        self.state.create_initial_state = fail_once
        with self.assertRaises(BootstrapError):
            self.handler.initialize(self.request())
        self.state.create_initial_state = original

        matches = self.registry.find_projects(project_name="Personal Habit Tracker")
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["status"], "blocked")


if __name__ == "__main__":
    unittest.main()
