# Architecture Documentation Index

**System:** AI Project Operating System  
**Source of Truth:** `00_Architecture/ACTIVE/` for active architecture references; `00_Architecture/ARCHIVE/` for historical material.  
**Owner:** System Owner  
**Status:** Canonicalization in progress — no architectural decisions changed.

## Active Architecture Sources of Truth

| Document | Purpose | Status |
|---|---|---|
| `ACTIVE/architecture-blueprint.md` | Architecture overview and layer boundaries | Completed |
| `ACTIVE/system-contracts-and-state-model.md` | Canonical contracts, state, ownership, transitions | Completed — Approved |
| `ACTIVE/project-instance-architecture-decisions-record.md` | Approved Project Instance decisions | Approved |
| `ACTIVE/project-instance-bootstrap-package.md` | Required bootstrap package and initialization rules | Active reference |
| `ACTIVE/runtime-control-plane-architecture-decision.md` | Runtime authority and control-plane boundary | Proposed for approval |
| `ACTIVE/runtime-contract.md` | Canonical Runtime request, response, storage, execution, and failure contract | Proposed for approval |
| `ACTIVE/registry-adapter-contract.md` | Registry Adapter operations and authority contract | Proposed for approval |
| `ACTIVE/minimal-runtime-slice-implementation-plan.md` | Build order, tests, scope, and MVP success criteria | Proposed for approval |
| `ACTIVE/decision-log.md` | Approved architectural decisions and rationale | Active source |
| `ACTIVE/roadmap.md` | Official construction roadmap | Active source |
| `ACTIVE/development-workflow.md` | Rules for building and evolving the system | In Progress |
| `ACTIVE/phase-review-gate-framework.md` | Review and quality mechanism | Draft for approval |

## Archived Documents

Archived documents preserve the reasoning and historical path that led to the
active architecture. They are not active sources of truth and must not be used
for new implementation decisions when an ACTIVE document covers the topic.

### `ARCHIVE/superseded-decisions/`

- `project-instance-architecture-decision.md` — superseded by the approved decisions record.
- `runtime-contract-decision.md` — consolidated into `ACTIVE/runtime-contract.md`.
- `runtime-request-response-storage-boundary-decision.md` — consolidated into `ACTIVE/runtime-contract.md`.
- `runtime-host-and-storage-boundary-decision.md` — consolidated into `ACTIVE/runtime-contract.md`.

### `ARCHIVE/previous-plans/`

- `runtime-mvp-prototype-plan.md` — superseded by `ACTIVE/minimal-runtime-slice-implementation-plan.md`.

### `ARCHIVE/exploration/`

Reserved for future exploratory material that does not represent active authority.

## Canonicalization Rules

- One active source of truth exists per topic.
- Archived documents retain historical value but have no implementation authority.
- Project State remains canonical only in `system-contracts-and-state-model.md`.
- Runtime behavior is governed by `runtime-contract.md`.
- MVP implementation sequencing is governed by `minimal-runtime-slice-implementation-plan.md`.
- No file is deleted as part of this migration.
