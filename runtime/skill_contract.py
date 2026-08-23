"""Generic Skill Definition loading and compliance validation."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class SkillContractError(Exception):
    """A Skill Definition is missing or violates the generic contract."""


@dataclass(frozen=True)
class SkillContract:
    name: str
    version: str
    purpose: str
    required_inputs: tuple[str, ...]
    execution_rules: dict[str, Any]
    required_outputs: tuple[str, ...]
    validation_rules: dict[str, Any]
    definition_path: Path

    def validate_input(self, context: Any) -> None:
        if not isinstance(context, dict):
            raise SkillContractError("Skill input must be an object")
        missing = [
            field for field in self.required_inputs
            if field not in context or context[field] is None
        ]
        if missing:
            raise SkillContractError(f"Missing required Skill input: {', '.join(missing)}")

    def validate_output(self, output: Any) -> None:
        if not isinstance(output, dict):
            raise SkillContractError("Skill output must be an object")
        missing = [field for field in self.required_outputs if field not in output]
        if missing:
            raise SkillContractError(f"Missing required Skill output: {', '.join(missing)}")

        list_fields = self.validation_rules.get("list_fields", [])
        for field in list_fields:
            if not isinstance(output.get(field), list):
                raise SkillContractError(f"Skill output field must be a list: {field}")

        if self.validation_rules.get("decisions_require_explicit_approval"):
            for decision in output.get("decisions", []):
                if not isinstance(decision, dict) or decision.get("approved") is not True:
                    raise SkillContractError("Every Discovery decision must be explicitly approved")

        if self.validation_rules.get("open_questions_require_fields"):
            required = set(self.validation_rules["open_questions_require_fields"])
            for question in output.get("open_questions", []):
                if not isinstance(question, dict) or not required.issubset(question):
                    raise SkillContractError("Open Questions must include question, why_it_matters, and required_validation")

        if "initial_scope" in self.required_outputs or self.validation_rules.get("initial_scope_required"):
            scope = output.get("initial_scope")
            if not isinstance(scope, dict) or not isinstance(scope.get("in_scope"), list) or not isinstance(scope.get("out_of_scope"), list):
                raise SkillContractError("initial_scope must contain in_scope and out_of_scope lists")


class SkillDefinitionLoader:
    """Load the machine-readable contract embedded in a Skill Definition."""

    MARKER = re.compile(r"```skill-contract\s*\n(.*?)\n```", re.DOTALL)

    def load(self, definition_path: str | Path) -> SkillContract:
        path = Path(definition_path)
        if not path.is_file():
            raise SkillContractError(f"Skill Definition not found: {path}")
        text = path.read_text(encoding="utf-8")
        match = self.MARKER.search(text)
        if not match:
            raise SkillContractError(f"Skill Definition has no skill-contract block: {path}")
        try:
            raw = json.loads(match.group(1))
        except json.JSONDecodeError as exc:
            raise SkillContractError(f"Invalid Skill contract JSON: {path}") from exc

        required = {"identity", "inputs", "execution_rules", "outputs", "validation_rules"}
        missing = required - set(raw)
        if missing:
            raise SkillContractError(f"Skill contract is missing: {sorted(missing)}")
        identity = raw["identity"]
        for field in ("name", "version", "purpose"):
            if not isinstance(identity.get(field), str) or not identity[field].strip():
                raise SkillContractError(f"Skill identity field is required: {field}")
        required_inputs = raw["inputs"].get("required", [])
        required_outputs = raw["outputs"].get("required", [])
        if not isinstance(required_inputs, list) or not isinstance(required_outputs, list):
            raise SkillContractError("Skill inputs.required and outputs.required must be lists")
        return SkillContract(
            name=identity["name"],
            version=identity["version"],
            purpose=identity["purpose"],
            required_inputs=tuple(required_inputs),
            execution_rules=raw["execution_rules"],
            required_outputs=tuple(required_outputs),
            validation_rules=raw["validation_rules"],
            definition_path=path,
        )
