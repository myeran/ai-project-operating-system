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
3. For status or continuation, if the Runtime is unavailable, explain that the project is not connected; do not claim the Navigator ran. For a new project, follow the Codex fast path below to locate the shared Runtime first.
4. If the user asks to start a new project, collect the required context: project name, type, goal, expected outcome, current stage, and the chosen local Mac folder. Follow the new-project workspace setup below, then use the Runtime's project-start flow.
5. If the user asks to continue, resolve the named project before reading or reporting its state. If the project is ambiguous, ask the user to choose; do not guess.

## Codex fast path

When the user writes a natural-language request such as `אני רוצה להתחיל פרויקט חדש`,
do not require `$project-navigator` or the browser Local Chat first. From any project
folder, locate or register the shared Runtime and start it if it is unavailable:

The first user-visible response must be exactly:

```text
שלום ובהצלחה בפרוייקט
```

Only after this greeting, perform the Runtime connection internally and then ask for
the project name. Do not put the Runtime status or the project-name question before
the greeting.

```bash
runtime_root="$(python3 ~/.codex/skills/project-navigator/runtime_bridge.py start --workspace "$PWD")"
```

The bridge is idempotent, keeps the conversation in Codex, and records the shared
Runtime location in `~/.codex/project-navigator/runtime.json`. Then collect only the
missing project context, one question at a time. For `--workspace-location`, use
the canonical absolute path chosen for this new project's local folder, never `$PWD`
unless it is that folder. Do not create parallel project state or invent missing answers.

## New-project workspace setup

For each new project, use this default arrangement: one ordinary ChatGPT Project;
Chat in that Project for planning, discussion, and approved decisions; one persistent
Work chat in the same Project for execution; and one real Mac local folder as the
source of truth for project files. The Runtime remains the authority for lifecycle
state, phase transitions, and Skills. `~/.codex/.chatgpt-projects/` is an internal
mirror, never the new project's root or `--workspace-location`.

1. Ask the user to choose an existing local folder or accept a proposed folder
   outside the internal mirror. Resolve it to an absolute canonical path and create
   it if needed. Check the resolved path is still outside the internal mirror.
   Keep the approved minimal project structure and governance.
2. Create the ordinary ChatGPT Project (or reuse it if this same setup already
   created it). Open a planning Chat there and one Work chat in the same Project.
   Connect that Work to the canonical local folder. Reuse this Work for later
   execution stages; do not open a new Work for each stage.
3. In that connected Work, create a uniquely named temporary text file in the local
   folder, read its contents back, update it, read the update, and remove it. Confirm
   the artifact is gone. If connection or read/write/cleanup fails, report setup as
   incomplete and do not claim the project is ready.
4. Submit the canonical project-start request through
   `$runtime_root/runtime/local_client.py` with that path as `--workspace-location`.
   Read the new project's raw Runtime status (`Project Status: <name>`) and compare
   its `project.location` from the Registry with the canonical path. Resolve any
   mismatch before handoff; the CLI's formatted summary omits this field.
5. At handoff, give the user the Project name, canonical folder path, which Chat is
   for planning, which persistent Work is for execution, the read/write result, and
   the next single lifecycle stage. Continue one stage at a time, preserving the
   existing human approval and Skill boundaries.

If the available app cannot create the Project or connect Work to the folder,
give the user the exact remaining UI action and mark setup incomplete. Do not
submit project-start to the Runtime until the persistent Work connection and its
read/write/cleanup check succeed. Never substitute the internal mirror for the
local folder.

The launcher step is an internal Codex action: run it automatically before asking the
user to provide project details. Do not tell the user to run the command, open the
browser, or perform another setup step when the repository root and launcher are
available.

## Interaction style

Use clear, concise Hebrew by default when the user writes Hebrew. Start with the result, then give the minimum next question or action needed. Guide one decision at a time. Preserve human approval boundaries: Skills recommend and analyze; the user approves strategic decisions, Scope, commitments, and phase transitions.

## Important boundary

This Codex Skill is the conversational entry point. It does not replace or silently mutate the Python Runtime Skill named `project_navigator_skill`; when the Runtime is unavailable, say so plainly and provide the connection step.
