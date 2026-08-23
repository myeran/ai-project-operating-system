# Local Chat Conversation Layer Decision

## Scope

This decision covers the Local Chat presentation and conversation boundary. It
does not create a second Runtime, state store, Orchestrator, or Skill.

## Ownership

- Runtime API remains the canonical owner of Project State, lifecycle, phase,
  and business guidance.
- MCP remains the only transport from Local Chat to Runtime API.
- Local Chat owns only volatile conversation context: active project reference,
  current presentation question, and optional debug preference.
- Local Chat may classify explicit user intent for routing and presentation; it
  must not make lifecycle or business decisions.

## Flow

`User → Conversation/Intent Handler → MCP → Runtime API → Runtime`

The free-form user message is forwarded as `message` together with the hidden
`project_id` for `continue_project`. Runtime remains responsible for accepting,
validating, and interpreting project input.

## Invariants

- No direct SQLite access from Local Chat.
- No tool name, project ID, raw payload, or internal status is shown by default.
- Without an active project, a non-start message fails closed with a helpful
  invitation to start one.
- Explicit status requests route to `project_status`; other project-related
  messages with an active project route to `continue_project`.
- Debug output is opt-in and never enabled by default.
- If Runtime returns malformed guidance, Local Chat shows a safe Hebrew fallback
  and does not invent project state.

## Migration disposition

| Existing mechanism | Decision | Result |
| --- | --- | --- |
| Keyword-only `_intent` | REPLACE | State-aware intent handler with explicit intents plus safe active-project fallback |
| Raw `format_payload` output | REPLACE | Hebrew response presentation layer |
| `active_project_id` in client response | KEEP internally / HIDE externally | Used only for subsequent MCP calls |
| Runtime and MCP boundaries | KEEP | Extend `continue_project` with optional free-form `message` |

## Validation

Unit tests cover state-aware routing, free-form forwarding, Hebrew
presentation, debug opt-in, and the requested multi-turn flow. Existing Runtime
and MCP regression tests remain required.
