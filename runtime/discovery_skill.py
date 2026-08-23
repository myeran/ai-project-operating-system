"""Runtime adapter for the existing Discovery Skill Definition."""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    from .skill_contract import SkillContractError, SkillDefinitionLoader
except ImportError:  # Supports direct test-module execution.
    from skill_contract import SkillContractError, SkillDefinitionLoader


class DiscoverySkillError(SkillContractError):
    """Discovery Skill could not be resolved, executed, or validated."""


class DiscoverySkill:
    """Execute Discovery while taking behavior rules from its Definition."""

    name = "Discovery Skill"

    def __init__(self, definition_path: str | Path | None = None) -> None:
        self.definition_path = Path(
            definition_path
            or Path(__file__).parents[1] / "03_Skill_Registry" / "Skills" / "Discovery Skill.md"
        )
        self.loader = SkillDefinitionLoader()

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        try:
            contract = self.loader.load(self.definition_path)
            contract.validate_input(context)

            def value(key: str, default: Any) -> Any:
                supplied = context.get(key)
                return default if supplied is None else supplied

            rules = contract.execution_rules
            confirmed_findings = value("confirmed_findings", [])
            open_questions = value("open_questions", None)
            validation_required = value("validation_required", None)
            has_validated_findings = bool(confirmed_findings)
            output = {
                "problem_statement": value(
                    "problem_statement", rules["default_problem_statement"]
                ),
                "confirmed_findings": confirmed_findings,
                "assumptions": value("assumptions", []),
                "decisions": value("decisions", []),
                "user_needs": value("user_needs", []),
                "initial_scope": value(
                    "initial_scope", {"in_scope": [], "out_of_scope": []}
                ),
                "open_questions": (
                    rules["initial_discovery_questions"]
                    if open_questions is None and not has_validated_findings
                    else (open_questions or [])
                ),
                "risks": value(
                    "risks", {"confirmed": [], "potential": [], "unknown": []}
                ),
                "validation_required": (
                    rules["initial_validation_required"]
                    if validation_required is None and not has_validated_findings
                    else (validation_required or [])
                ),
                "recommended_next_action": value(
                    "recommended_next_action", rules["default_recommended_next_action"]
                ),
            }
            contract.validate_output(output)
            return {
                "skill_name": contract.name,
                "skill_version": contract.version,
                "contract_path": str(contract.definition_path),
                "output": output,
            }
        except SkillContractError as exc:
            raise DiscoverySkillError(str(exc)) from exc

