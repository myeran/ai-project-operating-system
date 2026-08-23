"""Project Orchestrator connection for Bootstrap, State, and Discovery.

Discovery execution remains proposal-only: the Orchestrator activates the
existing Skill, structures its output, and never commits State or transitions
phases automatically.
"""

from __future__ import annotations

from typing import Any

try:
    from .bootstrap_handler import BootstrapRequest, ProjectInstanceBootstrapHandler
    from .project_resolver import ResolutionResult
    from .skill_registry import SkillRegistry, SkillRegistryError
    from .state_adapter import InvalidStateError, StateAdapter, StateAdapterError
    from .project_navigator_skill import ProjectNavigatorSkill, DEFAULT_PHASE_TRANSITIONS
except ImportError:  # Supports direct test-module execution.
    from bootstrap_handler import BootstrapRequest, ProjectInstanceBootstrapHandler
    from project_resolver import ResolutionResult
    from skill_registry import SkillRegistry, SkillRegistryError
    from state_adapter import InvalidStateError, StateAdapter, StateAdapterError
    from project_navigator_skill import ProjectNavigatorSkill, DEFAULT_PHASE_TRANSITIONS


class OrchestratorError(Exception):
    """Project Orchestrator boundary failure."""


PHASE_SKILL_MAP = {
    "Discovery": "Discovery Skill",
    "Strategy": "Product Strategy Skill",
    "Planning": "Project Planning Skill",
    "Design": "UX/UI Skill",
    "Execution": "Engineering Skill",
    "Validation": "Review Skill",
    "Launch": "Launch Skill",
    "Learning": "Documentation Skill",
}


class ProjectOrchestrator:
    """Connect Project Instance initialization to canonical State guidance."""

    def __init__(
        self,
        bootstrap: ProjectInstanceBootstrapHandler,
        state: StateAdapter,
        skill_registry: SkillRegistry | None = None,
    ) -> None:
        self.bootstrap = bootstrap
        self.state = state
        self.skill_registry = skill_registry or SkillRegistry()
        self.navigator = ProjectNavigatorSkill(DEFAULT_PHASE_TRANSITIONS, PHASE_SKILL_MAP)

    def project_navigator(self, resolution: ResolutionResult) -> dict[str, Any]:
        """Return a read-only roadmap projection from Registry + canonical State."""
        if resolution.status != "RESOLVED" or not resolution.project_id:
            return {"navigator": ProjectNavigatorSkill.name, "read_only": True, "can_advance": False,
                    "current_phase": None, "steps": [], "next_action": "לא ניתן לזהות את הפרויקט"}
        state = self.state.get_state(resolution.project_id)
        orchestration = self.orchestrate(resolution)
        return self.navigator.navigate(
            state,
            orchestration["phase_guidance"],
            skill_available=lambda name: self._skill_registered(name),
        )

    def _skill_registered(self, name: str) -> bool:
        try:
            self.skill_registry.resolve(name)
            return True
        except SkillRegistryError:
            return False

    def start_project(
        self,
        request: BootstrapRequest,
        *,
        activate_skill: bool = False,
    ) -> dict[str, Any]:
        """Bootstrap a project and optionally activate its current-phase Skill."""

        initialized = self.bootstrap.initialize(request)
        result = self._orchestration_result(
            project_id=initialized["project_id"],
            state=initialized["state"],
            action="Project Instance initialized; Discovery is ready to begin.",
        )
        result["initialized"] = initialized
        if activate_skill and request.project_context:
            resolution = ResolutionResult(
                status="RESOLVED",
                project_id=initialized["project_id"],
                project_name=request.project_name,
                current_phase=initialized["state"]["phase"],
                current_status=initialized["state"]["status"],
                os_version=initialized["os_version"],
            )
            activated = self.activate_current_phase(
                resolution,
                context={
                    "project_name": request.project_name,
                    "project_description": request.description,
                    "project_context": request.project_context,
                },
                actor=request.actor,
            )
            activated["initialized"] = initialized
            return activated
        return result

    def continue_project(self, project_id: str) -> dict[str, Any]:
        """Load canonical State and return guidance without changing it."""

        return self.orchestrate(
            ResolutionResult(status="RESOLVED", project_id=project_id)
        )

    def orchestrate(self, resolution: ResolutionResult) -> dict[str, Any]:
        """Load State for a resolved project and return guidance only."""

        if resolution.status != "RESOLVED" or not resolution.project_id:
            return {
                "result_type": "Orchestration Result",
                "project_id": resolution.project_id,
                "current_phase": None,
                "status": "BLOCKED",
                "state_loaded": False,
                "phase_guidance": self._blocked_guidance(
                    "Project Instance was not resolved; State was not loaded."
                ),
                "state_update_proposal": None,
            }
        try:
            state = self.state.get_state(resolution.project_id)
        except InvalidStateError as exc:
            return {
                "result_type": "Orchestration Result",
                "project_id": resolution.project_id,
                "current_phase": None,
                "status": "BLOCKED",
                "state_loaded": False,
                "phase_guidance": self._blocked_guidance(
                    "Canonical Project State is invalid and cannot be used safely."
                ),
                "state_update_proposal": None,
                "error": str(exc),
            }
        result = self._orchestration_result(
            project_id=resolution.project_id,
            state=state,
            action="Continue the current phase using the required user action.",
        )
        result["result_type"] = "Orchestration Result"
        result["state_loaded"] = True
        result["state_update_proposal"] = self._transition_proposal(state)
        if resolution.current_phase and resolution.current_phase != state["phase"]:
            result["status"] = "BLOCKED"
            result["phase_guidance"] = self._blocked_guidance(
                "Registry phase and canonical State phase do not match."
            )
            result["state_update_proposal"] = None
        if resolution.current_status and resolution.current_status != state["status"]:
            result["status"] = "BLOCKED"
            result["phase_guidance"] = self._blocked_guidance(
                "Registry status and canonical State status do not match."
            )
            result["state_update_proposal"] = None
        return result

    def run_discovery(
        self,
        resolution: ResolutionResult,
        context: dict[str, Any] | None = None,
        *,
        actor: str = "orchestrator",
    ) -> dict[str, Any]:
        """Compatibility wrapper for the current-phase activation path."""

        return self.activate_current_phase(resolution, context=context, actor=actor)

    def activate_current_phase(
        self,
        resolution: ResolutionResult,
        context: dict[str, Any] | None = None,
        *,
        actor: str = "orchestrator",
    ) -> dict[str, Any]:
        """Select the Skill for the canonical phase and activate it safely."""

        if resolution.status != "RESOLVED" or not resolution.project_id:
            return self._capability_failure(
                resolution.project_id,
                "Project Instance was not resolved; the current-phase Skill was not activated.",
            )
        try:
            state = self.state.get_state(resolution.project_id)
            skill_name = PHASE_SKILL_MAP.get(state["phase"])
            if not skill_name:
                return self._capability_failure(
                    resolution.project_id,
                    f"No Skill mapping exists for phase {state['phase']}.",
                    state=state,
                )
            skill = self.skill_registry.resolve(skill_name)
            skill_context = self._prepare_skill_context(skill_name, resolution, state, context or {})
            execution = skill.execute(skill_context)
            skill_output = execution["output"]
            changes = self._skill_state_changes(state, skill_name, skill_output)
            proposal = self.state.propose_state_update(
                resolution.project_id,
                changes,
                actor=actor,
            )
            proposed_state = dict(state)
            proposed_state.update(changes)
            guidance = self._phase_guidance(
                state["phase"],
                proposed_state,
                f"Validate the {skill_name} output and approve the next project action.",
            )
            result = {
                "result_type": "Orchestration Result",
                "project_id": resolution.project_id,
                "current_phase": state["phase"],
                "status": state["status"],
                "state_version": state["version"],
                "state_loaded": True,
                "skill_status": "COMPLETED",
                "active_skill": execution.get("skill_name", "Discovery Skill"),
                "skill_input": skill_context,
                "skill_output": skill_output,
                "phase_guidance": guidance,
                "state_update_proposal": proposal,
                "state_committed": False,
                "execution_allowed": False,
            }
            if skill_name == "Discovery Skill":
                result["discovery_status"] = "COMPLETED"
                result["discovery_input"] = skill_context
                result["discovery_output"] = skill_output
            return result
        except Exception as exc:
            return self._capability_failure(
                resolution.project_id,
                f"{skill_name if 'skill_name' in locals() else 'Current-phase Skill'} could not be completed safely: {exc}",
                state=state if 'state' in locals() else None,
            )

    @staticmethod
    def skill_for_phase(phase: str) -> str | None:
        """Return the canonical primary Skill name for a lifecycle phase."""

        return PHASE_SKILL_MAP.get(phase)

    @staticmethod
    def _prepare_skill_context(
        skill_name: str,
        resolution: ResolutionResult,
        state: dict[str, Any],
        supplied: dict[str, Any],
    ) -> dict[str, Any]:
        canonical = state.get("canonical_state") or {}
        identity = canonical.get("project_identity") or {}
        planning = canonical.get("planning_data") or {}
        decisions = canonical.get("decision_management") or {}
        discovery_context = {
            "project_name": supplied.get("project_name") or resolution.project_name or identity.get("name"),
            "project_description": supplied.get("project_description") or identity.get("description", ""),
            "project_context": supplied.get("project_context") or identity.get("project_context", {}),
            "current_phase": state["phase"],
            "existing_project_context": supplied.get("existing_project_context", {}),
            "known_information": supplied.get("known_information", {"project_identity": identity}),
            "missing_information": supplied.get("missing_information", state.get("missing_items") or []),
            # Preserve None so the Skill contract can supply its canonical
            # initial Discovery questions and validation requirements.
            "open_questions": supplied.get("open_questions"),
            "validation_required": supplied.get("validation_required"),
            "goals": supplied.get("goals", planning.get("goals", [])),
            "constraints": supplied.get("constraints", []),
            "existing_decisions": supplied.get("existing_decisions", decisions.get("decisions", [])),
        }
        if skill_name == "Product Strategy Skill":
            return {
                "project_context": discovery_context["project_context"],
                "discovery_findings": supplied.get(
                    "discovery_findings",
                    state.get("completed_outputs") or [],
                ),
                "problem_statement": supplied.get("problem_statement", ""),
                "goals": discovery_context["goals"],
                "constraints": discovery_context["constraints"],
                "existing_decisions": discovery_context["existing_decisions"],
                "available_knowledge": supplied.get("available_knowledge", {}),
                "options_considered": supplied.get("options_considered"),
                "recommendations": supplied.get("recommendations"),
                "risks": supplied.get("risks"),
                "decisions_needed": supplied.get("decisions_needed"),
            }
        return discovery_context

    @staticmethod
    def _skill_state_changes(
        state: dict[str, Any],
        skill_name: str,
        output: dict[str, Any],
    ) -> dict[str, Any]:
        if skill_name == "Discovery Skill":
            return ProjectOrchestrator._discovery_state_changes(state, output)
        if skill_name == "Product Strategy Skill":
            completed = list(state.get("completed_outputs") or [])
            artifact = "Product Strategy Output"
            if artifact not in completed:
                completed.append(artifact)
            return {
                "completed_outputs": completed,
                "missing_items": list(output["decisions_needed"]) or ["None identified"],
                "required_user_action": "Review the strategic recommendation and approve or revise the direction.",
                "expected_output": ["Strategic Analysis", "Options Considered", "Product Strategy Artifact"],
                "completion_criteria": [
                    "Strategic direction is explicitly approved",
                    "Key alternatives and risks are documented",
                    "Decision owner and next action are clear",
                ],
                "next_recommended_action": "Review the Product Strategy recommendation and provide an explicit decision.",
            }
        raise OrchestratorError(f"No State projection mapping exists for Skill: {skill_name}")

    @staticmethod
    def _discovery_state_changes(
        state: dict[str, Any],
        output: dict[str, Any],
    ) -> dict[str, Any]:
        completed = list(state.get("completed_outputs") or [])
        if "Discovery Output" not in completed:
            completed.append("Discovery Output")
        validation = list(output["validation_required"])
        existing = list(state.get("knowledge_items") or [])
        by_question = {item.get("question"): item for item in existing if isinstance(item, dict)}
        knowledge_items = []
        for index, question_data in enumerate(output.get("open_questions") or [], start=1):
            question = question_data.get("question") if isinstance(question_data, dict) else str(question_data)
            if not question:
                continue
            previous = by_question.get(question) or {}
            knowledge_items.append({
                "id": previous.get("id", f"discovery-question-{index}"),
                "question": question,
                "answer": previous.get("answer", ""),
                "status": previous.get("status", "open"),
                "updated_at": previous.get("updated_at"),
            })
        return {
            "completed_outputs": completed,
            "missing_items": validation or ["None identified"],
            "required_user_action": output["recommended_next_action"],
            "expected_output": [
                "Discovery Summary",
                "Confirmed Findings",
                "Assumptions",
                "Decisions",
                "User Needs",
                "Initial Scope",
                "Open Questions",
                "Risks",
                "Validation Required",
            ],
            "completion_criteria": state.get("completion_criteria") or [
                "Problem and users are understood",
                "Key findings and assumptions are documented",
                "Initial scope boundaries exist",
                "Required validation is identified",
            ],
            "next_recommended_action": output["recommended_next_action"],
            "knowledge_items": knowledge_items,
        }

    def _discovery_failure(
        self,
        project_id: str | None,
        reason: str,
        *,
        state: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        phase = state["phase"] if state else None
        return {
            "result_type": "Orchestration Result",
            "project_id": project_id,
            "current_phase": phase,
            "status": "BLOCKED",
            "state_loaded": state is not None,
            "discovery_status": "FAILED",
            "active_skill": None,
            "discovery_output": None,
            "phase_guidance": self._blocked_guidance(reason),
            "state_update_proposal": None,
            "state_committed": False,
            "execution_allowed": False,
            "error": reason,
        }

    def _capability_failure(
        self,
        project_id: str | None,
        reason: str,
        *,
        state: dict[str, Any] | None = None,
        active_skill: str | None = None,
    ) -> dict[str, Any]:
        phase = state["phase"] if state else None
        return {
            "result_type": "Orchestration Result",
            "project_id": project_id,
            "current_phase": phase,
            "status": "BLOCKED",
            "state_loaded": state is not None,
            "active_skill": active_skill,
            "discovery_status": "NOT_APPLICABLE" if phase != "Discovery" else "FAILED",
            "discovery_output": None,
            "phase_guidance": self._blocked_guidance(reason),
            "state_update_proposal": None,
            "state_committed": False,
            "execution_allowed": False,
            "error": reason,
        }

    def _orchestration_result(
        self,
        *,
        project_id: str,
        state: dict[str, Any],
        action: str,
    ) -> dict[str, Any]:
        phase = state["phase"]
        status = state["status"]
        guidance = self._phase_guidance(phase, state, action)
        return {
            "project_id": project_id,
            "current_phase": phase,
            "status": status,
            "state_version": state["version"],
            "phase_guidance": guidance,
            "execution_allowed": False,
            "discovery_executed": False,
            "active_capability": "Discovery Skill" if phase == "Discovery" else None,
        }

    @staticmethod
    def _phase_guidance(
        phase: str,
        state: dict[str, Any],
        action: str,
    ) -> dict[str, Any]:
        """Produce the mandatory guidance shape without mutating State."""

        completed = state["completed_outputs"] or ["Project Instance initialized"]
        missing = state["missing_items"]
        if phase == "Discovery" and not missing:
            missing = [
                "Problem and user need",
                "Initial goals and scope boundaries",
                "Assumptions, open questions, and initial risks",
            ]

        if phase == "Discovery":
            required_action = state["required_user_action"] or (
                "Provide the initial project context: problem, users, desired outcome, "
                "known constraints, and existing materials."
            )
            expected_output = state["expected_output"] or [
                "Discovery Summary",
                "Confirmed Findings",
                "Assumptions",
                "Open Questions",
                "Initial Risks",
                "Updated Project Brief",
            ]
            completion_criteria = state["completion_criteria"] or [
                "Problem and users are understood",
                "Key findings and assumptions are documented",
                "Initial scope boundaries exist",
                "Required validation is identified",
            ]
            next_action = state["next_recommended_action"] or (
                "Complete the Discovery intake so the Discovery Skill can analyze it."
            )
        else:
            required_action = state["required_user_action"] or action
            expected_output = state["expected_output"] or [
                f"Validated outputs for {phase}"
            ]
            completion_criteria = state["completion_criteria"] or [
                f"Required outputs for {phase} are validated"
            ]
            next_action = state["next_recommended_action"] or action

        return {
            "phase_status": {"current_phase": phase, "status": state["status"]},
            "completed": completed,
            "missing": missing or ["None identified"],
            "required_user_action": required_action,
            "expected_output": expected_output,
            "completion_criteria": completion_criteria,
            "next_recommended_action": next_action,
        }

    @staticmethod
    def _transition_proposal(state: dict[str, Any]) -> dict[str, Any] | None:
        if state["status"] != "completed" and state["phase"] != "Completed":
            return None
        next_phase = {
            "Discovery": "Strategy",
            "Strategy": "Planning",
            "Planning": "Design",
            "Design": "Execution",
            "Execution": "Validation",
            "Validation": "Launch",
            "Launch": "Learning",
            "Learning": "Completed",
        }.get(state["phase"])
        if not next_phase:
            return None
        return {
            "type": "PHASE_TRANSITION_PROPOSAL",
            "from_phase": state["phase"],
            "to_phase": next_phase,
            "requires_approval": True,
            "automatic_transition": False,
            "reason": "Current phase is marked completed.",
        }

    @staticmethod
    def _blocked_guidance(reason: str) -> dict[str, Any]:
        return {
            "phase_status": {"current_phase": None, "status": "blocked"},
            "completed": ["None identified"],
            "missing": [reason],
            "required_user_action": "Resolve the blocking state issue before continuing.",
            "expected_output": ["Validated Project State and aligned Registry metadata"],
            "completion_criteria": ["Project State can be loaded and validated safely"],
            "next_recommended_action": "Review the State and Registry records, then retry orchestration.",
        }
