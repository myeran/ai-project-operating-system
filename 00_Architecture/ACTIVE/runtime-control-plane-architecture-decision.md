# Runtime Control Plane Architecture Decision

**System:** AI Project Operating System  
**Decision Status:** Proposed for Approval  
**Scope:** Runtime boundary only — no implementation  
**Canonical State:** `ACTIVE/system-contracts-and-state-model.md`

## 1. Executive Summary

המערכת המתועדת כוללת Control Plane עשיר, אך חסרה שכבת Runtime שמכריחה בקשות פרויקט לעבור דרכו.

ההחלטה המוצעת היא להוסיף **Runtime Control Plane יחיד** במודל Hybrid:

- ChatGPT Project / Codex / UI משמשים User and Execution Clients.
- Runtime Control Plane משמש Entry Gateway, Resolver, Orchestrator, Policy Gate ו־Response Authority.
- Skills ו־Workers נשארים יכולות ביצוע, לא שכבות ניהול.
- Project State ו־Project Registry נטענים ומתעדכנים דרך Adapter יחיד.

```text
User / Client
      ↓
Runtime Control Plane
      ↓
Project Instance + OS Capabilities
      ↓
Skills / Workers / Tools
      ↓
Validated State Update
      ↓
User Response
```

## 2. Problem Statement

ה־Workers וה־Workflows הקיימים מתועדים במסמכים, אך אין רכיב Runtime שמקבל כל בקשה, מזהה אותה כבקשת פרויקט, טוען Project Instance ומונע Execution ישיר.

כתוצאה מכך ChatGPT Project עלול לפעול מתוך Chat Context בלבד ולעקוף:

- Project Entry Point.
- Project Bootstrap.
- Lifecycle Orchestrator.
- Execution Gate.
- Phase Guidance Output Contract.

## 3. Runtime Responsibilities

### 3.1 Runtime Entry Gateway

אחריות:

- לקבל כל בקשה מה־Client.
- לזהות האם היא קשורה לפרויקט.
- לנתב בקשות פרויקט ל־Control Plane.
- למנוע תשובת Project Management ישירה מה־Chat Context.

בקשות שאינן קשורות לפרויקט יכולות לעבור במסלול רגיל, אם אין להן השפעה על Project State או Project Outputs.

### 3.2 Project Resolver

אחריות:

- לזהות Project ID או Project Name.
- לחפש ב־Project Registry.
- להבדיל בין New, Continue, Status, Compare ו־Ambiguous.
- למנוע יצירת Duplicate Project.

New Project ללא התאמה עובר ל־Bootstrap. התאמה קיימת דורשת החלטת משתמש כאשר אינה חד־משמעית.

### 3.3 State Adapter

אחריות:

- לטעון את Project State הקנוני.
- לטעון את OS Version הקשורה ל־Project Instance.
- להחזיר State Snapshot ל־Runtime Orchestrator.
- לקבל State Update Proposal.
- לבצע Commit רק לאחר Validation והרשאה.

ה־State Adapter הוא בעל גישה טכנית ל־State, אך ה־Orchestrator הוא בעל ההחלטה התפעולית על שינויו.

### 3.4 Runtime Orchestrator

אחריות:

- לזהות Intent.
- לזהות Current Phase ו־Status.
- לבחור Skill, Worker או Template.
- לנהל Handoff.
- לנתב החלטות ואישורים.
- לבדוק Completion Criteria.
- להחליט אם להמשיך, לעצור, להסלים או להציע מעבר.

הוא אינו מחליף את Project Orchestrator Agent ברמת המתודולוגיה; הוא שכבת ההפעלה שמממשת את סמכותו בזמן Runtime.

### 3.5 Execution Gate

אחריות:

- לבדוק אם פעולה מותרת לפי Phase, Scope, Risk ו־Approval.
- לחסום Execution שאינו עומד בתנאים.
- לאפשר ביצוע לאחר שה־Control Plane אישר אותו.

#### Allowed

- Discovery Analysis.
- Research.
- Planning.
- יצירת תוצרים מאושרים.
- Execution לאחר Planning/Design ותנאי המעבר הנדרשים.

#### Blocked

- Coding או Execution משמעותי לפני Planning כאשר הוא נדרש.
- שינוי Scope ללא Review ואישור.
- שינוי Project State ללא Validation.
- החלטה אסטרטגית ללא Human Approval.
- מעבר Phase ללא Completion Criteria.

### 3.6 Response Renderer

אחריות:

- להיות הסמכות היחידה לתגובות Phase למשתמש.
- להרכיב Phase Guidance Output Contract מלא.
- להציג Completed, Missing, Validation, Required User Action, Expected Output, Completion Criteria ו־Next Recommended Action.
- להציג Skill/Worker outputs כתוכן מקור, לא כהנחיית Phase ישירה.

Skills ו־Workers אינם מחזירים Phase Guidance ישירות למשתמש.

## 4. Component Architecture

```text
Runtime Entry Gateway
        ↓
Project Resolver
        ↓
Bootstrap Loader / State Adapter
        ↓
Runtime Orchestrator
        ↓
Execution Gate
        ↓
Skill / Worker / Tool Adapter
        ↓
Output Validator
        ↓
State Update Commit
        ↓
Response Renderer
        ↓
User
```

### Single Ownership Rules

- Gateway owns request entry.
- Resolver owns Project Instance identification.
- State Adapter owns State persistence boundary.
- Runtime Orchestrator owns routing and progression.
- Execution Gate owns authorization to execute.
- Response Renderer owns user-facing Phase guidance.
- Skills/Workers own domain execution only.

אין להוסיף Orchestrator מקביל או Response Authority נוסף.

## 5. Runtime Host Decision

### Option A — ChatGPT Project as Runtime Host

**Benefits:**

- חוויית משתמש טבעית.
- Context וידע זמינים בשיחה.
- התחלה מהירה.

**Limitations:**

- אין ודאות שכל הודעה תעבור Interception מחייב.
- קשה להבטיח Execution Gate.
- קשה להבטיח State/Registry Commit אטומי.

**Control Level:** נמוך עד בינוני. מתאים כ־Client או Prototype, לא כנקודת אכיפה יחידה.

### Option B — Custom GPT / Agent Runtime

**Benefits:**

- הוראות וכלים ממוקדים יותר.
- יכולת טובה יותר לנתב Workflow.
- חוויית משתמש פשוטה.

**Limitations:**

- עדיין תלוי ביכולות Host ופלטפורמה.
- לא בהכרח מספק Gateway, State Commit ו־Execution Gate מלאים.

**Control Level:** בינוני. מתאים לממשק מבוקר, אך דורש בדיקה של יכולת האכיפה בפועל.

### Option C — External Runtime Application/API

**Benefits:**

- שליטה מלאה ב־Gateway.
- State/Registry ו־Policy Enforcement ניתנים לאכיפה.
- ניתן ליישם Fail-Closed, Audit ו־Version Binding.

**Limitations:**

- עלות פיתוח ותחזוקה.
- דורש ממשק משתמש או חיבור ל־Chat.
- מוסיף רכיב תפעולי.

**Control Level:** גבוה.

### Option D — Hybrid Model

ChatGPT Project, Codex או UI משמשים Clients. Runtime Control Plane חיצוני או מקומי מנהל Routing, State, Policy ו־Responses.

**Benefits:**

- שומר חוויית משתמש טבעית.
- מוסיף נקודת אכיפה אמיתית.
- מאפשר החלפת Clients בלי לשנות את ה־Control Plane.

**Limitations:**

- דורש חיבור בין Client ל־Runtime.
- דורש הגדרת גבולות ברורה בין Client ל־Authority.

**Control Level:** גבוה, כאשר כל בקשת פרויקט עוברת דרך ה־Runtime.

### Recommended Host

**Option D — Hybrid Model**.

ChatGPT Project אינו יהיה ה־Project Instance או ה־Control Plane. הוא יהיה Client/Workspace. Runtime Control Plane יהיה נקודת האכיפה וה־Source of Runtime Authority.

## 6. Project Instance Relationship

הבחירה היא:

**B. ChatGPT Project = Workspace for Project Instance**

Project Instance הוא הישות הקנונית הכוללת Project ID, Registry Entry, Project State, Knowledge, Evidence ו־OS Version Binding.

ChatGPT Project הוא סביבת עבודה שיכולה לארח את ה־Instance, אך אינה מחליפה את ה־Registry או את ה־Canonical State.

## 7. Canonical Runtime Flow

```text
User Request
        ↓
Runtime Entry Gateway
        ↓
Intent Detection
        ↓
Project Resolver
        ↓
Project Instance Bootstrap or Load
        ↓
Load OS Version
        ↓
Load Canonical Project State
        ↓
Runtime Orchestrator
        ↓
Lifecycle / Policy Decision
        ↓
Execution Gate
        ↓
Skill / Worker / Tool Execution
        ↓
Output Validation
        ↓
State Update Proposal
        ↓
Commit Through State Adapter
        ↓
Response Renderer
        ↓
User
```

כאשר State, Intent או הרשאה אינם ברורים, הזרימה נעצרת ומוחזרת תגובת Escalation במקום Execution.

## 8. Isolation and Governance Rules

- Project State הוא Canonical State יחיד לכל Project Instance.
- Project Knowledge נשאר מבודד כברירת מחדל.
- Project Registry מכיל אינדקס, לא את כל פרטי הפרויקט.
- Skills ו־Workers מקבלים Context רלוונטי בלבד.
- Skills ו־Workers אינם מבצעים State Commit.
- Human Owner מאשר Goals, Scope משמעותי והחלטות אסטרטגיות.
- System Owner מאשר שינויי OS, Contracts ו־System Core.
- Knowledge Promotion דורש Evidence, Review, Abstraction ואישור.
- OS Updates אינם מתפשטים אוטומטית.
- Invalid או Ambiguous State נכשל בצורה סגורה — ללא Execution.

## 9. Minimal Implementation Scope

### In Scope

המסלול הראשון בלבד:

```text
Start Project
        ↓
Resolve / Create Project Instance
        ↓
Bootstrap
        ↓
Initialize Project State
        ↓
Start Discovery
        ↓
Render Phase Guidance
```

### Required Runtime Components

- Runtime Entry Gateway.
- Project Resolver.
- Minimal Registry Adapter.
- Minimal State Adapter.
- Bootstrap Loader.
- Runtime Orchestrator.
- Phase Guidance Response Renderer.

### Deferred

- Full Execution Gateway for all tools.
- Multi-Worker parallelism.
- External Integrations.
- Automation.
- Dashboards.
- Complex Permission System.
- Cross-Project Knowledge Sharing.
- Automatic OS Migration.

### Success Criteria

- `Start Project: X` תמיד עובר דרך Runtime Entry Gateway.
- Duplicate Project מזוהה לפני יצירה.
- Project Instance נוצר עם Project ID ו־OS Version.
- Project State נוצר במצב קנוני.
- Discovery מתחיל דרך Lifecycle Orchestrator.
- תגובת המשתמש עוברת דרך Phase Guidance Contract.
- לא ניתן לבצע Coding/Execution משמעותי לפני המסלול המאושר.

## 10. Risks

| Risk | Severity | Mitigation |
|---|---:|---|
| Platform אינו מאפשר Interception מלא | Major | להשתמש ב־Runtime חיצוני/מקומי כ־Gateway מחייב |
| כפילות בין Chat Context ל־Runtime State | Major | State Adapter יחיד ו־Source of Truth ברור |
| Runtime הופך ל־Orchestrator נוסף | Major | להגדיר Runtime Orchestrator כיישום ההפעלה של ה־Project Orchestrator, לא כבעלות חדשה |
| עלות פיתוח גבוהה | Medium | להתחיל ב־Minimal Slice בלבד |
| שינוי OS שובר Project Instance | Major | Version Binding, Compatibility Assessment ו־Rollback |
| יותר מדי Gates | Medium | Risk-Based Execution Gate ו־Minimum Necessary Process |
| כשל Client יוצר עקיפה | Major | Fail-Closed לכל בקשות Project Management ללא Runtime |
| Registry לא עקבי עם State | Major | Registry אינדקס בלבד, State נשאר מקור האמת המלא |

## 11. Recommendation

המלצה: **Add a Hybrid Runtime Control Plane**.

לא מומלץ להפוך את ChatGPT Project לבקרת האכיפה היחידה. הוא מתאים כ־Workspace/Client, אך אינו מספיק לבדו כדי להבטיח Routing, State Commit ו־Execution Gate.

הארכיטקטורה הקיימת נשמרת. מתווספת שכבת Runtime אחת שמפעילה ואוכפת אותה.

## 12. Approval Criteria

יש לאשר את ההחלטה רק כאשר מוסכם כי:

- Runtime Control Plane הוא שכבת ההפעלה היחידה.
- אין Orchestrator מקביל.
- ChatGPT Project הוא Workspace/Client, לא Project Instance קנוני.
- כל Project Request עובר Gateway.
- Project State מתעדכן רק דרך State Adapter ובעלות Orchestrator.
- Execution Gate מחייב לפני Execution משמעותי.
- Response Renderer הוא הסמכות היחידה לתגובות Phase.
- Minimal Implementation Slice מאושר בנפרד לפני מימוש.

אישור מסמך זה אינו מאשר קוד, Worker חדש, Skill חדש, Automation או בחירת טכנולוגיה ספציפית.
