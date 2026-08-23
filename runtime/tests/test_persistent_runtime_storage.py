import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from bootstrap_handler import BootstrapRequest, ProjectInstanceBootstrapHandler  # noqa: E402
from registry_adapter import ProjectRegistryAdapter  # noqa: E402
from runtime_gateway import RuntimeEntryGateway  # noqa: E402
from state_adapter import StateAdapter  # noqa: E402


class PersistentRuntimeStorageTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database = str(Path(self.temp_dir.name) / "persistent-runtime.sqlite3")

    def tearDown(self):
        self.temp_dir.cleanup()

    def _create_project(self):
        registry = ProjectRegistryAdapter(self.database)
        state = StateAdapter(self.database)
        bootstrap = ProjectInstanceBootstrapHandler(registry, state)
        result = bootstrap.initialize(
            BootstrapRequest(
                project_name="Persistent Habit Tracker",
                owner="owner-1",
                description="Survives a runtime restart.",
                os_version="v1.0",
                actor="bootstrap",
            )
        )
        state.close()
        registry.close()
        return result

    def test_1_create_then_restart_find_project(self):
        created = self._create_project()

        registry = ProjectRegistryAdapter(self.database)
        try:
            loaded = registry.get_project(created["project_id"])
            found = registry.find_projects(project_name="Persistent Habit Tracker")
        finally:
            registry.close()

        self.assertEqual(loaded["project_id"], created["project_id"])
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]["project_id"], created["project_id"])

    def test_2_continue_existing_project_after_restart(self):
        created = self._create_project()

        gateway = RuntimeEntryGateway()
        request = gateway.receive(
            "Continue Project: Persistent Habit Tracker",
            user_id="owner-1",
            source_client="codex",
        )
        registry = ProjectRegistryAdapter(self.database)
        state = StateAdapter(self.database)
        try:
            matches = registry.find_projects(project_name=request.project_name)
            loaded_state = state.get_state(matches[0]["project_id"])
        finally:
            state.close()
            registry.close()

        self.assertEqual(request.intent, "CONTINUE_PROJECT")
        self.assertEqual(matches[0]["project_id"], created["project_id"])
        self.assertEqual(loaded_state["project_id"], created["project_id"])
        self.assertEqual(loaded_state["phase"], "Discovery")
        self.assertEqual(loaded_state["status"], "proposed")
        self.assertEqual(loaded_state["version"], 1)

    def test_3_audit_persists_after_restart(self):
        created = self._create_project()

        registry = ProjectRegistryAdapter(self.database)
        state = StateAdapter(self.database)
        try:
            registry_events = registry.audit_events(created["project_id"])
            state_events = state.audit_events(created["project_id"])
        finally:
            state.close()
            registry.close()

        self.assertEqual([event["event_type"] for event in registry_events], ["project_created"])
        self.assertEqual([event["event_type"] for event in state_events], ["state_created"])


if __name__ == "__main__":
    unittest.main()
