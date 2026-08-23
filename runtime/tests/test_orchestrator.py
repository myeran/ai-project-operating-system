import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from bootstrap_handler import BootstrapRequest, ProjectInstanceBootstrapHandler  # noqa: E402
from orchestrator import ProjectOrchestrator  # noqa: E402
from project_resolver import ResolutionResult  # noqa: E402
from registry_adapter import ProjectRegistryAdapter  # noqa: E402
from state_adapter import StateAdapter  # noqa: E402


class ProjectOrchestratorMVPTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database = str(Path(self.temp_dir.name) / "runtime.sqlite3")
        self.registry = ProjectRegistryAdapter(self.database)
        self.state = StateAdapter(self.database)
        self.bootstrap = ProjectInstanceBootstrapHandler(self.registry, self.state)
        self.orchestrator = ProjectOrchestrator(self.bootstrap, self.state)

    def tearDown(self):
        self.state.close()
        self.registry.close()
        self.temp_dir.cleanup()

    def request(self):
        return BootstrapRequest(
            project_name="Orchestrated Habit Tracker",
            owner="owner-1",
            description="A project started through the orchestrator.",
            os_version="v1.0",
            actor="project-entry",
        )

    def test_start_project_connects_bootstrap_and_state(self):
        result = self.orchestrator.start_project(self.request())

        self.assertEqual(result["current_phase"], "Discovery")
        self.assertEqual(result["status"], "proposed")
        self.assertFalse(result["execution_allowed"])
        self.assertFalse(result["discovery_executed"])
        self.assertEqual(result["active_capability"], "Discovery Skill")
        self.assertIn("required_user_action", result["phase_guidance"])

    def test_phase_mapping_selects_discovery_skill(self):
        self.assertEqual(self.orchestrator.skill_for_phase("Discovery"), "Discovery Skill")
        initialized = self.orchestrator.start_project(
            BootstrapRequest(
                project_name="Activated Discovery",
                owner="owner-1",
                description="Context supplied for activation.",
                os_version="v1.0",
                project_context={"project_type": "Product"},
                actor="project-entry",
            ),
            activate_skill=True,
        )
        self.assertEqual(initialized["discovery_status"], "COMPLETED")
        self.assertEqual(initialized["active_skill"], "Discovery Skill")
        self.assertTrue(initialized["state_update_proposal"])

    def test_missing_phase_skill_fails_closed(self):
        initialized = self.orchestrator.start_project(self.request())
        self.state._connection.execute(
            "UPDATE project_state SET phase = ? WHERE project_id = ?",
            ("Launch", initialized["project_id"]),
        )
        self.state._connection.commit()
        result = self.orchestrator.activate_current_phase(
            ResolutionResult(status="RESOLVED", project_id=initialized["project_id"])
        )
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("Skill", result["error"])
        self.assertFalse(result["execution_allowed"])

    def test_strategy_phase_activates_product_strategy_skill(self):
        initialized = self.orchestrator.start_project(self.request())
        self.state._connection.execute(
            "UPDATE project_state SET phase = ? WHERE project_id = ?",
            ("Strategy", initialized["project_id"]),
        )
        self.state._connection.commit()
        result = self.orchestrator.activate_current_phase(
            ResolutionResult(status="RESOLVED", project_id=initialized["project_id"]),
            context={
                "discovery_findings": ["Validated user problem"],
                "project_context": {"project_type": "Product"},
            },
        )
        self.assertEqual(result["active_skill"], "Product Strategy Skill")
        self.assertEqual(result["skill_status"], "COMPLETED")
        self.assertTrue(result["state_update_proposal"])

    def test_continue_project_reads_current_state(self):
        initialized = self.orchestrator.start_project(self.request())

        result = self.orchestrator.continue_project(initialized["project_id"])

        self.assertEqual(result["project_id"], initialized["project_id"])
        self.assertEqual(result["state_version"], 1)
        self.assertEqual(result["phase_guidance"]["phase_status"]["current_phase"], "Discovery")

    def test_guidance_contract_is_complete(self):
        result = self.orchestrator.start_project(self.request())
        guidance = result["phase_guidance"]

        self.assertEqual(
            set(guidance),
            {
                "phase_status",
                "completed",
                "missing",
                "required_user_action",
                "expected_output",
                "completion_criteria",
                "next_recommended_action",
            },
        )
        self.assertTrue(guidance["required_user_action"])
        self.assertTrue(guidance["expected_output"])
        self.assertTrue(guidance["completion_criteria"])

    def test_orchestrator_does_not_change_state_on_continue(self):
        initialized = self.orchestrator.start_project(self.request())
        before = self.state.get_state(initialized["project_id"])

        self.orchestrator.continue_project(initialized["project_id"])
        after = self.state.get_state(initialized["project_id"])

        self.assertEqual(after["version"], before["version"])
        self.assertEqual(after["status"], before["status"])

    def test_resolved_project_generates_full_orchestration_result(self):
        initialized = self.orchestrator.start_project(self.request())
        resolution = ResolutionResult(
            status="RESOLVED",
            project_id=initialized["project_id"],
            project_name="Orchestrated Habit Tracker",
            current_phase="Discovery",
            current_status="proposed",
            os_version="v1.0",
        )

        result = self.orchestrator.orchestrate(resolution)

        self.assertEqual(result["result_type"], "Orchestration Result")
        self.assertTrue(result["state_loaded"])
        self.assertEqual(result["current_phase"], "Discovery")
        self.assertIsNone(result["state_update_proposal"])

    def test_completed_phase_returns_transition_proposal_without_transitioning(self):
        initialized = self.orchestrator.start_project(self.request())
        proposal = self.state.propose_state_update(
            initialized["project_id"],
            {"status": "completed"},
            actor="reviewer",
        )
        self.state.commit_state_update(proposal["proposal_id"], expected_version=1)

        resolution = ResolutionResult(
            status="RESOLVED",
            project_id=initialized["project_id"],
            current_phase="Discovery",
            current_status="completed",
        )
        result = self.orchestrator.orchestrate(resolution)

        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["state_update_proposal"]["to_phase"], "Strategy")
        self.assertTrue(result["state_update_proposal"]["requires_approval"])
        self.assertEqual(self.state.get_state(initialized["project_id"])["phase"], "Discovery")

    def test_unresolved_project_is_blocked_without_state_load(self):
        result = self.orchestrator.orchestrate(ResolutionResult(status="NOT_FOUND"))

        self.assertEqual(result["status"], "BLOCKED")
        self.assertFalse(result["state_loaded"])
        self.assertIsNone(result["state_update_proposal"])

    def test_invalid_state_fails_safely(self):
        initialized = self.orchestrator.start_project(self.request())
        self.state._connection.execute(
            "UPDATE project_state SET phase = ? WHERE project_id = ?",
            ("InvalidPhase", initialized["project_id"]),
        )
        self.state._connection.commit()

        result = self.orchestrator.orchestrate(
            ResolutionResult(status="RESOLVED", project_id=initialized["project_id"])
        )

        self.assertEqual(result["status"], "BLOCKED")
        self.assertFalse(result["state_loaded"])


if __name__ == "__main__":
    unittest.main()
