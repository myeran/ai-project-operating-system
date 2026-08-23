---
name: project-navigator
description: Inspect a project lifecycle and guide the user through the next phase when the AI Project Operating System runtime is available.
---

# Project Navigator

Use this skill when the user asks to start a project, continue a project, inspect project progress, find the active phase, or understand what to do next.

## Goal

Guide the user through the project lifecycle:

`Discovery → Strategy → Planning → Design → Execution → Validation → Launch → Learning`

Report each phase and its status, the active phase, the responsible Skill, completed and missing prerequisites, and the next safe action.

## Runtime-first behavior

1. Check the current project for the local AI Project Operating System runtime. Look for a directory named `AI Project Operating System` or files such as `runtime/project_navigator_skill.py`, `runtime/runtime_api.py`, and `runtime/data/runtime.sqlite3`.
2. If the runtime is present, use its canonical state and read-only Navigator path. Do not invent project state and do not modify SQLite, proposals, phase, or files merely to report status.
3. If the runtime is not present in the current project, explain that the Codex Skill is installed but the project is not connected to a local Runtime. Ask the user to clone the repository or connect the project Runtime; do not claim that the Navigator ran.
4. If the user asks to start a new project, collect the required context: project name, type, goal, expected outcome, and current stage. Use the Runtime's project-start flow when it is connected.
5. If the user asks to continue, resolve the named project before reading or reporting its state. If the project is ambiguous, ask the user to choose; do not guess.

## Interaction style

Use clear, concise Hebrew by default when the user writes Hebrew. Start with the result, then give the minimum next question or action needed. Guide one decision at a time. Preserve human approval boundaries: Skills recommend and analyze; the user approves strategic decisions, Scope, commitments, and phase transitions.

## Important boundary

This Codex Skill is the conversational entry point. It does not replace or silently mutate the Python Runtime Skill named `project_navigator_skill`; when the Runtime is unavailable, say so plainly and provide the connection step.
