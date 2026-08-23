# Runtime Contract Decision Document

**System:** AI Project Operating System  
**Status:** Proposed for Approval  
**Scope:** Minimal Runtime Control Plane contract  
**Canonical State:** `00_Architecture/system-contracts-and-state-model.md`  
**Related Decision:** `00_Architecture/runtime-control-plane-architecture-decision.md`

## 1. Purpose

מסמך זה מגדיר את החוזה המינימלי בין User, Runtime Control Plane, Project Instance, Project Orchestrator Agent, Lifecycle, Skills, Workers ו־Project State.

מטרתו לאפשר מימוש עקבי ללא שינויי בעלות, עקיפת Lifecycle או יצירת מודל State נוסף.

## 2. Runtime Identity

### 2.1 Project Instance Identity

כל בקשת Runtime הקשורה לפרויקט חייבת להיפתר ל־Project Instance בעל:

```yaml
project_instance_identity:
  project_id: <stable unique id>
  project_name: <name>
  owner: <human owner>
  os_version_reference: <bound OS version>
  current_phase: <canonical lifecycle phase>
  current_status: proposed | active | blocked | awaiting_approval | completed | cancelled
```

שדות אלה הם Reference/Projection של ה־Canonical Project State וה־Project Registry; הם אינם מודל State חדש.

### 2.2 Request Resolution

- אם קיים `project_id`, השתמש בו כמזהה הראשי.
- אם קיים רק Project Name, חפש ב־Project Registry.
- אם אין התאמה, ניתוב ל־Project Instance Bootstrap.
- אם קיימת התאמה יחידה, טען את ה־Project Instance.
- אם קיימות מספר התאמות, עצור ובקש בחירה.
- אם קיימת התאמה דומה אך לא ודאית, אל תיצור או תמזג ללא אישור.

## 3. Gateway Contract

### 3.1 Input

```yaml
runtime_request:
  request_id: <unique request id>
  user_request: <raw user request>
  project_id: <optional>
  project_name: <optional>
  workspace_context: <optional context reference>
  available_metadata: []
  client_id: <client identity>
  received_at: <timestamp>
```

### 3.2 Responsibilities

Runtime Entry Gateway:

- מקבל את הבקשה הראשונה.
- מזהה אם היא קשורה לניהול פרויקט.
- מבצע או מפעיל Intent Detection.
- מבקש Project Resolution.
- מנתב ל־Bootstrap או ל־Runtime Orchestrator.

### 3.3 Prohibitions

Gateway אינו רשאי:

- לבצע Project Work.
- לשנות Project State.
- לאשר מעבר Phase.
- להפעיל Skill או Worker ישירות.
- לעקוף Lifecycle או Response Renderer.

## 4. Orchestrator Agent Contract

### 4.1 Responsibility

Project Orchestrator Agent הוא בעל האחריות התפעולית על:

- Project Progression.
- Current Phase ו־Status.
- Required Outputs ו־Completion Criteria.
- Skill Activation.
- Worker Delegation.
- Decision Routing.
- Escalation.
- User Guidance.

### 4.2 Input

```yaml
orchestrator_context:
  runtime_request: <request contract>
  project_instance_identity: <resolved identity>
  os_version: <bound OS version>
  project_state_snapshot: <canonical snapshot>
  relevant_project_knowledge: []
  relevant_decisions: []
  relevant_risks: []
  lifecycle_rules: <applicable rules>
  available_capabilities: []
```

### 4.3 Output

ה־Orchestrator מחזיר ל־Runtime Control Plane:

```yaml
orchestrator_result:
  status: continue | needs_input | needs_approval | blocked | completed | escalated
  current_phase: <phase>
  required_outputs: []
  completed_outputs: []
  missing_items: []
  execution_request: <optional authorized request>
  state_update_proposal: []
  response_payload: <data for Response Renderer>
  next_action: <action>
```

ה־Orchestrator אינו משנה Global OS Knowledge או פרויקט אחר.

## 5. Lifecycle Contract

### 5.1 Phase Identification

השלב הפעיל נקבע מתוך `project_state.current_status.current_phase`. אין להסיק Phase רק מהודעת המשתמש או מהיסטוריית השיחה.

### 5.2 Phase Control

ה־Orchestrator מזהה:

- Current Phase.
- Required Outputs.
- Completed Outputs.
- Missing Information.
- Validation Required.
- Open Questions.
- Risks and Blockers.
- Completion Criteria.

### 5.3 Canonical Lifecycle Terminology

- `Discovery` — הבנת הבעיה, המשתמשים והצורך.
- `Strategy` — כיוון, ערך ומטרות.
- `Planning` — Scope, תוכנית, משאבים ותלותים.
- `Design` — תכנון פתרון כאשר נדרש.
- `Execution` — ביצוע מאושר.
- `Validation` — בדיקת תוצר, מידע או תנאי קבלה.
- `Launch` — פעולה חיצונית משמעותית כאשר נדרש.
- `Learning` — למידה וסיכום פרויקט.
- `Review` — מנגנון רוחבי, לא בהכרח Phase עצמאי.
- `Improvement` — תהליך שיפור מערכת מבוקר.
- `Completed` — ערך Status קנוני, לא Phase.

### 5.4 Transition Rules

מעבר דורש:

1. Required Outputs קיימים.
2. Completion Criteria מתקיימים.
3. אין Blocker לא פתור.
4. Risks קריטיים טופלו או אושרו.
5. Approval קיים כאשר נדרש.
6. State Update Proposal עבר Validation ו־Commit.

אין לבצע מעבר Phase רק משום שהמשתמש ביקש לדלג.

## 6. Skill/Worker Handoff Contract

### 6.1 Invocation Input

```yaml
capability_request:
  task_id: <task id>
  capability_type: skill | worker
  capability_name: <approved capability>
  project_id: <project id>
  current_phase: <phase>
  task: <task>
  goal: <goal>
  context: []
  constraints: []
  expected_output: []
  acceptance_criteria: []
```

### 6.2 Invocation Output

```yaml
capability_result:
  status: completed | partial | blocked | escalated
  result: []
  evidence: []
  confidence: <known scale or qualitative label>
  findings: []
  assumptions: []
  recommendations: []
  risks: []
  decisions_required: []
  created_artifacts: []
  state_update_proposal: []
  handoff:
    requested_orchestrator_action: <action>
```

### 6.3 Rules

Skills ו־Workers:

- אינם משנים Canonical State ישירות.
- אינם משנים Lifecycle Phase.
- אינם משנים Scope או Goals.
- אינם מאשרים החלטות אסטרטגיות.
- אינם מייצרים Phase Guidance ישירות למשתמש.
- מחזירים תוצאה ל־Orchestrator בלבד.

## 7. State Contract

### 7.1 Read

Runtime רשאי לקרוא:

- Project Registry לצורך Resolution.
- Project State לצורך ניהול הפרויקט.
- Project Knowledge רלוונטי בלבד.
- System Knowledge מאושר לצורך OS Capabilities.

### 7.2 Write Proposal

Orchestrator, Skills ו־Workers יכולים להציע עדכונים בהתאם לתחום אחריותם. ההצעה חייבת לכלול:

```yaml
state_update_proposal:
  proposal_id: <id>
  project_id: <id>
  target_paths: []
  proposed_values: {}
  reason: <reason>
  source_task_id: <task id>
  actor: <actor>
  timestamp: <timestamp>
  expected_impact: <impact>
```

### 7.3 Commit

State Adapter מבצע Commit רק כאשר:

- Project ID תואם.
- Version Check הצליח.
- Actor מזוהה.
- Timestamp קיים.
- מקור Task או Decision קיים.
- אין סתירה עם State עדכני.
- Approval קיים כאשר נדרש.

ה־Orchestrator הוא בעל ההחלטה התפעולית; State Adapter הוא גבול ההתמדה והאימות הטכני. Human Owner מאשר Goals, Scope משמעותי והחלטות אסטרטגיות.

כל Commit יוצר Audit Record ו־Version חדש לפי המודל הקנוני.

## 8. Execution Gate

### 8.1 Requires Authorization

נדרש Gate עבור:

- Code Creation או Execution משמעותי.
- External Actions.
- Scope Changes.
- Phase Transitions.
- Canonical State Commits.
- החלטות משפטיות, כספיות, רגולטוריות או בלתי הפיכות.

### 8.2 Does Not Require Execution Gate

בדרך כלל אין צורך ב־Execution Gate עבור:

- Analysis בלבד.
- שאלות הבהרה.
- Suggestions שאינן מבצעות שינוי.
- יצירת Proposal שאינו Commit.

### 8.3 Fail Behavior

כאשר Execution מבוקש לפני אישור או לפני תנאי Phase:

- חסום את הפעולה.
- אל תיצור Artifact ביצועי כאילו אושר.
- הסבר מה חסר.
- הצג Required User Action דרך Response Renderer.
- שמור Proposal או Escalation בלבד, אם רלוונטי.

## 9. Response Contract

Response Renderer הוא הסמכות היחידה לתגובות משתמש הקשורות ל־Phase.

### Required Phase Guidance

כל תגובה כאשר Phase אינו שלם כוללת:

- Current Phase.
- Status.
- Completed.
- Remaining Validation / Missing Items.
- Required User Action.
- Expected Output.
- Completion Criteria.
- Next Recommended Action.

Skills מספקים Findings, Assumptions, Recommendations ו־Evidence. Workers מספקים Execution Results. ה־Renderer בלבד הופך אותם להנחיית Phase למשתמש.

## 10. Failure Handling

המערכת פועלת Fail-Closed:

| Failure | Block | Explain | Recovery |
|---|---|---|---|
| Registry unavailable | Project Resolution/Creation | לא ניתן לזהות Instance | להחזיר Registry ולנסות שוב |
| State unavailable | Project Action | לא ניתן לדעת מצב קנוני | לשחזר גישה ל־State, ללא Execution |
| Gateway unavailable | Project Request | אין נקודת כניסה מאומתת | להשתמש ב־Runtime נתמך בלבד |
| Version mismatch | Capability/State Commit | OS Version אינה תואמת | Compatibility Assessment / Upgrade Decision |
| Invalid Project Instance | כל פעולה פרויקטלית | Identity או State לא תקינים | תיקון או הסלמה ל־Owner |
| Ambiguous resolution | Creation/Continuation | נמצאו מספר Instances אפשריים | בחירת משתמש מפורשת |
| Commit conflict | State Commit | State השתנה מאז הקריאה | Reload, Re-evaluate, Re-Approve |

אין לבצע פעולה פרויקטלית משמעותית כאשר אחד מהשירותים הקריטיים אינו זמין.

## 11. Minimal Implementation Scope

### In Scope

```text
Start Project
        ↓
Gateway
        ↓
Resolve Instance
        ↓
Bootstrap
        ↓
Load State
        ↓
Project Orchestrator Agent
        ↓
Discovery
        ↓
Guidance Response
```

### Required Components

- Runtime Entry Gateway.
- Minimal Project Resolver.
- Minimal Registry Adapter.
- Minimal State Adapter.
- Bootstrap Loader.
- Runtime Orchestrator Adapter.
- Discovery invocation boundary.
- Phase Guidance Response Renderer.

### Deferred

- Full tool-by-tool Execution Gate.
- Parallel Workers.
- External Integrations.
- Automation.
- Dashboards.
- Cross-project Knowledge Sharing.
- Automatic OS Migration.

### Success Criteria

- `Start Project: X` cannot bypass Gateway.
- Existing Project is resolved before creation.
- New Project Instance receives Project ID and OS Version.
- Canonical Project State is initialized and loaded.
- Discovery is invoked through the Orchestrator boundary.
- User response follows the complete Phase Guidance Contract.
- No direct Coding/Execution occurs in this slice.

## 12. Approval Criteria

יש לאשר את החוזה לפני מימוש רק כאשר:

- קיימת סמכות Runtime יחידה.
- Gateway, Resolver, State Adapter ו־Orchestrator אינם חולקים בעלות.
- Project State נשאר המודל הקנוני היחיד.
- State Commit מחייב Version, Actor, Timestamp ו־Audit.
- Skills ו־Workers מחזירים Handoff בלבד.
- Execution Gate מוגדר ומסוגל לחסום פעולה לא מאושרת.
- Response Renderer הוא מקור התגובה היחיד ל־Phase Guidance.
- Failure Handling הוא Fail-Closed.
- Minimal Slice מופרד מהרחבות עתידיות.

האישור אינו מאשר קוד, טכנולוגיה, Worker, Skill או Automation ספציפיים.
