"""Runtime adapter for the Launch Skill Definition."""
from __future__ import annotations
from pathlib import Path
from typing import Any
try:
    from .skill_contract import SkillContractError, SkillDefinitionLoader
except ImportError:
    from skill_contract import SkillContractError, SkillDefinitionLoader

class LaunchSkillError(SkillContractError):
    """Launch Skill could not be executed or validated."""

class LaunchSkill:
    name = "Launch Skill"
    def __init__(self, definition_path: str | Path | None = None) -> None:
        self.definition_path = Path(definition_path or Path(__file__).parents[1] / "03_Skill_Registry" / "Skills" / "Launch Skill.md")
        self.loader = SkillDefinitionLoader()

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        try:
            contract = self.loader.load(self.definition_path); contract.validate_input(context)
            output = {"findings": ["Launch preparation is based on the validated release artifact and approved scope."], "readiness_checks": list(context.get("validation_results") or ["Validation results are present and approved by the responsible owner.", "Monitoring and support ownership are confirmed.", "Rollback trigger and recovery path are documented."]), "rollout_plan": list(context.get("launch_requirements") or ["Begin with a controlled rollout, monitor agreed signals, and expand only after the checkpoint."]), "rollback_plan": ["Stop rollout when an agreed trigger is met.", "Restore the last known good version or state.", "Record the incident and reassess readiness."], "risks": list(context.get("known_risks") or ["Launch readiness depends on monitoring, support, and rollback ownership."]), "decisions_needed": list(context.get("decisions_needed") or ["Approve launch timing, rollout scope, and rollback authority."]), "launch_artifact": {"status": "recommendation_only", "requires_human_approval": True, "release_executed": False, "scope_changed": False}}
            contract.validate_output(output)
            return {"skill_name": contract.name, "skill_version": contract.version, "contract_path": str(contract.definition_path), "output": output}
        except SkillContractError as exc:
            raise LaunchSkillError(str(exc)) from exc
