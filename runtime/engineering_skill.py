"""Runtime adapter for the Engineering Skill Definition."""
from __future__ import annotations
from pathlib import Path
from typing import Any
try:
    from .skill_contract import SkillContractError, SkillDefinitionLoader
except ImportError:
    from skill_contract import SkillContractError, SkillDefinitionLoader

class EngineeringSkillError(SkillContractError):
    """Engineering Skill could not be executed or validated."""

class EngineeringSkill:
    name = "Engineering Skill"
    def __init__(self, definition_path: str | Path | None = None) -> None:
        self.definition_path = Path(definition_path or Path(__file__).parents[1] / "03_Skill_Registry" / "Skills" / "Engineering Skill.md")
        self.loader = SkillDefinitionLoader()

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        try:
            contract = self.loader.load(self.definition_path); contract.validate_input(context)
            work_items = list(context.get("work_items") or [{"task": "Implement the approved first milestone", "owner": context["owners"][0] if context["owners"] else None}])
            output = {"findings": ["The technical recommendation is based on the approved plan and scope."], "implementation_plan": context["project_plan"], "work_items": work_items, "technical_recommendations": list(context.get("technical_recommendations") or ["Implement the smallest testable slice and add focused checks before integration."]), "risks": list(context.get("risks") or ["Technical assumptions require validation during implementation."]), "decisions_needed": list(context.get("decisions_needed") or ["Approve the technical approach and implementation ownership."]), "engineering_artifact": {"status": "recommendation_only", "requires_human_approval": True, "scope_changed": False, "code_committed": False}}
            contract.validate_output(output)
            return {"skill_name": contract.name, "skill_version": contract.version, "contract_path": str(contract.definition_path), "output": output}
        except SkillContractError as exc:
            raise EngineeringSkillError(str(exc)) from exc
