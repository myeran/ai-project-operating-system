# Runtime Request Response and Storage Boundary Decision

**System:** AI Project Operating System  
**Status:** Proposed for Approval  
**Scope:** Runtime Contract and Persistence Boundaries  
**Related Contract:** `00_Architecture/runtime-contract-decision.md`  
**Canonical State:** `00_Architecture/system-contracts-and-state-model.md`

## 1. Purpose

מסמך זה מגדיר את גבולות המימוש הנדרשים לפני בניית Runtime Control Plane Minimal Slice:

- כיצד Request נכנס למערכת.
- כיצד רכיבים מתקשרים.
- כיצד Response נוצר.
- היכן נשמרים Registry, Project State ו־Audit.
- מי רשאי לקרוא, להציע שינוי, לבצע Commit ולאשר פעולה.

המסמך אינו מגדיר קוד, Storage טכני, Worker או Skill חדש.

## 2. Request Contract

### 2.1 Canonical Runtime Request

```yaml
runtime_request:
  request_id: <unique request id>
  correlation_id: <conversation or workflow correlation id>
  user_id: <user identity or approved anonymous reference>
  project_id: <optional stable project id>
  project_name: <optional project name>
  intent: <initially classified intent>
  request_type: <canonical request type>
  user_request: <original user request>
  workspace_context: <optional workspace reference>
  available_metadata: []
  timestamp: <received timestamp>
  source_client: <client identity>
```

### 2.2 Required Fields

- `request_id` — מזהה ייחודי לכל בקשה.
- `correlation_id` — מקשר את הבקשה לשיחה או Workflow.
- `user_id` — מזהה משתמש או Reference מאושר.
- `user_request` — הטקסט המקורי ללא שינוי.
- `timestamp` — זמן קבלת הבקשה.
- `source_client` — מקור הבקשה.

`project_id` או `project_name` נדרש כאשר הבקשה קשורה לפרויקט קיים. עבור `START_PROJECT`, Project Name או שם עבודה זמני נדרש לפני Bootstrap.

### 2.3 Optional Fields

- `project_id` כאשר מדובר בפרויקט חדש.
- `project_name` כאשר קיים Project ID.
- `workspace_context`.
- `available_metadata`.
- `intent` ו־`request_type` לפני סיווג ראשוני.

### 2.4 Validation Rules

- `request_id` ו־`correlation_id` אינם ריקים.
- `request_id` אינו משמש פעם נוספת לבקשה אחרת.
- `timestamp` נוצר ב־Gateway ואינו מתקבל מהמשתמש כמקור סמכות.
- `source_client` מזוהה.
- `project_id` חייב להתאים ל־Project Registry כאשר הוא קיים.
- Intent לא ודאי מסומן `ambiguous` ואינו מפעיל פעולה בלתי הפיכה.
- Gateway אינו מקבל שדות State שהמשתמש מבקש לכפות כעובדה.

## 3. Routing Contract

### 3.1 Ownership

#### Gateway

- מבצע Initial Classification בלבד.
- מזהה אם הבקשה קשורה לפרויקט.
- מסווג `intent` ראשוני.
- מבקש Project Resolution.
- אינו מקבל החלטת Project Action סופית.

#### Project Resolver

- מזהה Project Instance באמצעות Project ID או Project Registry.
- מחזיר Match יחיד, No Match או Ambiguous Match.
- אינו משנה Project State.

#### Orchestrator

- מקבל את ה־Request ואת תוצאת ה־Resolution.
- מבצע Final Project Action Decision.
- טוען State ו־Context רלוונטיים.
- מחליט על Lifecycle, Skill/Worker, Approval או Escalation.

### 3.2 Routing Examples

| Request Type | Routing Decision |
|---|---|
| `START_PROJECT` | Project Existence Check → Bootstrap → Initialize State → Discovery Handoff |
| `CONTINUE_PROJECT` | Resolve Project → Load State → Continue Lifecycle |
| `STATUS` | Resolve Project → Read State → Response Renderer |
| `EXECUTION_REQUEST` | Resolve Project → Load State → Policy/Execution Gate |
| `VALIDATION_REQUEST` | Resolve Project → Load Phase State → Orchestrator Validation Guidance |
| `AMBIGUOUS` | עצירה → Clarification או User Selection |

ה־Gateway אינו מפעיל Skills, Workers או Execution ישירות.

## 4. Response Contract

### 4.1 Canonical Runtime Response

```yaml
runtime_response:
  request_id: <request id>
  correlation_id: <correlation id>
  project_id: <project id if resolved>
  current_phase: <phase or null>
  status: <canonical status or response status>
  completed: []
  missing: []
  required_user_action: <single action or None identified>
  expected_output: []
  completion_criteria: []
  next_recommended_action: <next action>
  response_type: guidance | clarification | escalation | confirmation | error
```

### 4.2 User-Facing Authority

רק Response Renderer, תחת Lifecycle Orchestrator, רשאי ליצור תגובה הקשורה ל־Phase.

כל תגובה כאשר Phase אינו שלם חייבת לכלול:

- Current Phase.
- Status.
- Completed.
- Missing.
- Required User Action.
- Expected Output.
- Completion Criteria.
- Next Recommended Action.

Skills ו־Workers מחזירים Structured Results בלבד. File Link, Task Request או Current Phase בלבד אינם Response תקפים כאשר נדרשת פעולת משתמש.

### 4.3 Response Validation

לפני הצגה למשתמש:

1. ודא ש־`request_id` תואם לבקשה.
2. ודא ש־`project_id` תואם ל־Resolution.
3. ודא שכל סעיפי Phase Guidance קיימים.
4. אם סעיף חסר, השלֵם אותו או כתוב `None identified`.
5. ודא שה־Required User Action הוא פעולה אחת, ספציפית וברורה.

## 5. Storage Boundary

### 5.1 Project Registry

#### Purpose

Project Registry הוא מקור האמת לאינדקס Project Instances, Resolution ומניעת כפילויות.

#### Required Fields

```yaml
project_registry_entry:
  project_id: <stable unique id>
  project_name: <name>
  owner: <human owner>
  status: <canonical status>
  current_phase: <canonical phase>
  os_version: <bound OS version>
  location: <canonical workspace reference>
  created_date: <date>
  last_activity: <timestamp>
```

Registry אינו מחליף את Project State ואינו מכיל את כל Project Knowledge.

### 5.2 Project State Storage

#### Canonical State

Project State הוא הרשומה הקנונית היחידה למצב Project Instance, לפי `system-contracts-and-state-model.md`.

#### Read Authority

- State Adapter קורא את ה־Canonical State.
- Runtime Orchestrator רשאי לצרוך Snapshot.
- Skills ו־Workers מקבלים רק Context רלוונטי דרך Orchestrator.
- User אינו כותב State ישירות.

#### Write Proposal Authority

- Orchestrator רשאי להציע עדכוני Workflow ו־State בתחום אחריותו.
- Skills רשאים להציע Findings, Risks, Recommendations ו־State Updates בתחום שלהם.
- Workers רשאים להציע תוצאות ביצוע ו־State Updates בתחום המשימה.
- Human Owner מאשר Goals, Scope משמעותי והחלטות אסטרטגיות.

#### Commit Authority

State Adapter הוא גבול ה־Persistence וה־Commit הטכני. הוא מבצע Commit רק להצעה מאומתת ומורשית שהתקבלה דרך Orchestrator.

## 6. State Commit Rules

כל Commit חייב לכלול:

```yaml
commit_context:
  proposal_id: <proposal id>
  project_id: <project id>
  expected_version: <version read>
  new_version: <next version>
  actor: <authorized actor>
  timestamp: <commit timestamp>
  source_task_id: <task id>
  source_decision_id: <optional decision id>
  audit_record_id: <audit id>
```

Commit מותר רק כאשר:

- Project ID תואם.
- `expected_version` תואם לגרסה הנוכחית.
- Actor מזוהה ומורשה.
- Timestamp קיים.
- קיימת סיבת שינוי ומקור Task או Decision.
- אין סתירה עם State עדכני.
- Approval קיים כאשר נדרש.

כשל Version Check מחייב Reload ו־Re-evaluation. אין לבצע Blind Overwrite.

## 7. Audit Storage

Audit מתעד לכל הפחות:

- State Changes.
- Phase Transitions.
- Decisions.
- Approvals.
- Execution Authorizations.
- Rejections, Blocks ו־Escalations.
- Version Changes ו־Conflicts.

```yaml
audit_record:
  audit_id: <unique id>
  request_id: <request id>
  correlation_id: <correlation id>
  project_id: <project id>
  event_type: <event type>
  actor: <actor>
  timestamp: <timestamp>
  before_version: <version>
  after_version: <version or null>
  reason: <reason>
  source_reference: <task / decision / proposal>
  result: approved | rejected | blocked | committed
```

Audit אינו מקור אמת להחלפת Project State; הוא Evidence של פעולות ושינויים.

## 8. Action Authorization

### 8.1 Authorization Table

| Action Type | Required Phase | Required Approval | Risk Level |
|---|---|---|---|
| `READ_STATE` | כל Phase | None | Low |
| `START_PROJECT` | Before Phase | None, לאחר Existence Check | Low |
| `RUN_DISCOVERY` | Discovery | None for analysis; Owner input when needed | Low/Medium |
| `RUN_ANALYSIS` | לפי Current Phase | None for analysis בלבד | Low/Medium |
| `CREATE_ARTIFACT` | לפי Current Phase | None אם בתחום Scope מאושר | Low/Medium |
| `EXECUTE_CODE` | Execution לאחר Planning/Design לפי צורך | Execution authorization; Human approval לפי סיכון | High |
| `CHANGE_SCOPE` | Planning ומעלה | Human Owner | High |
| `TRANSITION_PHASE` | לפי Completion Criteria | Orchestrator; Human approval לפי Gate | Medium/High |
| `COMMIT_STATE` | כל Phase | State Validation; Human approval לפי שדה | Low/High |

### 8.2 Gate Rules

- Analysis, Questions ו־Suggestions אינם Execution.
- Proposal אינו Commit.
- Code Creation או פעולה חיצונית דורשים Gate.
- Scope, Goals, Strategic Decisions ו־Irreversible Actions דורשים Human Approval.
- State Commit תמיד דורש Validation; לא כל Commit דורש אישור אנושי.
- פעולה שאינה עומדת בתנאים נחסמת ואינה יוצרת Artifact ביצועי.

## 9. Minimal Slice Boundary

### Included

```text
Start Project
        ↓
Resolve/Create Instance
        ↓
Bootstrap
        ↓
Load State
        ↓
Discovery
        ↓
Guidance Response
```

### Required Boundaries

- Gateway מקבל ומסווג Request.
- Resolver בודק Registry.
- Bootstrap יוצר Instance חדש בלבד.
- State Adapter יוצר וטוען State.
- Orchestrator מפעיל Discovery.
- Response Renderer מחזיר Guidance מלא.
- אין Code Execution או External Action ב־Slice הראשון.

### Excluded

- Full Tool Execution Gateway.
- Parallel Workers.
- External Integrations.
- Automation.
- Dashboards.
- Cross-Project Knowledge Sharing.
- Automatic OS Migration.
- טכנולוגיית Storage ספציפית.

## 10. Risks

| Risk | Severity | Mitigation |
|---|---:|---|
| Gateway ו־Orchestrator מקבלים אחריות חופפת | Major | Gateway מסווג בלבד; Orchestrator מחליט פעולה סופית |
| Registry ו־State אינם מסונכרנים | Major | Registry לאינדקס בלבד ו־State כמקור האמת המלא |
| Commit ללא Version Check | Major | Optimistic Version Check ו־Audit חובה |
| Client עוקף Gateway | Blocking | Client ללא Gateway מוגדר Non-Enforcing ואינו רשאי לבצע Project Actions |
| Response חלקית | Major | Response Renderer Validation לפני שליחה |
| הרחבת Slice מוקדמת | Medium | לאסור Code/External Actions בגרסה הראשונה |

## 11. Approval Criteria

יש לאשר את גבולות המימוש כאשר:

- Request Contract יציב ומזהה כל בקשה.
- Gateway מסווג בלבד ואינו מנהל Project Action.
- Orchestrator הוא בעל ההחלטה הסופית.
- Registry, State ו־Audit הם גבולות נפרדים וברורים.
- State Commit דורש Version, Actor, Timestamp, Source ו־Audit.
- Execution Authorization מוגדר לכל Action Type ב־Minimal Slice.
- Response Renderer הוא הסמכות היחידה לתגובות Phase.
- Client ללא Gateway אינו נחשב Runtime נתמך.
- Minimal Slice אינו כולל Code Execution או Automation.

האישור אינו מאשר קוד, טכנולוגיית Storage, Worker, Skill או Automation.
