"""State-aware conversation routing and user-facing Hebrew presentation.

This module owns only volatile chat context and presentation. Project state and
business decisions remain behind the MCP/Runtime boundary.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ConversationIntent(str, Enum):
    START_PROJECT = "start_project"
    PROJECT_STATUS = "project_status"
    CONTINUE_PROJECT = "continue_project"
    NEEDS_START = "needs_start"
    PROJECT_NAVIGATOR = "project_navigator"


@dataclass
class ConversationState:
    active_project_id: str | None = None
    active_project_name: str | None = None
    question_index: int = 0
    discovery_questions: list[dict[str, Any]] = field(default_factory=list)

    @property
    def has_active_project(self) -> bool:
        return bool(self.active_project_id or self.active_project_name)


class ConversationIntentHandler:
    """Classify using conversation state first and only narrow explicit cues."""

    _START = re.compile(r"(?:פרויקט\s+חדש|להתחיל\s+פרויקט|התחל\s+פרויקט|new\s+project|start\s+project)", re.I)
    _STATUS = re.compile(r"(?:סטטוס|מצב\s+הפרויקט|מה\s+מצב|status|state)", re.I)
    _PROJECT_PROPOSAL = re.compile(
        r"(?:אני\s+רוצה\s+(?:לבנות|ליצור|להקים|לפתח)|(?:לבנות|ליצור|להקים|לפתח)\s+(?:מערכת|אפליקציה|שירות|כלי|פרויקט)|יש\s+לי\s+רעיון)",
        re.I,
    )
    _NAVIGATOR = re.compile(r"^\s*(?:project[ _-]?navigator(?:[ _-]?skill)?|navigator|מפת\s+הפרויקט)\s*$", re.I)

    def classify(self, text: str, state: ConversationState) -> ConversationIntent:
        if self._NAVIGATOR.search(text):
            return ConversationIntent.PROJECT_NAVIGATOR
        if self._START.search(text):
            return ConversationIntent.START_PROJECT
        if self._STATUS.search(text):
            return ConversationIntent.PROJECT_STATUS if state.has_active_project else ConversationIntent.NEEDS_START
        if state.has_active_project:
            return ConversationIntent.CONTINUE_PROJECT
        if self._PROJECT_PROPOSAL.search(text):
            return ConversationIntent.START_PROJECT
        return ConversationIntent.NEEDS_START

    @staticmethod
    def is_help_request(text: str) -> bool:
        normalized = re.sub(r"[?!.,؛,:]", " ", text.lower())
        cues = (
            "מה לעשות",
            "מה השלב הבא",
            "מה אתה צריך ממני",
            "לא הבנתי",
            "אפשר להסביר",
            "למה זה חשוב",
        )
        return any(cue in normalized for cue in cues)


class ResponsePresentation:
    """Convert Runtime guidance into short, natural Hebrew chat responses."""

    _PHASES = {"Discovery": "הבנת הצורך", "Strategy": "גיבוש הכיוון", "Planning": "תכנון", "Execution": "ביצוע"}
    _STATUSES = {"proposed": "בהגדרה", "active": "בתהליך", "completed": "הושלם", "blocked": "ממתין לטיפול"}
    _QUESTIONS = {
        "What problem are we trying to solve?": "איזו בעיה אנחנו מנסים לפתור?",
        "Who experiences this problem first?": "מי נתקל בבעיה הזו קודם?",
        "How is the problem solved today?": "איך פותרים את הבעיה כיום?",
        "What is frustrating or insufficient about the current approach?": "מה מתסכל או לא מספיק בגישה הנוכחית?",
        "What would count as evidence that the problem was solved?": "מה ייחשב הוכחה שהבעיה נפתרה?",
    }

    def present(
        self,
        intent: ConversationIntent,
        payload: dict[str, Any],
        state: ConversationState,
        user_text: str = "",
    ) -> str:
        if payload.get("error_type"):
            return self._error(payload)

        self._remember_questions(payload, state)
        if intent == ConversationIntent.START_PROJECT:
            return self._start_response(state)
        if intent == ConversationIntent.PROJECT_STATUS:
            return self._status_response(payload)
        if intent == ConversationIntent.PROJECT_NAVIGATOR:
            return self._navigator_response(payload)
        if intent == ConversationIntent.NEEDS_START:
            return "בשמחה. כדי להתחיל, כתוב לי מה אתה רוצה לבנות או להשיג."

        question = self._current_question(state)
        if ConversationIntentHandler.is_help_request(user_text):
            return f"בטח. כדי להתקדם אני צריך להבין: {question}"
        state.question_index += 1
        next_question = self._current_question(state)
        return f"הבנתי, תודה. השלב הבא: {next_question}"

    def _start_response(self, state: ConversationState) -> str:
        return f"בשמחה. נתחיל בהבנת הפרויקט. {self._current_question(state)}"

    def _status_response(self, payload: dict[str, Any]) -> str:
        phase = self._PHASES.get(str(payload.get("current_phase")), "השלב הנוכחי")
        status = self._STATUSES.get(str(payload.get("status")).lower(), "בתהליך")
        action = self._translate_action(payload.get("next_recommended_action"))
        return f"הפרויקט נמצא כרגע בשלב {phase} והוא {status}. {action}"

    @staticmethod
    def _navigator_response(payload: dict[str, Any]) -> str:
        current = payload.get("current_phase") or "לא ידוע"
        lines = [f"מפת הפרויקט — השלב הנוכחי: {current}", ""]
        for step in payload.get("steps") or []:
            status = {"current": "נוכחי", "completed": "הושלם", "pending": "ממתין"}.get(step.get("status"), step.get("status", ""))
            skill = step.get("responsible_skill") or "אין Skill רשום"
            lines.append(f"- {step.get('phase')}: {status} — {skill}")
        missing = payload.get("missing") or []
        if missing:
            lines.extend(["", "חסר בשלב הנוכחי:", *[f"- {item}" for item in missing]])
        lines.extend(["", f"הפעולה הבאה: {payload.get('next_action') or 'לא נקבעה'}"])
        return "\n".join(lines)

    @staticmethod
    def _remember_questions(payload: dict[str, Any], state: ConversationState) -> None:
        output = payload.get("discovery_output") or {}
        questions = output.get("open_questions") if isinstance(output, dict) else None
        if isinstance(questions, list):
            normalized = [q for q in questions if isinstance(q, dict) and isinstance(q.get("question"), str)]
            if normalized:
                if normalized != state.discovery_questions:
                    state.discovery_questions = normalized
                    state.question_index = 0

    @staticmethod
    def _current_question(state: ConversationState) -> str:
        if state.discovery_questions:
            index = min(state.question_index, len(state.discovery_questions) - 1)
            question = state.discovery_questions[index]["question"]
            return ResponsePresentation._QUESTIONS.get(question, question)
        return "מה הבעיה או הצורך המרכזי שאתה רוצה לפתור?"

    @staticmethod
    def _translate_action(action: Any) -> str:
        text = str(action or "").strip()
        translations = {
            "Answer the Discovery questions and provide evidence before defining product direction.": "כדאי לענות על שאלות ההיכרות כדי שנוכל להגדיר כיוון ברור.",
            "Continue the current phase using the required user action.": "אפשר להמשיך עם המידע הבא שנדרש.",
        }
        return translations.get(text, "אפשר להמשיך עם המידע הבא שנדרש.")

    @staticmethod
    def _error(payload: dict[str, Any]) -> str:
        error_type = payload.get("error_type")
        if error_type in {"RUNTIME_UNAVAILABLE", "RUNTIME_FAILURE"}:
            return "כרגע לא הצלחתי להתחבר למערכת. נסה שוב בעוד רגע."
        if error_type == "PROJECT_NOT_FOUND":
            return "לא מצאתי את הפרויקט הפעיל. אפשר להתחיל פרויקט חדש ונמשיך משם."
        return "לא הצלחתי להשלים את הפעולה. נסה לנסח שוב במילים שלך."

    @classmethod
    def present_error(cls, payload: dict[str, Any]) -> str:
        return cls._error(payload)
