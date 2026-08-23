import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from project_planning_skill import ProjectPlanningSkill, ProjectPlanningSkillError  # noqa: E402
from skill_registry import SkillRegistry  # noqa: E402
from skill_contract import SkillDefinitionLoader  # noqa: E402


class ProjectPlanningSkillTests(unittest.TestCase):
    def setUp(self):
        self.skill = ProjectPlanningSkill()

    def context(self):
        return {
            "project_context": {"project_type": "Product", "project_goal": "Test planning"},
            "approved_goals": ["Deliver a validated first milestone"],
            "approved_scope": {"in_scope": ["First milestone"], "out_of_scope": ["Later extensions"]},
            "current_phase": "Planning",
            "constraints": ["Small initial team"],
            "resources": ["One engineer"],
            "owners": ["Project owner"],
            "existing_decisions": ["Start with a narrow milestone"],
            "risks": ["Owner availability may change"],
            "dependencies": ["Approved requirements"],
        }

    def test_definition_is_machine_readable(self):
        contract = SkillDefinitionLoader().load(self.skill.definition_path)
        self.assertEqual(contract.name, "Project Planning Skill")
        self.assertEqual(contract.version, "1.0.0")
        self.assertIn("approved_scope", contract.required_inputs)

    def test_missing_input_is_rejected(self):
        with self.assertRaises(ProjectPlanningSkillError):
            self.skill.execute({"project_context": {}})

    def test_plan_is_valid_and_recommendation_only(self):
        result = self.skill.execute(self.context())
        output = result["output"]
        self.assertEqual(result["skill_name"], "Project Planning Skill")
        self.assertEqual(set(output), set(SkillDefinitionLoader().load(self.skill.definition_path).required_outputs))
        self.assertEqual(output["project_plan_artifact"]["status"], "recommendation_only")
        self.assertTrue(output["project_plan_artifact"]["requires_human_approval"])
        self.assertFalse(output["project_plan_artifact"]["scope_changed"])
        self.assertFalse(output["project_plan_artifact"]["resources_committed"])

    def test_skill_is_registered(self):
        self.assertIsInstance(SkillRegistry().resolve("Project Planning Skill"), ProjectPlanningSkill)


if __name__ == "__main__":
    unittest.main()
