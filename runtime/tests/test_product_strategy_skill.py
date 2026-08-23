import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from product_strategy_skill import ProductStrategySkill  # noqa: E402


class ProductStrategySkillTests(unittest.TestCase):
    def setUp(self):
        self.skill = ProductStrategySkill()

    def context(self):
        return {
            "project_context": {"project_type": "Product", "project_goal": "Test direction"},
            "discovery_findings": ["Users experience a fragmented workflow"],
            "goals": ["Clarify the product direction"],
            "constraints": ["Small initial scope"],
            "existing_decisions": [],
            "available_knowledge": {},
        }

    def test_definition_and_output_contract(self):
        result = self.skill.execute(self.context())
        self.assertEqual(result["skill_name"], "Product Strategy Skill")
        for field in (
            "findings",
            "strategic_analysis",
            "options_considered",
            "recommendations",
            "risks",
            "decisions_needed",
            "strategy_artifact",
        ):
            self.assertIn(field, result["output"])

    def test_strategy_is_recommendation_only(self):
        result = self.skill.execute(self.context())
        self.assertEqual(result["output"]["strategy_artifact"]["status"], "recommendation_only")
        self.assertTrue(result["output"]["strategy_artifact"]["requires_human_approval"])


if __name__ == "__main__":
    unittest.main()
