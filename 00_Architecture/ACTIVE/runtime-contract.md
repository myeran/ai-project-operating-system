# Runtime Contract

**System:** AI Project Operating System  
**Status:** Canonical Runtime Contract — Proposed for Approval  
**Scope:** Runtime Control Plane boundaries for the Minimal Runtime Slice  
**Canonical State:** `system-contracts-and-state-model.md`  
**Related Architecture:** `runtime-control-plane-architecture-decision.md`

## 1. Purpose

This document is the single active contract for communication, authority,
state access, execution control, and user-facing responses in the Runtime
Control Plane. It consolidates the earlier Runtime contract, request/response
boundary, and host/storage boundary decisions without changing their approved
architectural direction.

It defines contracts, not code, database technology, deployment, or automation.

## 2. Runtime Responsibilities

```text
User / Client
      ↓
Runtime Entry Gateway
      ↓
Project Resolver
      ↓
State Adapter
      ↓
Project Orchestrator Agent
      ↓
Skills / Workers
      ↓
State Proposal and Commit
      ↓
Response Renderer
      ↓
User
```

### Runtime Entry Gateway

- Receives every project-related request.
- Validates the request envelope.
- Performs initial intent classification only.
- Does not load Project State, activate Skills, or make the final project decision.

### Project Resolver

- Resolves a Project Instance by stable ID or Registry lookup.
- Classifies results as found, not found, duplicate, or ambiguous.
- Does not create or update Project State.

### State Adapter

- Loads the canonical Project State.
- Exposes read snapshots to the Orchestrator.
- Validates version, actor, timestamp, and audit context for commits.
- Does not decide lifecycle transitions.

### Project Orchestrator Agent

- Makes the final project-action and lifecycle decision.
- Chooses whether to ask, activate a Skill/Worker, escalate, or transition.
- Validates structured outputs before proposing state changes.
- Owns phase control and user-facing guidance orchestration.

### Skills and Workers

- Execute bounded analysis or assigned work.
- Receive relevant context only.
- Return structured findings, recommendations, risks, artifacts, and handoff requests.
- Do not change canonical state, approve strategic decisions, or generate phase guidance directly.

### Response Renderer

- Is the only component that renders user-facing phase guidance.
- Validates the complete Runtime Response Contract before returning a response.
- May render clarification, escalation, confirmation, or fail-closed responses.

## 3. Request Contract

```yaml
runtime_request:
  request_id: <unique request id>
  correlation_id: <conversation or workflow id>
  user_id: <user identity or approved anonymous reference>
  project_id: <optional stable project id>
  project_name: <optional project name>
  intent: <initial or final intent classification>
  request_type: <canonical request type>
  user_request: <original request>
  workspace_context: <optional client/workspace reference>
  timestamp: <Gateway timestamp>
  source_client: <client identity>
```

### Required Fields

`request_id`, `correlation_id`, `user_id`, `user_request`, `timestamp`, and
`source_client` are required. A project-related request requires `project_id`
or `project_name` after resolution; `START_PROJECT` requires a project name or
an explicit clarification step.

### Validation Rules

- Request IDs are unique and are not reused.
- Gateway timestamp is authoritative for receipt time.
- A supplied Project ID must resolve through the Registry.
- Ambiguous intent or project identity cannot trigger irreversible action.
- User-provided state fields are proposals, not canonical facts.

## 4. Routing and Handoff Contract

| Request | Required route |
|---|---|
| `START_PROJECT` | Gateway → Resolver → Bootstrap → State Initialization → Orchestrator → Discovery |
| `CONTINUE_PROJECT` | Gateway → Resolver → State Load → Orchestrator → Lifecycle Guidance |
| `STATUS` | Gateway → Resolver → State Read → Response Renderer |
| `VALIDATION_REQUEST` | Gateway → Resolver → Orchestrator → Validation Guidance |
| `EXECUTION_REQUEST` | Gateway → Resolver → State Load → Execution Gate → Skill/Worker |
| `AMBIGUOUS` | Gateway → Clarification; no project action |

The Gateway performs initial classification. The Orchestrator owns the final
action decision. No Skill, Worker, or chat context may bypass this route.

## 5. Response Contract

```yaml
runtime_response:
  request_id: <request id>
  correlation_id: <correlation id>
  project_id: <resolved project id or null>
  current_phase: <phase or null>
  status: <canonical status or response status>
  completed: []
  missing: []
  required_user_action: <one clear action or None identified>
  expected_output: []
  completion_criteria: []
  next_recommended_action: <next action>
  response_type: guidance | clarification | escalation | confirmation | error
```

For an incomplete phase, all of these sections are mandatory:

- Phase Status: Current Phase and Status.
- Completed: validated outputs and achievements.
- Missing: information, decisions, artifacts, or validations.
- Required User Action: exactly one specific action.
- Expected Output: what the action will produce or update.
- Completion Criteria: what must be true to close the phase.
- Next Recommended Action: what follows after the current action.

Empty sections must state `None identified`. A file link, task-only response, or
short status update is invalid when user action is required.

## 6. Storage Boundary

### Project Registry

The Registry is the canonical index of Project Instances. It stores identity and
resolution metadata, including Project ID, name, owner, status, current phase,
OS version reference, workspace location, created date, last activity, version,
and audit metadata.

The Registry does not contain the full Project State or Project Knowledge.

### Project State

Project State remains the single canonical state model defined in
`system-contracts-and-state-model.md`. The State Adapter owns loading and
technical commit of validated proposals. The Orchestrator owns workflow and
phase decisions; Skills and Workers may only propose bounded updates.

### Audit

At minimum record project creation, resolution, state changes, phase transitions,
decisions, approvals, bootstrap completion, discovery activation, responses, and
fail-closed outcomes. Each event includes request/correlation IDs, Project ID,
actor, timestamp, version, result, and source task or decision where applicable.

### Host and Client Boundary

The initial model is Hybrid: a Local Runtime is the control host; ChatGPT and
Codex are clients/workspaces; a Project Instance is an independent logical
entity. A client without the Gateway is not a supported Runtime path.

## 7. State Proposal and Commit Rules

Every state or Registry mutation requires:

```yaml
commit_context:
  proposal_id: <proposal id>
  project_id: <project id>
  expected_version: <version read>
  actor: <authorized actor>
  timestamp: <commit timestamp>
  source_task_id: <task id>
  source_decision_id: <optional decision id>
  audit_record_id: <audit id>
```

- Compare-and-commit is required; stale writes fail.
- Registry and Project State must not silently disagree.
- Commit authority is technical persistence authority, not strategic decision authority.
- No commit is reported successful before its audit record is accepted.
- Unknown, malformed, contradictory, or unauthorized state fails closed.

## 8. Execution Gate

| Action Type | Required phase | Approval | Risk |
|---|---|---|---|
| `READ_STATE` | Any resolved phase | None | Low |
| `START_PROJECT` | Entry / Discovery | None for initialization | Low |
| `RUN_DISCOVERY` | Discovery | None unless strategic decision is required | Low/Medium |
| `RUN_ANALYSIS` | Active relevant phase | None | Low/Medium |
| `CREATE_ARTIFACT` | Active relevant phase | Per artifact risk | Low/Medium |
| `EXECUTE_CODE` | Execution | Planning/Execution readiness and required approval | High |
| `CHANGE_SCOPE` | Strategy/Planning | Human Owner approval | High |
| `TRANSITION_PHASE` | Transition boundary | Orchestrator plus required human approval | Medium/High |
| `COMMIT_STATE` | Any valid state operation | Authorized Orchestrator proposal | Medium |

Actions that can materially change scope, money, legal position, external
systems, or create irreversible effects require an Execution Gate and escalation.
Coding or external execution before the required lifecycle conditions is blocked.

## 9. Failure Handling

- **Registry unavailable:** fail closed; no resolution-dependent action or creation claim.
- **Project not found:** return structured not-found; Resolver decides whether Bootstrap is valid.
- **Duplicate or ambiguous project:** stop automatic creation and request user choice.
- **State unavailable or invalid:** do not execute or overwrite; escalate reconciliation.
- **Version mismatch:** reject commit, reload, and re-evaluate through the Orchestrator.
- **Runtime unavailable:** report inability to perform a controlled action; do not simulate success.
- **Missing capability:** report the gap and keep the project blocked or awaiting approval.
- **Response contract failure:** regenerate through Response Renderer; never return a shortened phase response.

## 10. Minimal Runtime Slice

### Included

- Runtime Entry Gateway.
- Project Resolver and Registry access.
- Project Instance Bootstrap.
- Canonical State initialization and loading.
- Project Orchestrator Agent interface.
- Discovery activation boundary.
- Full Phase Guidance Response Renderer.
- Basic audit and fail-closed tests.

### Excluded

- Production code execution.
- Full UI.
- Cloud deployment.
- Multi-user permissions.
- Advanced integrations.
- Agent teams and parallel Workers.
- Cross-project knowledge sharing.
- Automatic OS migration.

## 11. Approval Criteria

The contract is ready for implementation when:

- Runtime has one control authority and one supported entry route.
- Project State remains the only canonical state model.
- Registry, State, and Audit boundaries are distinct.
- Request and Response contracts are complete.
- Execution Gate and fail-closed behavior are testable.
- Skills and Workers cannot bypass the Orchestrator or Response Renderer.
- The Minimal Runtime Slice is bounded and does not authorize production execution.
