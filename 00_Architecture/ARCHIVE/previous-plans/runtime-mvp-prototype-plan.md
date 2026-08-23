# Runtime MVP Prototype Plan

**System:** AI Project Operating System  
**Status:** Proposed for Approval  
**Prototype Host:** Local Runtime / Codex Host  
**Storage:** SQLite for Registry, State and Audit; Filesystem for Project Artifacts  
**Scope:** Architecture validation only

## 1. Objective

להוכיח במסלול הקטן ביותר שהמערכת יכולה לבצע:

```text
Start Project
        ↓
Runtime Entry
        ↓
Project Instance Creation / Resolution
        ↓
State Loading
        ↓
Project Orchestrator Agent
        ↓
Discovery
        ↓
Phase Guidance Response
```

ה־Prototype אינו Platform ואינו Production Runtime. מטרתו לאמת Routing, Isolation, State Persistence, Lifecycle Entry ו־Response Contract.

## 2. Scope

### Included

- Runtime Entry Gateway.
- Initial Intent Classification.
- Project Resolver.
- SQLite Project Registry.
- SQLite Project State Adapter.
- Bootstrap Initialization.
- Project Orchestrator Agent Interface.
- Discovery Trigger/Interface.
- Phase Guidance Response Renderer.
- Audit Events בסיסיים.
- End-to-End ו־Failure Tests.

### Excluded

- Full UI.
- Multi-user Support.
- Cloud Deployment.
- Advanced Permissions.
- Full Skill Marketplace.
- Automation Platform.
- Complex Integrations.
- Parallel Workers.
- Production Code Execution.
- Cross-Project Knowledge Sharing.
- Automatic OS Migration.

## 3. Components

### 3.1 Runtime Gateway

**Purpose:** נקודת כניסה יחידה לבקשות פרויקט.  
**Responsibility:** אימות Request, זיהוי Project Intent וניתוב ראשוני.  
**Input:** Runtime Request.  
**Output:** Validated Request ו־Initial Intent.  
**Dependencies:** Runtime Request Contract.

ה־Gateway אינו טוען State, אינו מפעיל Discovery ואינו מבצע Project Work.

### 3.2 Project Resolver

**Purpose:** זיהוי Project Instance קיים או חדש.  
**Responsibility:** חיפוש לפי Project ID/Name וסיווג Match.  
**Input:** Validated Request ו־Registry Query.  
**Output:** Existing / No Match / Duplicate / Ambiguous.  
**Dependencies:** Registry Adapter.

### 3.3 Registry Adapter

**Purpose:** גישה קנונית ל־Project Registry.  
**Responsibility:** Read, Unique Check ו־Create Entry.  
**Input:** Project Query או Registry Entry Proposal.  
**Output:** Registry Result או Commit Result.  
**Dependencies:** SQLite, Version and Audit Rules.

### 3.4 State Adapter

**Purpose:** שמירת וטעינת Canonical Project State.  
**Responsibility:** Read Snapshot, Version Check ו־Commit מאומת.  
**Input:** Project ID או State Update Proposal.  
**Output:** State Snapshot או Commit Result.  
**Dependencies:** SQLite, Canonical State Model, Audit.

### 3.5 Bootstrap Handler

**Purpose:** יצירת Project Instance חדש.  
**Responsibility:** יצירת Project ID, OS Version Binding, Workspace ו־Initial State.  
**Input:** No-Match Resolution ו־Project Name.  
**Output:** Initialized Project Instance ו־Handoff ל־Orchestrator.  
**Dependencies:** Registry Adapter, State Adapter, OS Version Reference, Filesystem.

### 3.6 Project Orchestrator Agent Interface

**Purpose:** חיבור Runtime ל־Project Orchestrator Agent.  
**Responsibility:** קבלת State/Context, זיהוי Discovery והחזרת Lifecycle Decision.  
**Input:** Request, State Snapshot, OS Rules ו־Relevant Context.  
**Output:** Discovery Request, State Proposal ו־Guidance Payload.  
**Dependencies:** Lifecycle Framework, Runtime Contract, Phase Guidance Contract.

### 3.7 Discovery Interface

**Purpose:** הפעלת Discovery במסגרת ה־Control Plane.  
**Responsibility:** העברת Task/Context ל־Discovery Skill או Interface מאושר.  
**Input:** Project Context, Goals ידועים, Users, Constraints ו־Expected Output.  
**Output:** Findings, Assumptions, Open Questions, Risks ו־Recommendations.  
**Dependencies:** Discovery Skill Contract.

ה־Discovery Interface אינו מחזיר Phase Guidance ישירות למשתמש.

### 3.8 Response Renderer

**Purpose:** יצירת התגובה היחידה למשתמש.  
**Responsibility:** הרכבת Full Phase Guidance Output Contract.  
**Input:** Orchestrator Result, Completed, Missing, Validation ו־Criteria.  
**Output:** Runtime Response.  
**Dependencies:** Response Contract.

## 4. Data Model

### 4.1 Project Registry

```yaml
project_registry_entry:
  project_id: <stable unique id>
  project_name: <name>
  owner: <human owner or pending confirmation>
  status: proposed | active | blocked | awaiting_approval | completed | cancelled
  current_phase: Discovery
  os_version: <bound version>
  created_date: <date>
  last_activity: <timestamp>
```

### 4.2 Project State

ה־Prototype משתמש ב־Canonical State Model הקיים. השדות הבאים הם Projection מינימלי הדרוש למסלול, ולא מודל חדש:

```yaml
project_state_projection:
  project_id: <canonical project id>
  phase: <maps to current_status.current_phase>
  status: <maps to current_status.status>
  completed_outputs: <maps to knowledge.outputs/documents>
  missing_items: <derived operational view>
  next_action: <maps to next_actions.tasks>
  version: <maps to audit.version>
  updated_by: <maps to audit.last_updated_by>
  updated_timestamp: <maps to audit.last_updated_at>
```

ה־Projection אינו מחליף את המבנה המלא הכולל Project Identity, Planning, Decisions, Risks, Knowledge, Next Actions ו־Audit.

### 4.3 Audit

ה־Prototype מתעד לפחות:

- `PROJECT_CREATED`.
- `STATE_CHANGED`.
- `PHASE_CHANGED`.
- `DECISION_RECORDED`.
- `PROJECT_RESOLVED`.
- `BOOTSTRAP_COMPLETED`.
- `DISCOVERY_STARTED`.
- `RESPONSE_RENDERED`.
- `FAIL_CLOSED`.

כל אירוע כולל Request ID, Correlation ID, Project ID, Actor, Timestamp, Version ו־Result.

## 5. Runtime Flow

### 5.1 New Project

```text
User Request
        ↓
Runtime Gateway
        ↓
Intent Detection: START_PROJECT
        ↓
Project Resolver
        ↓
No Existing Match
        ↓
Bootstrap Handler
        ↓
Create Registry Entry
        ↓
Initialize Canonical Project State
        ↓
Load State Snapshot
        ↓
Project Orchestrator Agent
        ↓
Discovery Interface
        ↓
State Update Proposal
        ↓
Validation / Commit, אם מותר
        ↓
Response Renderer
        ↓
User
```

### 5.2 Step Contracts and Failure Behavior

| Step | Input | Output | Failure Behavior |
|---|---|---|---|
| Gateway | User Request | Validated Request | Reject invalid request; no Project Action |
| Intent Detection | Request | Initial Intent | Mark ambiguous; ask clarification |
| Resolver | ID/Name | Match result | Stop on duplicate/ambiguous |
| Bootstrap | No Match | Instance + Registry + State | Roll back/mark failed; no Discovery |
| State Load | Project ID | State Snapshot | Fail-Closed; no Execution |
| Orchestrator | State + Context | Discovery Decision | Escalate on invalid State or missing capability |
| Discovery | Task + Context | Structured Output | Return partial/blocked; no Phase Guidance direct |
| Commit | Proposal + Version | New State Version | Reject conflict; reload and re-evaluate |
| Renderer | Validated Result | Full Guidance Response | Reject incomplete response and regenerate |

## 6. Tests

### Test 1 — New Project

**Input:**

```text
Start Project: Personal Habit Tracker
```

**Expected:**

- Gateway activated.
- Intent `START_PROJECT` identified.
- No duplicate found.
- Project Instance created.
- Registry Entry created.
- OS Version bound.
- State initialized with `Discovery` and `proposed`.
- Discovery started through Orchestrator.
- Full Phase Guidance Response returned.

### Test 2 — Existing Project

**Input:**

```text
Continue Project: Personal Habit Tracker
```

**Expected:**

- Existing Instance resolved.
- No new Instance created.
- State loaded.
- Current Phase returned by Orchestrator.
- Full Guidance Response returned.

### Test 3 — Missing Registry

**Input:** Existing Project Request with unavailable Registry.

**Expected:**

- Fail-Closed.
- No creation or Execution.
- Clear error and recovery action.
- Audit `FAIL_CLOSED`.

### Test 4 — Invalid State

**Input:** Project with missing, malformed or conflicting State.

**Expected:**

- No Discovery or Execution.
- State repair/escalation required.
- No blind overwrite.

### Test 5 — Duplicate Project

**Input:** New Project Name matching an existing Entry.

**Expected:**

- No duplicate creation.
- Existing Project summary returned.
- User choice required.

### Test 6 — Execution Before Discovery

**Input:** Immediate Coding/Execution request after Start Project.

**Expected:**

- Execution blocked.
- Discovery requirement explained.
- Full Guidance Response returned.

## 7. Implementation Order

1. Confirm Runtime Host and local Runtime boundary.
2. Define SQLite schema boundary without exposing it to Orchestrator.
3. Implement Registry Adapter.
4. Implement State Adapter and Version Check.
5. Implement Audit Adapter.
6. Implement Runtime Gateway.
7. Implement Project Resolver.
8. Implement Bootstrap Handler.
9. Implement Project Orchestrator Agent Interface.
10. Implement Discovery Interface.
11. Implement Response Renderer.
12. Run Tests 1–6.

אין להוסיף Tool Execution, Integrations או Parallel Workers לפני שכל בדיקות ה־MVP עוברות.

## 8. Risks

| Risk | Severity | Mitigation |
|---|---:|---|
| Host אינו מאפשר Interception | Blocking | לאשר Local Runtime עם Gateway מחייב לפני מימוש |
| SQLite הופך למודל State מקביל | Major | State Adapter בלבד; Canonical Model נשאר מקור האמת |
| Orchestrator ו־Runtime מתפצלים | Major | Interface יחיד ו־Runtime Adapter ללא בעלות חדשה |
| Discovery Skill עוקף Renderer | Major | Discovery Interface מחזיר Structured Output בלבד |
| Prototype מתרחב לפלטפורמה | Major | לנעול Scope ולדחות Execution/Integrations |
| כשל Commit | Major | Version Check, Audit ו־Fail-Closed |
| בדיקות לא מגלות עקיפה | Medium | לכלול Duplicate, Invalid State ו־Direct Execution |

## 9. Success Criteria

ה־Prototype מצליח כאשר:

- Project חדש נוצר דרך Gateway בלבד.
- Project קיים נפתר ללא Duplicate.
- Registry, State ו־Audit נשמרים באופן עקבי.
- Project Instance מתחיל ב־Discovery.
- Discovery מופעל דרך Orchestrator בלבד.
- State נשאר Persistent בין בקשות.
- Full Phase Guidance Response מוחזרת למשתמש.
- Direct Execution bypass נחסם.
- Tests 1–6 עוברים.

## 10. Next Step

לפני כתיבת קוד יש לאשר:

1. Runtime Host מקומי.
2. SQLite כ־MVP Storage ל־Registry/State/Audit.
3. Filesystem כתוצרי Project Instance.
4. Minimal Prototype Scope.
5. Test Matrix 1–6.

לאחר האישור, הצעד הראשון יהיה מימוש ובדיקת **Registry Adapter Contract** בלבד, ללא חיבור ל־Discovery או ל־Execution.
