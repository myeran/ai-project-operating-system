# Local Knowledge Management Decision

**Status:** Implemented
**Scope:** Local UI knowledge summary, answer editing, checkpoint, and resume

## Decision

Project questions and answers are canonical knowledge items under
`Project State.canonical_state.knowledge.items`. Each item has a stable `id`,
`question`, `answer`, `status` (`open`, `approved`, or `needs_update`), and
`updated_at`.

The Runtime API owns validation and persistence. MCP exposes the capability to
the Local UI. The browser never reads SQLite and contains presentation-only
logic. Updates use the existing State Adapter proposal, approval, optimistic
version check, commit, and audit path.

## Invariants

- An update targets an existing item ID; it cannot create a duplicate question.
- Unknown item IDs, invalid statuses, malformed items, and stale versions fail
  closed.
- “Save and exit” persists a checkpoint through MCP and Runtime, not browser
  storage.
- The existing Orchestrator and Skills remain the owners of lifecycle and
  domain decisions; the knowledge feature only edits the user-owned answer
  projection.

## Boundary

```text
User → Local UI → MCP → Runtime API → State Adapter → SQLite
```

The MCP additions are `project_knowledge_summary`, `update_knowledge_item`,
and `save_project_checkpoint`. Existing lifecycle tools and proposal flows are
retained.
