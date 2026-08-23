"""Read-only project roadmap projection over canonical Runtime sources."""

from __future__ import annotations

from typing import Any, Callable, Mapping

DEFAULT_PHASE_TRANSITIONS = {
    "Discovery": {"Strategy"}, "Strategy": {"Planning"}, "Planning": {"Design", "Execution"},
    "Design": {"Execution"}, "Execution": {"Validation"}, "Validation": {"Launch", "Learning"},
    "Launch": {"Learning"}, "Learning": {"Completed"}, "Completed": set(),
}
DEFAULT_PHASE_SKILLS = {
    "Discovery": "Discovery Skill", "Strategy": "Product Strategy Skill", "Planning": "Project Planning Skill",
    "Design": "UX/UI Skill", "Execution": "Engineering Skill", "Validation": "Review Skill",
    "Launch": "Launch Skill", "Learning": "Documentation Skill",
}

class ProjectNavigatorSkill:
    """Present lifecycle progress without activating Skills or changing State."""

    name = "project_navigator_skill"

    def __init__(self, phase_transitions: Mapping[str, set[str]] | None = None, phase_skills: Mapping[str, str] | None = None):
        self._phase_transitions = phase_transitions or DEFAULT_PHASE_TRANSITIONS
        self._phase_skills = phase_skills or DEFAULT_PHASE_SKILLS

    def navigate(
        self,
        state: Mapping[str, Any],
        phase_guidance: Mapping[str, Any],
        *,
        skill_available: Callable[[str], bool] | None = None,
    ) -> dict[str, Any]:
        phases = self._ordered_phases()
        current = state.get("phase")
        current_index = phases.index(current) if current in phases else -1
        transition_ready = state.get("status") == "completed" and current != "Completed"
        next_phase = phases[current_index + 1] if transition_ready and current_index + 1 < len(phases) else None
        next_skill = self._phase_skills.get(next_phase or current)
        guidance = dict(phase_guidance)
        steps = []
        for index, phase in enumerate(phases):
            if phase == current:
                status = "current"
            elif current_index >= 0 and index < current_index:
                status = "completed"
            else:
                status = "pending"
            skill = self._phase_skills.get(phase)
            steps.append({
                "phase": phase,
                "status": status,
                "responsible_skill": skill,
                "skill_registered": bool(skill and (skill_available(skill) if skill_available else True)),
                "completed": list(guidance.get("completed", [])) if status == "current" else [],
                "missing": list(guidance.get("missing", [])) if status == "current" else [],
            })
        if transition_ready and next_phase:
            next_action = "הפעל את השלב הבא"
        elif current:
            next_action = guidance.get("next_recommended_action") or "השלם את תנאי השלב הנוכחי"
        else:
            next_action = "לא ניתן לזהות את השלב הנוכחי"
        return {
            "navigator": self.name,
            "project_id": state.get("project_id"),
            "current_phase": current,
            "current_status": state.get("status"),
            "steps": steps,
            "completed": list(guidance.get("completed", [])),
            "missing": list(guidance.get("missing", [])),
            "current_skill": self._phase_skills.get(current),
            "next_phase": next_phase,
            "next_skill": next_skill,
            "next_action": next_action,
            "can_advance": bool(transition_ready and next_phase),
            "state_version": state.get("version"),
            "read_only": True,
        }

    def _ordered_phases(self) -> list[str]:
        phases = set(self._phase_transitions)
        phases.update(phase for targets in self._phase_transitions.values() for phase in targets)
        roots = sorted(phase for phase in phases if not any(phase in targets for targets in self._phase_transitions.values()))
        ordered: list[str] = []

        def visit(phase: str) -> None:
            if phase in ordered:
                return
            ordered.append(phase)
            for child in sorted(self._phase_transitions.get(phase, set())):
                visit(child)

        for root in roots:
            visit(root)
        return ordered
