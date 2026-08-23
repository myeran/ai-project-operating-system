"""Runtime adapter for the existing Product Strategy Skill Definition."""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    from .skill_contract import SkillContractError, SkillDefinitionLoader
except ImportError:  # Supports direct test-module execution.
    from skill_contract import SkillContractError, SkillDefinitionLoader


class ProductStrategySkillError(SkillContractError):
    """Product Strategy could not be resolved, executed, or validated."""


class ProductStrategySkill:
    """Execute Product Strategy under its machine-readable Definition contract."""

    name = "Product Strategy Skill"

    def __init__(self, definition_path: str | Path | None = None) -> None:
        self.definition_path = Path(
            definition_path
            or Path(__file__).parents[1] / "03_Skill_Registry" / "Skills" / "Product Strategy Skill.md"
        )
        self.loader = SkillDefinitionLoader()

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        try:
            contract = self.loader.load(self.definition_path)
            contract.validate_input(context)
            discovery = context["discovery_findings"]
            goals = context["goals"]
            constraints = context["constraints"]
            existing_decisions = context["existing_decisions"]
            output = {
                "findings": list(discovery) if isinstance(discovery, list) else [discovery],
                "strategic_analysis": {
                    "project_context": context["project_context"],
                    "goals": goals,
                    "constraints": constraints,
                    "existing_decisions": existing_decisions,
                    "validated_problem": context.get("problem_statement", ""),
                },
                "options_considered": context.get(
                    "options_considered"
                ) or [
                    {
                        "option": "Focused initial direction",
                        "advantages": ["Keeps the first strategy narrow and testable"],
                        "disadvantages": ["May defer broader opportunities"],
                        "risks": ["Requires validation before commitment"],
                    }
                ],
                "recommendations": context.get(
                    "recommendations"
                ) or [
                    "Recommendation based on current information: validate the focused direction before commitment"
                ],
                "risks": context.get(
                    "risks"
                ) or [
                    "Strategic direction remains provisional until owner approval"
                ],
                "decisions_needed": context.get(
                    "decisions_needed"
                ) or [
                    "Project owner approval of strategic direction"
                ],
                "strategy_artifact": {
                    "direction": "Provisional product direction",
                    "status": "recommendation_only",
                    "requires_human_approval": True,
                },
            }
            contract.validate_output(output)
            return {
                "skill_name": contract.name,
                "skill_version": contract.version,
                "contract_path": str(contract.definition_path),
                "output": output,
            }
        except SkillContractError as exc:
            raise ProductStrategySkillError(str(exc)) from exc
