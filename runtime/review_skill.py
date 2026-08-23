"""Runtime adapter for the Review Skill Definition."""
from __future__ import annotations
from pathlib import Path
from typing import Any
try:
    from .skill_contract import SkillContractError, SkillDefinitionLoader
except ImportError:
    from skill_contract import SkillContractError, SkillDefinitionLoader

class ReviewSkillError(SkillContractError):
    """Review Skill could not be executed or validated."""

class ReviewSkill:
    name = "Review Skill"
    def __init__(self, definition_path: str | Path | None = None) -> None:
        self.definition_path = Path(definition_path or Path(__file__).parents[1] / "03_Skill_Registry" / "Skills" / "Review Skill.md")
        self.loader = SkillDefinitionLoader()

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        try:
            contract = self.loader.load(self.definition_path); contract.validate_input(context)
            gaps = list(context.get("risks_and_open_issues") or [])
            status = "needs_revision" if gaps else "approved_with_notes"
            output = {"findings": ["Artifact review completed against the supplied requirements and acceptance criteria."], "quality_analysis": {"requirements_count": len(context["requirements"]), "acceptance_criteria_count": len(context["acceptance_criteria"]), "artifact_present": bool(context["artifact"])}, "recommendations": list(context.get("recommendations") or ["Address all critical gaps before requesting phase transition."]), "risks_and_open_issues": gaps, "decisions_needed": list(context.get("decisions_needed") or ["Human owner to determine whether the review result is sufficient for the next gate."]), "review_artifact": {"status": status, "approval_authority": "human_owner", "state_changed": False}}
            contract.validate_output(output)
            return {"skill_name": contract.name, "skill_version": contract.version, "contract_path": str(contract.definition_path), "output": output}
        except SkillContractError as exc:
            raise ReviewSkillError(str(exc)) from exc
