"""Runtime adapter for the UX/UI Skill Definition."""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    from .skill_contract import SkillContractError, SkillDefinitionLoader
except ImportError:  # Supports direct test-module execution.
    from skill_contract import SkillContractError, SkillDefinitionLoader


class UXUISkillError(SkillContractError):
    """UX/UI could not be resolved, executed, or validated."""


class UXUISkill:
    """Create recommendation-only UX/UI guidance without mutating Runtime State."""

    name = "UX/UI Skill"

    def __init__(self, definition_path: str | Path | None = None) -> None:
        self.definition_path = Path(
            definition_path
            or Path(__file__).parents[1] / "03_Skill_Registry" / "Skills" / "UX UI Skill.md"
        )
        self.loader = SkillDefinitionLoader()

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        try:
            contract = self.loader.load(self.definition_path)
            contract.validate_input(context)
            user_flows = list(context.get("user_flows") or self._default_user_flows(context))
            output = {
                "findings": [
                    f"UX/UI recommendations are based on the approved scope for phase {context['current_phase']}.",
                    "The proposed interface remains subject to user validation and human approval.",
                ],
                "user_needs": list(context.get("user_needs") or [
                    f"Enable {user} to complete the primary workflow with clear feedback." 
                    for user in context["target_users"]
                ]),
                "information_architecture": list(context.get("information_architecture") or [
                    {"area": "Primary workflow", "contents": ["Start", "Progress", "Outcome"]}
                ]),
                "user_flows": user_flows,
                "interface_recommendations": list(context.get("interface_recommendations") or [
                    "Keep the primary action visible and provide clear progress and error feedback.",
                    "Use consistent hierarchy, labels, and interaction patterns.",
                ]),
                "accessibility_risks": [
                    "Color must not be the only channel for status or errors.",
                    "Keyboard navigation, focus order, and readable contrast require validation.",
                ],
                "decisions_needed": list(context.get("decisions_needed") or [
                    "Approve the primary user flow and the minimum accessibility acceptance criteria."
                ]),
                "ux_ui_artifact": {
                    "project_context": context["project_context"],
                    "approved_scope": context["approved_scope"],
                    "design_system": context.get("design_system") or "To be selected",
                    "status": "recommendation_only",
                    "requires_human_approval": True,
                    "scope_changed": False,
                    "implementation_committed": False,
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
            raise UXUISkillError(str(exc)) from exc

    @staticmethod
    def _default_user_flows(context: dict[str, Any]) -> list[dict[str, Any]]:
        return [{
            "flow": "Primary user journey",
            "user": context["target_users"][0] if context["target_users"] else "Target user",
            "steps": ["Enter", "Complete primary task", "Review outcome"],
        }]
