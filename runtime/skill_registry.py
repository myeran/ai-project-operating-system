"""Minimal runtime Skill Registry lookup."""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    from .discovery_skill import DiscoverySkill
    from .documentation_skill import DocumentationSkill
    from .engineering_skill import EngineeringSkill
    from .launch_skill import LaunchSkill
    from .project_planning_skill import ProjectPlanningSkill
    from .product_strategy_skill import ProductStrategySkill
    from .review_skill import ReviewSkill
    from .ux_ui_skill import UXUISkill
    from .project_navigator_skill import ProjectNavigatorSkill
except ImportError:  # Supports direct test-module execution.
    from discovery_skill import DiscoverySkill
    from documentation_skill import DocumentationSkill
    from engineering_skill import EngineeringSkill
    from launch_skill import LaunchSkill
    from project_planning_skill import ProjectPlanningSkill
    from product_strategy_skill import ProductStrategySkill
    from review_skill import ReviewSkill
    from ux_ui_skill import UXUISkill
    from project_navigator_skill import ProjectNavigatorSkill


class SkillRegistryError(Exception):
    """A requested Skill is not available."""


class SkillRegistry:
    """Resolve approved Skill definitions without creating new Skills."""

    def __init__(self, skills: dict[str, Any] | None = None) -> None:
        default_path = Path(__file__).parents[1] / "03_Skill_Registry" / "Skills" / "Discovery Skill.md"
        self._skills = skills if skills is not None else {
            "Discovery Skill": DiscoverySkill(default_path),
            "Documentation Skill": DocumentationSkill(),
            "Engineering Skill": EngineeringSkill(),
            "Launch Skill": LaunchSkill(),
            "Product Strategy Skill": ProductStrategySkill(),
            "Project Planning Skill": ProjectPlanningSkill(),
            "Review Skill": ReviewSkill(),
            "UX/UI Skill": UXUISkill(),
            "project_navigator_skill": ProjectNavigatorSkill(),
        }

    def resolve(self, skill_name: str) -> Any:
        skill = self._skills.get(skill_name)
        if skill is None:
            raise SkillRegistryError(f"Skill unavailable: {skill_name}")
        return skill
