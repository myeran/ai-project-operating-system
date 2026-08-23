import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from skill_contract import SkillDefinitionLoader  # noqa: E402
from skill_registry import SkillRegistry  # noqa: E402
from ux_ui_skill import UXUISkill, UXUISkillError  # noqa: E402


class UXUISkillTests(unittest.TestCase):
    def setUp(self):
        self.skill = UXUISkill()

    def context(self):
        return {
            "project_context": {"project_type": "Product", "project_goal": "Test UX"},
            "approved_goals": ["Make the first workflow understandable"],
            "approved_scope": {"in_scope": ["Primary workflow"], "out_of_scope": ["Advanced settings"]},
            "current_phase": "Design",
            "constraints": ["Small initial release"],
            "target_users": ["New user"],
            "user_workflows": ["Find an option and review the result"],
            "existing_decisions": ["Start with one primary flow"],
            "resources": ["Existing design system"],
        }

    def test_definition_is_machine_readable(self):
        contract = SkillDefinitionLoader().load(self.skill.definition_path)
        self.assertEqual(contract.name, "UX/UI Skill")
        self.assertEqual(contract.version, "1.0.0")
        self.assertIn("target_users", contract.required_inputs)

    def test_missing_input_is_rejected(self):
        with self.assertRaises(UXUISkillError):
            self.skill.execute({"project_context": {}})

    def test_design_is_valid_and_recommendation_only(self):
        result = self.skill.execute(self.context())
        output = result["output"]
        contract = SkillDefinitionLoader().load(self.skill.definition_path)
        self.assertEqual(result["skill_name"], "UX/UI Skill")
        self.assertEqual(set(output), set(contract.required_outputs))
        self.assertEqual(output["ux_ui_artifact"]["status"], "recommendation_only")
        self.assertTrue(output["ux_ui_artifact"]["requires_human_approval"])
        self.assertFalse(output["ux_ui_artifact"]["scope_changed"])
        self.assertFalse(output["ux_ui_artifact"]["implementation_committed"])

    def test_skill_is_registered(self):
        self.assertIsInstance(SkillRegistry().resolve("UX/UI Skill"), UXUISkill)


if __name__ == "__main__":
    unittest.main()
