# Minimal Runtime Slice Implementation Plan

**System:** AI Project Operating System  
**Status:** Proposed for Approval  
**Scope:** First Runtime Control Plane Slice  
**Related Contracts:**

- `runtime-control-plane-architecture-decision.md`
- `runtime-contract.md`
- `system-contracts-and-state-model.md`

## 1. Goal

לתכנן את המימוש הראשון של Runtime Control Plane במסלול המצומצם:

```text
Start Project
        ↓
Runtime Entry Gateway
        ↓
Resolve / Create Project Instance
        ↓
Bootstrap
        ↓
Load Project State
        ↓
Project Orchestrator Agent
        ↓
Discovery
        ↓
Phase Guidance Response
```

המטרה היא להוכיח שהמערכת יכולה לקבל בקשת פרויקט, ליצור או לזהות Project Instance, להתחיל Discovery ולהחזיר Guidance מלא — בלי לבצע Coding או Execution משמעותי.

## 2. Scope

### Included

- קבלת Runtime Request תקני.
- Initial Intent Classification.
- Project Resolution באמצעות Project Registry.
- מניעת Duplicate Project.
- יצירת Project Instance חדש.
- OS Version Binding.
- Bootstrap והכנת Workspace מינימלי.
- יצירת וטעינת Canonical Project State.
- הפעלת Project Orchestrator Agent Runtime.
- הפעלת Discovery Skill דרך Orchestrator בלבד.
- יצירת Phase Guidance Response מלאה.
- Audit בסיסי ליצירה, טעינה, החלטות ו־State Commit.
- Fail-Closed עבור Registry, State או Resolution שאינם זמינים.

### Excluded

- Full Execution Engine.
- כתיבת Production Code.
- External Actions.
- Advanced Automation.
- External Integrations.
- Multi-Agent Coordination.
- Parallel Workers.
- Complex Permissions.
- Full UI.
- Cross-Project Knowledge Sharing.
- Automatic OS Migration.
- Dashboard או Metrics Platform.

## 3. Components

### 3.1 Runtime Entry Gateway

מקבל Runtime Request, מאמת שדות בסיסיים ומבצע Classification ראשוני בלבד.

### 3.2 Project Resolver

מזהה Project Instance לפי Project ID או Project Registry ומחזיר:

- Existing Match.
- No Match.
- Ambiguous Match.
- Invalid Match.

### 3.3 Registry Adapter

מספק Read/Write מוגבל ל־Project Registry לצורך Resolution ויצירת Entry.

### 3.4 State Adapter

טוען, מאמת ומבצע Commit של Canonical Project State לפי Version, Actor, Timestamp ו־Audit.

### 3.5 Bootstrap Loader

מאתחל Project Instance חדש, OS Version Reference, Workspace מינימלי ו־Initial State.

### 3.6 Project Orchestrator Agent Runtime

מקבל Resolved Project Context, מזהה Current Phase, מפעיל Discovery ומרכיב State/Guidance Proposals.

### 3.7 Discovery Activation Boundary

מפעיל את Discovery Skill דרך חוזה Input/Output קיים. אינו מאפשר ל־Skill להחזיר Phase Guidance ישירות.

### 3.8 Response Renderer

מייצר את תגובת המשתמש היחידה עבור Phase Guidance:

- Current Phase.
- Status.
- Completed.
- Missing / Remaining Validation.
- Required User Action.
- Expected Output.
- Completion Criteria.
- Next Recommended Action.

## 4. Build Order

### Step 0 — Runtime Host Selection

**Purpose:** לבחור את סביבת ההפעלה הראשונה.  
**Dependencies:** Runtime Architecture Decision.  
**Input:** Client/Host constraints.  
**Output:** Host Decision ו־Runtime Boundary.  
**Validation:** כל Project Request חייב להיות מסוגל לעבור דרך Gateway.

אין להתחיל מימוש לפני בחירת Host ראשוני.

### Step 1 — Runtime Entry Gateway

**Purpose:** נקודת כניסה יחידה.  
**Dependencies:** Runtime Request Contract.  
**Input:** Runtime Request.  
**Output:** Validated Request ו־Initial Intent.  
**Validation:** בקשת Project אינה יכולה לעבור למסלול ישיר.

### Step 2 — Project Resolver

**Purpose:** זיהוי Project Instance.  
**Dependencies:** Registry Adapter.  
**Input:** Project ID/Name ו־Intent.  
**Output:** Existing / New / Ambiguous / Invalid Resolution.  
**Validation:** אין יצירה כאשר קיימת התאמה לא פתורה.

### Step 3 — Registry Adapter

**Purpose:** קריאה ועדכון מבוקר של Project Registry.  
**Dependencies:** Storage Boundary Decision.  
**Input:** Registry Query או Entry Proposal.  
**Output:** Registry Result או Commit Result.  
**Validation:** Required Fields, Unique Project ID ו־Audit.

### Step 4 — State Adapter

**Purpose:** טעינה ו־Commit של Canonical Project State.  
**Dependencies:** Canonical State Model.  
**Input:** Project ID ו־State Proposal.  
**Output:** State Snapshot או Commit Result.  
**Validation:** Version Check, Actor, Timestamp, Source ו־Audit.

### Step 5 — Bootstrap Loader

**Purpose:** יצירת Project Instance חדש.  
**Dependencies:** Resolver, Registry Adapter, State Adapter, OS Version.  
**Input:** New Project Request ו־OS Reference.  
**Output:** Registered Project Instance, Workspace ו־Initial State.  
**Validation:** `current_phase: Discovery`, `status: proposed`, ללא Knowledge זר.

### Step 6 — Project Orchestrator Agent Runtime

**Purpose:** ניהול ה־Control Flow לאחר Resolution/Bootstrap.  
**Dependencies:** State Snapshot, Lifecycle Rules, Contracts.  
**Input:** Request, Project State ו־Relevant Context.  
**Output:** Lifecycle Decision, Capability Request, State Proposal ו־Response Payload.  
**Validation:** אין Phase Transition ללא Completion Criteria.

### Step 7 — Discovery Activation

**Purpose:** ביצוע Discovery Analysis.  
**Dependencies:** Orchestrator, Discovery Skill, Project Context.  
**Input:** Task, Goal, Context, Constraints, Expected Output.  
**Output:** Findings, Assumptions, Open Questions, Risks ו־Recommendations.  
**Validation:** אין Product Decision לא מאושר ואין Phase Guidance ישיר.

### Step 8 — Response Renderer

**Purpose:** יצירת תגובת משתמש.  
**Dependencies:** Orchestrator Result ו־Phase Guidance Contract.  
**Input:** Completed, Missing, Validation, Criteria ו־Next Action.  
**Output:** Runtime Response.  
**Validation:** כל סעיפי החוזה קיימים; תגובה חלקית נדחית.

## 5. Runtime Flow

### First Run — New Project

```text
User Request
        ↓
Gateway validates Request ID, Client and Request
        ↓
Initial Intent: START_PROJECT
        ↓
Resolver queries Registry
        ↓
No Match
        ↓
Bootstrap creates Project ID and binds OS Version
        ↓
Registry Entry Commit
        ↓
Canonical Project State Initialization
        ↓
State Load and Version Check
        ↓
Orchestrator identifies Discovery
        ↓
Discovery Skill Invocation
        ↓
Output Validation
        ↓
State Update Proposal / Commit where allowed
        ↓
Response Renderer
        ↓
User Guidance
```

### Decision Points

- האם הבקשה קשורה לפרויקט.
- האם Project Instance קיים.
- האם יש Match יחיד.
- האם State תקין וזמין.
- האם Discovery ניתן להפעלה.
- האם State Proposal עומד ב־Commit Rules.
- האם Response עומדת ב־Phase Guidance Contract.

### Failure Points

- Invalid Request.
- Ambiguous Project.
- Registry unavailable.
- State unavailable.
- OS Version mismatch.
- Invalid Initial State.
- Discovery unavailable.
- Version Conflict.
- Incomplete Response.

כל Failure קריטי עוצר את הזרימה ואינו מבצע Project Execution.

## 6. Data Requirements

### 6.1 Project Registry

```yaml
project_registry_entry:
  project_id: <stable unique id>
  project_name: <name>
  owner: <human owner or pending confirmation>
  status: proposed | active | blocked | awaiting_approval | completed | cancelled
  current_phase: <canonical phase>
  os_version: <bound OS version>
  location: <workspace reference>
  created_date: <date>
  last_activity: <timestamp>
```

### 6.2 Project State

ה־Minimal Slice חייב לתמוך במבנה הקנוני הבא:

- `project_identity`: Project ID, Name, Description, Owner, Stakeholders.
- `current_status`: Current Phase, Status, Progress, Blockers.
- `planning_data`: Goals, Scope, Timeline, Resources.
- `decision_management`: Decisions, Pending Decisions, Approvals.
- `risk_management`: Risks, Dependencies, Issues.
- `knowledge`: Documents, Outputs, Lessons Learned.
- `next_actions`: Tasks, Owners, Due Dates.
- `audit`: Last Updated, Actor, Version, History Reference.

בעת Bootstrap, מידע שאינו ידוע נשאר ריק או Pending Confirmation ואינו מומצא.

### 6.3 Request Context

חובה:

- Request ID.
- Correlation ID.
- User ID.
- User Request.
- Timestamp.
- Source Client.

לפרויקט: Project ID או Project Name.

### 6.4 Response Context

חובה:

- Request ID.
- Project ID כאשר נפתר.
- Current Phase.
- Status.
- Completed.
- Missing.
- Required User Action.
- Expected Output.
- Completion Criteria.
- Next Recommended Action.

## 7. Execution Boundaries

### Allowed

- יצירת Project Instance.
- בדיקת Project Existence.
- Bootstrap.
- טעינת Project State.
- Discovery Analysis.
- שאלות הבהרה.
- יצירת Guidance ו־Proposals.
- Commit מאומת של Initial State ותוצרים מותרים.

### Not Allowed

- כתיבת Production Code.
- External Actions.
- שינוי Scope אוטומטי.
- החלטה אסטרטגית ללא אישור.
- Commit ללא Validation.
- דילוג Lifecycle.
- שימוש ב־Chat Context כמקור State.
- הפעלת Skill או Worker ישירות מה־Gateway.

## 8. Testing Plan

### Test 1 — New Project

**Input:** `Start Project: X`.

**Expected:**

- Gateway activated.
- No duplicate found.
- Project Instance created.
- Registry updated.
- OS Version bound.
- Canonical State initialized.
- Discovery invoked through Orchestrator.
- Full Guidance Response returned.

### Test 2 — Existing Project

**Input:** `Continue Project: X`.

**Expected:**

- Existing Project Instance resolved.
- No new Instance created.
- State loaded.
- Current Phase returned by Orchestrator.
- Full Guidance Response returned.

### Test 3 — Invalid State

**Input:** Missing or invalid Registry/State.

**Expected:**

- Fail-Closed.
- No Execution.
- Clear reason.
- Recovery or escalation action.

### Test 4 — Ambiguous Project

**Input:** Project Name with multiple matches.

**Expected:**

- No creation.
- User selection request.
- No State modification.

### Test 5 — Direct Execution Attempt

**Input:** Request to write project code immediately after Start Project.

**Expected:**

- Execution blocked.
- Discovery/Planning requirement explained.
- Full Phase Guidance Response returned.

## 9. Risks

| Risk | Severity | Mitigation |
|---|---:|---|
| Host אינו מאפשר Gateway מחייב | Blocking | לבחור Runtime Host עם Interception או לסמן Client כ־Non-Enforcing |
| Scope מתרחב ל־Execution Engine | Major | לנעול את Minimal Slice ולדחות Code/Tools |
| Registry ו־State נשמרים בשני מקורות סותרים | Major | Registry אינדקס; State מקור האמת המלא |
| Runtime Orchestrator הופך לבעלות נוספת | Major | להגדירו כ־Runtime Adapter ל־Project Orchestrator Agent |
| Discovery Skill מחזיר Guidance ישיר | Major | Handoff ו־Response Renderer יחיד |
| Version Conflict ב־Commit | Major | Version Check ו־Reload לפני Commit |
| בדיקות מכסות רק New Project | Medium | לכלול Existing, Ambiguous, Invalid ו־Direct Execution |

## 10. Success Criteria

ה־Minimal Runtime Slice נחשב מוכן כאשר:

- כל בקשת Project עוברת Gateway.
- Project Instance מזוהה או נוצר ללא כפילות.
- Registry ו־State נוצרים/נטענים ממקור אמת ברור.
- OS Version נקשרת ל־Instance.
- Bootstrap מתבצע ללא Discovery פנימי.
- Discovery מופעל רק דרך Orchestrator.
- אין Coding או Execution משמעותי ב־Slice.
- כל תגובת Phase עומדת ב־Response Contract.
- Fail-Closed עובד במצבי Registry, State, Version ו־Resolution.
- Tests 1–5 עוברים.

## 11. Next Implementation Step

לפני כתיבת קוד יש לאשר:

1. Runtime Host ראשוני.
2. מקור Persistence ראשוני ל־Project Registry ו־Project State.
3. Runtime Request/Response Contracts.
4. State Commit ו־Audit Boundary.
5. Minimal Slice Scope ללא הרחבת Execution.

לאחר אישור, הצעד הראשון יהיה מימוש **Runtime Entry Gateway Contract** בלבד, עם Test עבור `Start Project: X`, לפני חיבור Bootstrap או Discovery.
