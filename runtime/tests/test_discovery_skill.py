import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from bootstrap_handler import BootstrapRequest, ProjectInstanceBootstrapHandler  # noqa: E402
from discovery_skill import DiscoverySkill  # noqa: E402
from orchestrator import ProjectOrchestrator  # noqa: E402
from project_resolver import ProjectResolver  # noqa: E402
from registry_adapter import ProjectRegistryAdapter  # noqa: E402
from skill_registry import SkillRegistry  # noqa: E402
from state_adapter import StateAdapter  # noqa: E402


class DiscoverySkillIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        database = str(Path(self.temp_dir.name) / "runtime.sqlite3")
        self.registry = ProjectRegistryAdapter(database)
        self.state = StateAdapter(database)
        self.bootstrap = ProjectInstanceBootstrapHandler(self.registry, self.state)
        self.orchestrator = ProjectOrchestrator(self.bootstrap, self.state)
        initialized = self.bootstrap.initialize(
            BootstrapRequest(
                project_name="Discovery Integration Project",
                owner="owner-1",
                description="A project for Discovery integration.",
                os_version="v1.0",
            )
        )
        self.project_id = initialized["project_id"]

    def tearDown(self):
        self.state.close()
        self.registry.close()
        self.temp_dir.cleanup()

    def resolution(self):
        from runtime_gateway import RuntimeEntryGateway

        gateway_request = RuntimeEntryGateway().receive(
            "Continue Project",
            project_id=self.project_id,
        )
        return ProjectResolver(self.registry).resolve(gateway_request)

    def test_discovery_activation_returns_all_structured_sections(self):
        result = self.orchestrator.run_discovery(
            self.resolution(),
            {
                "problem_statement": "Users cannot keep project context in one place.",
                "confirmed_findings": [{"finding": "Context is spread across files", "source": "project evidence"}],
                "assumptions": [{"assumption": "Users want one workspace", "how_to_validate": "User interview"}],
            },
        )

        self.assertEqual(result["discovery_status"], "COMPLETED")
        self.assertEqual(result["active_skill"], "Discovery Skill")
        contract = self.orchestrator.skill_registry.resolve("Discovery Skill").loader.load(
            self.orchestrator.skill_registry.resolve("Discovery Skill").definition_path
        )
        self.assertEqual(set(result["discovery_output"]), set(contract.required_outputs))
        self.assertIsNotNone(result["state_update_proposal"])
        self.assertFalse(result["state_committed"])

    def test_initial_discovery_prioritizes_questions_and_validation(self):
        skill = DiscoverySkill()
        output = skill.execute(
            {
                "project_name": "Personal Habit Tracker",
                "current_phase": "Discovery",
                "project_context": {
                    "project_type": "Product",
                    "current_stage": "Idea",
                },
            }
        )["output"]

        self.assertEqual(output["confirmed_findings"], [])
        self.assertEqual(output["decisions"], [])
        contract = skill.loader.load(skill.definition_path)
        self.assertEqual(output["open_questions"], contract.execution_rules["initial_discovery_questions"])
        self.assertTrue(output["validation_required"])
        self.assertIn("Answer the Discovery questions", output["recommended_next_action"])
        self.assertNotIn("MVP", output["recommended_next_action"])
        self.assertEqual(output["initial_scope"], {"in_scope": [], "out_of_scope": []})

    def test_discovery_creates_proposal_without_committing_state(self):
        before = self.state.get_state(self.project_id)
        result = self.orchestrator.run_discovery(self.resolution(), {})
        after = self.state.get_state(self.project_id)

        self.assertEqual(before["version"], after["version"])
        self.assertEqual(after["completed_outputs"], [])
        proposal = result["state_update_proposal"]
        self.assertEqual(proposal["status"], "pending")
        self.assertIn("Discovery Output", proposal["changes"]["completed_outputs"])

    def test_missing_information_is_preserved_as_validation(self):
        result = self.orchestrator.run_discovery(
            self.resolution(),
            {"validation_required": ["Validate target user"]},
        )

        self.assertEqual(result["discovery_output"]["validation_required"], ["Validate target user"])
        self.assertEqual(result["phase_guidance"]["missing"], ["Validate target user"])

    def test_unavailable_skill_fails_safely(self):
        unavailable = ProjectOrchestrator(
            self.bootstrap,
            self.state,
            SkillRegistry(skills={}),
        )
        result = unavailable.run_discovery(self.resolution(), {})

        self.assertEqual(result["discovery_status"], "FAILED")
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIsNone(result["state_update_proposal"])


if __name__ == "__main__":
    unittest.main()
