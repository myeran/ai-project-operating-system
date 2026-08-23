"""Runtime adapter for the Project Planning Skill Definition."""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    from .skill_contract import SkillContractError, SkillDefinitionLoader
except ImportError:  # Supports direct test-module execution.
    from skill_contract import SkillContractError, SkillDefinitionLoader


class ProjectPlanningSkillError(SkillContractError):
    """Project Planning could not be resolved, executed, or validated."""


class ProjectPlanningSkill:
    """Create a recommendation-only project plan without mutating Runtime State."""

    name = "Project Planning Skill"

    def __init__(self, definition_path: str | Path | None = None) -> None:
        self.definition_path = Path(
            definition_path
            or Path(__file__).parents[1] / "03_Skill_Registry" / "Skills" / "Project Planning Skill.md"
        )
        self.loader = SkillDefinitionLoader()

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        try:
            contract = self.loader.load(self.definition_path)
            contract.validate_input(context)

            work_breakdown = context.get("work_breakdown") or self._default_work_breakdown(context)
            milestones = context.get("milestones") or self._default_milestones(work_breakdown)
            output = {
                "findings": self._findings(context),
                "work_breakdown": list(work_breakdown),
                "sequencing": list(milestones),
                "recommendations": list(context.get("recommendations") or [
                    "Execute the plan in sequence and validate each milestone before continuing."
                ]),
                "risks_and_dependencies": self._risks_and_dependencies(context),
                "decisions_needed": list(context.get("decisions_needed") or [
                    "Project owner approval of the proposed plan, owners, and resource assumptions."
                ]),
                "project_plan_artifact": {
                    "project_context": context["project_context"],
                    "approved_goals": list(context["approved_goals"]),
                    "approved_scope": context["approved_scope"],
                    "current_phase": context["current_phase"],
                    "constraints": list(context["constraints"]),
                    "resources": list(context["resources"]),
                    "owners": list(context["owners"]),
                    "milestones": list(milestones),
                    "status": "recommendation_only",
                    "requires_human_approval": True,
                    "scope_changed": False,
                    "resources_committed": False,
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
            raise ProjectPlanningSkillError(str(exc)) from exc

    @staticmethod
    def _default_work_breakdown(context: dict[str, Any]) -> list[dict[str, Any]]:
        return [
            {"task": "Confirm goals and scope", "owner": context["owners"][0] if context["owners"] else None, "depends_on": []},
            {"task": "Prepare the first milestone deliverable", "owner": None, "depends_on": ["Confirm goals and scope"]},
            {"task": "Validate the milestone and update the plan", "owner": None, "depends_on": ["Prepare the first milestone deliverable"]},
        ]

    @staticmethod
    def _default_milestones(work_breakdown: list[Any]) -> list[dict[str, Any]]:
        return [
            {"milestone": "Plan approved", "deliverables": [work_breakdown[0]["task"]]},
            {"milestone": "First deliverable ready", "deliverables": [work_breakdown[1]["task"]]},
            {"milestone": "Plan checkpoint complete", "deliverables": [work_breakdown[2]["task"]]},
        ]

    @staticmethod
    def _findings(context: dict[str, Any]) -> list[str]:
        return [
            f"Planning is based on the approved goals and scope for phase {context['current_phase']}.",
            "The proposed plan does not by itself approve scope, budget, or resource commitments.",
        ]

    @staticmethod
    def _risks_and_dependencies(context: dict[str, Any]) -> list[Any]:
        return list(context["risks"]) + list(context["dependencies"])
