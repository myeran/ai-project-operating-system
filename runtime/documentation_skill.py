"""Runtime adapter for the Documentation Skill Definition."""
from __future__ import annotations
from pathlib import Path
from typing import Any
try:
    from .skill_contract import SkillContractError, SkillDefinitionLoader
except ImportError:
    from skill_contract import SkillContractError, SkillDefinitionLoader

class DocumentationSkillError(SkillContractError):
    """Documentation Skill could not be executed or validated."""

class DocumentationSkill:
    name = "Documentation Skill"
    def __init__(self, definition_path: str | Path | None = None) -> None:
        self.definition_path = Path(definition_path or Path(__file__).parents[1] / "03_Skill_Registry" / "Skills" / "Documentation Skill.md")
        self.loader = SkillDefinitionLoader()

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        try:
            contract = self.loader.load(self.definition_path); contract.validate_input(context)
            output = {"findings": ["Source material is ready to be organized for the stated documentation purpose."], "documentation_analysis": {"purpose": context["document_purpose"], "destination": context["destination"], "source_items": len(context["source_material"]), "source_of_truth": context["destination"]}, "recommendations": list(context.get("recommendations") or ["Keep the document focused, distinguish facts from assumptions, and link back to the source of truth."]), "knowledge_risks": ["Conflicting or stale source material should be resolved before publication."], "decisions_needed": list(context.get("decisions_needed") or ["Confirm document ownership and the authoritative destination."]), "documentation_artifact": {"status": "draft_recommendation", "requires_human_approval": True, "source_updated": False, "destination": context["destination"]}}
            contract.validate_output(output)
            return {"skill_name": contract.name, "skill_version": contract.version, "contract_path": str(contract.definition_path), "output": output}
        except SkillContractError as exc:
            raise DocumentationSkillError(str(exc)) from exc
