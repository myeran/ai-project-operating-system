import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from registry_adapter import ProjectMetadata, ProjectRegistryAdapter  # noqa: E402
from state_adapter import (  # noqa: E402
    ApprovalRequiredError,
    InvalidTransitionError,
    StateAdapter,
    VersionConflictError,
)


class StateAdapterMVPTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database = str(Path(self.temp_dir.name) / "runtime.sqlite3")
        self.registry = ProjectRegistryAdapter(self.database)
        self.project = self.registry.create_project(
            ProjectMetadata(
                project_name="State Adapter Test",
                owner="owner-1",
                location="projects/state-adapter-test",
                os_version="v1.0",
            ),
            actor="system",
        )
        self.state = StateAdapter(self.database)

    def tearDown(self):
        self.state.close()
        self.registry.close()
        self.temp_dir.cleanup()

    def test_1_create_state(self):
        state = self.state.create_initial_state(self.project["project_id"])

        self.assertEqual(state["phase"], "Discovery")
        self.assertEqual(state["status"], "proposed")
        self.assertEqual(state["version"], 1)
        self.assertEqual(self.state.audit_events()[0]["event_type"], "state_created")

    def test_2_read_state(self):
        self.state.create_initial_state(self.project["project_id"])

        loaded = self.state.get_state(self.project["project_id"])

        self.assertEqual(loaded["canonical_state"]["project_identity"]["name"], "State Adapter Test")
        self.assertEqual(loaded["canonical_state"]["current_status"]["current_phase"], "Discovery")

    def test_3_update_proposal_does_not_change_state(self):
        initial = self.state.create_initial_state(self.project["project_id"])

        proposal = self.state.propose_state_update(
            self.project["project_id"],
            {"status": "active", "required_user_action": "Provide project context"},
            actor="orchestrator",
        )

        current = self.state.get_state(self.project["project_id"])
        self.assertEqual(proposal["status"], "pending")
        self.assertEqual(current["version"], initial["version"])
        self.assertEqual(current["status"], "proposed")
        self.assertEqual(self.state.audit_events()[-1]["event_type"], "state_update_proposed")

    def test_4_commit_update(self):
        self.state.create_initial_state(self.project["project_id"])
        proposal = self.state.propose_state_update(
            self.project["project_id"],
            {"status": "active", "missing_items": ["Project context"]},
            actor="orchestrator",
        )

        updated = self.state.commit_state_update(
            proposal["proposal_id"], expected_version=1
        )

        self.assertEqual(updated["status"], "active")
        self.assertEqual(updated["version"], 2)
        self.assertEqual(updated["missing_items"], ["Project context"])
        self.assertEqual(self.state.audit_events()[-1]["event_type"], "state_updated")

    def test_5_version_conflict(self):
        self.state.create_initial_state(self.project["project_id"])
        proposal = self.state.propose_state_update(
            self.project["project_id"], {"status": "active"}, actor="orchestrator"
        )

        with self.assertRaises(VersionConflictError):
            self.state.commit_state_update(proposal["proposal_id"], expected_version=2)

        self.assertEqual(self.state.get_state(self.project["project_id"])["version"], 1)
        self.assertEqual(self.state.audit_events()[-1]["event_type"], "version_conflict")

    def test_6_invalid_transition(self):
        self.state.create_initial_state(self.project["project_id"])

        with self.assertRaises(InvalidTransitionError):
            self.state.propose_state_update(
                self.project["project_id"],
                {"phase": "Execution"},
                actor="orchestrator",
            )

        self.assertEqual(
            self.state.audit_events()[-1]["event_type"],
            "invalid_transition_rejected",
        )

    def test_7_phase_transition_requires_explicit_approval(self):
        self.state.create_initial_state(self.project["project_id"])
        proposal = self.state.propose_state_update(
            self.project["project_id"],
            {"phase": "Strategy"},
            actor="orchestrator",
        )

        with self.assertRaises(ApprovalRequiredError):
            self.state.commit_state_update(proposal["proposal_id"], expected_version=1)

        approved = self.state.commit_state_update(
            proposal["proposal_id"], expected_version=1, approved_by="owner-1"
        )
        self.assertEqual(approved["phase"], "Strategy")
        self.assertEqual(approved["version"], 2)
        registry_project = self.registry.get_project(self.project["project_id"])
        self.assertEqual(registry_project["current_phase"], "Strategy")
        self.assertEqual(registry_project["version"], 2)

    def test_8_audit_contains_required_state_events(self):
        self.state.create_initial_state(self.project["project_id"])
        proposal = self.state.propose_state_update(
            self.project["project_id"], {"status": "active"}, actor="orchestrator"
        )
        self.state.commit_state_update(proposal["proposal_id"], expected_version=1)

        self.assertEqual(
            [event["event_type"] for event in self.state.audit_events()],
            ["state_created", "state_update_proposed", "state_updated"],
        )


if __name__ == "__main__":
    unittest.main()
