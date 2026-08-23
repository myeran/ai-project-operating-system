import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from discovery_skill import DiscoverySkill, DiscoverySkillError  # noqa: E402
from skill_contract import SkillContractError, SkillDefinitionLoader  # noqa: E402


class SkillExecutionContractTests(unittest.TestCase):
    def setUp(self):
        self.skill = DiscoverySkill()
        self.contract = SkillDefinitionLoader().load(self.skill.definition_path)

    def test_definition_is_loaded(self):
        self.assertEqual(self.contract.name, "Discovery Skill")
        self.assertEqual(self.contract.version, "1.1.0")
        self.assertIn("project_name", self.contract.required_inputs)

    def test_missing_input_is_rejected(self):
        with self.assertRaises(DiscoverySkillError):
            self.skill.execute({"project_name": "Incomplete"})

    def test_invalid_output_is_rejected(self):
        output = {
            key: [] for key in self.contract.required_outputs
        }
        output["problem_statement"] = "Problem"
        output["initial_scope"] = {"in_scope": [], "out_of_scope": []}
        output["recommended_next_action"] = "Validate"
        output["confirmed_findings"] = "not-a-list"
        with self.assertRaises(SkillContractError):
            self.contract.validate_output(output)

    def test_valid_discovery_output_is_accepted(self):
        result = self.skill.execute(
            {
                "project_name": "Valid Project",
                "current_phase": "Discovery",
                "project_context": {"project_type": "Product"},
                "confirmed_findings": [],
            }
        )
        self.assertEqual(result["skill_version"], "1.1.0")
        self.assertEqual(set(result["output"]), set(self.contract.required_outputs))

    def test_compliance_failure_is_returned(self):
        with self.assertRaises(DiscoverySkillError) as error:
            self.skill.execute(
                {
                    "project_name": "Invalid Decision Project",
                    "current_phase": "Discovery",
                    "project_context": {"project_type": "Product"},
                    "decisions": [{"decision": "Build a feature"}],
                }
            )
        self.assertIn("explicitly approved", str(error.exception))


if __name__ == "__main__":
    unittest.main()
