import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from documentation_skill import DocumentationSkill  # noqa: E402
from engineering_skill import EngineeringSkill  # noqa: E402
from launch_skill import LaunchSkill  # noqa: E402
from review_skill import ReviewSkill  # noqa: E402
from skill_contract import SkillDefinitionLoader  # noqa: E402
from skill_registry import SkillRegistry  # noqa: E402


class RemainingLifecycleSkillTests(unittest.TestCase):
    def test_all_definitions_load_and_all_skills_are_registered(self):
        skills = (EngineeringSkill(), ReviewSkill(), LaunchSkill(), DocumentationSkill())
        registry = SkillRegistry()
        for skill in skills:
            contract = SkillDefinitionLoader().load(skill.definition_path)
            self.assertEqual(contract.name, skill.name)
            self.assertEqual(registry.resolve(skill.name).__class__, skill.__class__)

    def test_engineering_is_recommendation_only(self):
        result = EngineeringSkill().execute({
            "project_context": {}, "approved_goals": ["goal"], "approved_scope": {}, "current_phase": "Execution",
            "constraints": [], "resources": [], "owners": [], "project_plan": {}, "existing_decisions": [],
        })
        self.assertTrue(result["output"]["engineering_artifact"]["requires_human_approval"])
        self.assertFalse(result["output"]["engineering_artifact"]["code_committed"])

    def test_review_does_not_approve_or_change_state(self):
        result = ReviewSkill().execute({
            "project_context": {}, "current_phase": "Validation", "requirements": ["requirement"],
            "acceptance_criteria": ["criterion"], "existing_decisions": [], "architecture_rules": [],
            "artifact": {"name": "artifact"}, "risks_and_constraints": [],
        })
        self.assertEqual(result["output"]["review_artifact"]["approval_authority"], "human_owner")
        self.assertFalse(result["output"]["review_artifact"]["state_changed"])

    def test_launch_and_documentation_are_non_mutating(self):
        launch = LaunchSkill().execute({
            "project_context": {}, "approved_goals": [], "approved_scope": {}, "current_phase": "Launch",
            "constraints": [], "resources": [], "owners": [], "release_artifact": {}, "existing_decisions": [],
        })
        documentation = DocumentationSkill().execute({
            "project_context": {}, "current_phase": "Learning", "source_material": ["source"],
            "existing_decisions": [], "available_knowledge": {}, "destination": "Project Knowledge",
            "document_purpose": "Capture the launch learning",
        })
        self.assertFalse(launch["output"]["launch_artifact"]["release_executed"])
        self.assertFalse(documentation["output"]["documentation_artifact"]["source_updated"])


if __name__ == "__main__":
    unittest.main()
