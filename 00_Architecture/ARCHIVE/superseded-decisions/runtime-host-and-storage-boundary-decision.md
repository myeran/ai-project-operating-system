# Runtime Host and Storage Boundary Decision Document

**System:** AI Project Operating System  
**Status:** Proposed for Approval  
**Scope:** Initial Runtime Control Plane boundaries  
**Related:** `runtime-control-plane-architecture-decision.md`, `runtime-contract-decision.md`

## 1. Decision Summary

ההחלטה המוצעת היא:

- **Runtime Model:** Hybrid.
- **Initial Runtime Host:** Local Runtime בתוך סביבת Codex/מחשב המשתמש.
- **Clients:** ChatGPT Project, Codex או Client נתמך אחר.
- **Registry / State / Audit:** Local SQLite כ־Runtime Metadata Store.
- **Project Documents / Evidence / Outputs:** Filesystem של Project Instance.
- **OS Knowledge:** הקבצים הקנוניים של AI Project Operating System, כ־References לקריאה.
- **Project Instance:** ישות לוגית עצמאית, שאינה זהה ל־ChatGPT Project.

הבחירה שומרת על Control Plane אמיתי, תוך שמירה על פשטות של MVP והימנעות מתשתית Cloud מוקדמת.

## 2. Runtime Host Analysis

### Option A — ChatGPT Project as Runtime Host

#### Advantages

- חוויית משתמש טבעית.
- הקשר קיים וזמין.
- ניסוי מהיר ללא הקמת תשתית.

#### Limitations

- אין אכיפה מובטחת של Gateway.
- קשה למנוע תגובות ישירות מתוך Chat Context.
- אין בעלות ברורה על State Commit ו־Audit.
- קשה להבטיח Execution Gate.

#### Decision

לא מתאים כ־Runtime Authority יחיד. מתאים כ־Workspace או Client.

### Option B — Local Runtime / Codex Host

#### Advantages

- שליטה טובה ב־Gateway וב־Routing.
- גישה ישירה ל־Filesystem ול־SQLite.
- מתאים ל־MVP יחיד ול־Pilot.
- מאפשר Fail-Closed ו־Version Check.

#### Limitations

- תלות במחשב ובסביבת המשתמש.
- אין זמינות מרובת משתמשים כברירת מחדל.
- דורש חיבור מוגדר בין Client ל־Runtime.

#### Decision

מתאים כ־Initial Runtime Host.

### Option C — External Runtime Service/API

#### Advantages

- שליטה מלאה ונקודת כניסה מרכזית.
- תמיכה עתידית בלקוחות ובמשתמשים רבים.
- אפשרות ל־Availability ו־Scaling.

#### Limitations

- עלות פיתוח, אבטחה ותפעול.
- דורש Infrastructure מוקדם.
- עלול להרחיב את ה־MVP מעבר לצורך.

#### Decision

יידחה לשלב עתידי לאחר הוכחת ה־Minimal Slice.

### Option D — Hybrid Runtime

ChatGPT/Codex הם Clients; Runtime מקומי או חיצוני הוא Control Authority; Storage נפרד מה־Execution.

#### Advantages

- חוויית משתמש גמישה.
- הפרדה בין Client לבין Control Plane.
- אפשרות להחליף Host בעתיד.
- שומר על Project Instance ועל Source of Truth עצמאיים.

#### Risks

- דורש פרוטוקול חיבור ברור.
- Client לא מחובר עלול לעקוף את ה־Gateway.
- קיימת עלות תיאום בין שכבות.

#### Decision

נבחר כמודל הארכיטקטוני. ה־Local Runtime הוא ה־Control Authority הראשון.

## 3. Recommended Runtime Model

```text
ChatGPT Project / Codex / Client
              ↓
Local Runtime Gateway
              ↓
Runtime Control Plane
              ↓
SQLite Metadata Store + Project Filesystem
```

### Conditions

- Client שאינו עובר דרך Runtime Gateway אינו נחשב Runtime נתמך.
- בקשות Project Management ללא Gateway נכשלות או מסומנות Non-Enforcing.
- Runtime Orchestrator הוא Runtime Adapter של Project Orchestrator Agent, לא Orchestrator נוסף.
- Storage אינו מבצע החלטות Lifecycle; הוא מספק Persistence ו־Concurrency Control בלבד.

## 4. Storage Boundary

### 4.1 Project Registry

#### Purpose

Project Registry הוא מקור האמת לאינדקס כל ה־Project Instances ול־Project Existence Check.

#### Storage

ה־MVP ישמור את Registry ב־SQLite, בטבלה קנונית אחת או במבנה שקול.

#### Required Fields

```yaml
project_registry_entry:
  project_id: <stable unique id>
  project_name: <name>
  owner: <human owner>
  status: <canonical status>
  current_phase: <canonical phase>
  os_version: <bound OS version>
  location: <canonical project workspace reference>
  created_date: <date>
  last_activity: <timestamp>
```

#### Ownership

- Runtime Resolver קורא.
- Bootstrap מציע Entry חדש.
- Registry Adapter מאמת ומבצע Commit.
- Orchestrator מנהל את ההחלטה התפעולית.
- System Owner אחראי על כללי Registry ברמת OS.

### 4.2 Project State

#### Storage Location

Project State נשמר ב־SQLite כ־Canonical Runtime State, עם אפשרות לייצוא/גיבוי לקובץ קריא.

Project Documents, Evidence ו־Outputs נשמרים ב־Project Instance Filesystem. הם אינם מחליפים את State.

#### Read Authority

- State Adapter קורא את ה־Canonical State.
- Runtime Orchestrator מקבל Snapshot.
- Skills ו־Workers מקבלים Context רלוונטי בלבד.

#### Write Proposal Authority

- Orchestrator, Skills ו־Workers רשאים להציע עדכונים לפי Scope.
- Human Owner מאשר Goals, Scope משמעותי והחלטות אסטרטגיות.

#### Commit Authority

State Adapter הוא גבול ה־Persistence וה־Commit הטכני. Commit דורש:

- Project ID.
- Expected Version.
- New Version.
- Actor.
- Timestamp.
- Source Task או Decision.
- Audit Record.
- Validation ואישור לפי הצורך.

### 4.3 Audit History

Audit נשמר ב־SQLite, בנפרד מה־Project State אך מקושר אליו.

נשמרים:

- State Changes.
- Phase Transitions.
- Decisions.
- Approvals.
- Execution Authorizations.
- Blocks ו־Escalations.
- Version Conflicts.
- OS Version Binding או Upgrade Decisions.

Audit הוא Evidence תפעולי ואינו מחליף את Canonical State.

## 5. Development Phase Storage

### Options Evaluation

| Option | Benefit | Limitation | Decision |
|---|---|---|---|
| Local Files | פשוט, קריא, Git-friendly | Concurrency ו־Atomic Commit חלשים | מתאים למסמכים, לא כ־State Authority יחיד |
| SQLite | Atomic Commit, Version Checks, Query ו־Audit | דורש Adapter וגיבוי | נבחר ל־Registry/State/Audit |
| External Database | Scaling ו־Multi-user | מורכב מדי ל־MVP | נדחה |
| Cloud Storage | נגישות ושיתוף | תלות, הרשאות ו־Latency | נדחה |

### MVP Decision

- **SQLite:** Registry, Canonical Project State, Audit ו־Version Metadata.
- **Filesystem:** Project Context, Knowledge, Evidence, Outputs ו־Human-readable exports.
- **OS Files:** System Knowledge ו־Contracts במקור האמת הרשמי.

הבחירה נועדה לספק Atomicity ו־Versioning מינימליים בלי להקים שירות חיצוני.

## 6. Client Relationship Model

### ChatGPT Project

ChatGPT Project הוא Workspace/Client Context. הוא אינו Project Instance קנוני ואינו מחזיק לבדו את Source of Truth.

### Codex

Codex הוא Client/Execution Environment אפשרי שיכול לתקשר עם Runtime מקומי, לקרוא Project Files ולבצע פעולות רק לאחר Authorization.

### Runtime Control Plane

ה־Runtime הוא Control Authority עבור:

- Request Routing.
- Project Resolution.
- State Loading.
- Lifecycle Decision.
- Execution Authorization.
- State Commit.
- User Response Rendering.

### Project Instance

Project Instance הוא ישות לוגית עם Project ID, Registry Entry, Project State, Knowledge, Evidence, Outputs ו־OS Version Binding.

## 7. Runtime Connection Flow

```text
User
  ↓
ChatGPT Project / Codex / Supported Client
  ↓
Runtime Gateway
  ↓
Request Validation
  ↓
Project Resolver → SQLite Registry
  ↓
State Adapter → SQLite Project State
  ↓
Runtime / Project Orchestrator
  ↓
Bootstrap or Discovery Activation
  ↓
State Proposal
  ↓
Validation and Commit → SQLite + Audit
  ↓
Response Renderer
  ↓
Client / User
```

### Authentication Needs — MVP

אין להקים מערכת הרשאות מורכבת בשלב הראשון. נדרש לכל הפחות:

- Client Identity.
- User Identity או User Reference.
- Request ID ו־Correlation ID.
- זיהוי Runtime מקומי מהימן.
- חסימת Client לא מזוהה.

הרשאות מלאות, Multi-user ו־External Authentication יוגדרו בעתיד אם יהיה צורך.

### Context Loading

Runtime טוען לפי הרלוונטיות:

- OS Version Reference.
- Project Registry Entry.
- Project State Snapshot.
- Project Knowledge רלוונטי.
- Current Phase ו־Required Outputs.

אין לטעון את כל ה־OS או את כל Project Knowledge כברירת מחדל.

## 8. MVP Implementation Boundary

### Included

```text
Start Project
        ↓
Runtime Gateway
        ↓
Create / Resolve Instance
        ↓
Bootstrap
        ↓
SQLite Registry + State Initialization
        ↓
Discovery דרך Orchestrator
        ↓
Phase Guidance Response
```

### Required

- Local Runtime Host.
- Runtime Request/Response Contracts.
- SQLite Registry Adapter.
- SQLite State Adapter.
- SQLite Audit Adapter.
- Bootstrap Loader.
- Orchestrator Runtime Adapter.
- Discovery Invocation Boundary.
- Response Renderer.

### Excluded

- Full Automation.
- Advanced Integrations.
- Multi-Agent Systems.
- Complex Permissions.
- Cloud Deployment.
- Multi-user Scaling.
- Production Code Execution.
- Automatic OS Updates.

## 9. Risks

| Risk | Severity | Mitigation |
|---|---:|---|
| Local Runtime תלוי במחשב יחיד | Major | גיבוי SQLite וייצוא Files; מעבר עתידי ל־Service |
| ChatGPT/Codex עוקפים Gateway | Blocking | Non-Enforcing Client אינו רשאי לבצע Project Actions |
| SQLite גדל מעבר ל־MVP | Future | להגדיר Adapter כך שניתן יהיה להחליף Storage |
| State ו־Filesystem אינם מסונכרנים | Major | State כמקור האמת; Artifacts מקושרים דרך Knowledge Records |
| מעבר עתידי מ־SQLite ל־DB | Medium | לא לחשוף Storage ישירות ל־Orchestrator |
| Authentication חלש | Major | Client/User Identity מינימליים ו־Fail-Closed |
| Runtime Host לא מתאים | Major | להוכיח Interception ב־Smoke Test לפני הרחבה |

## 10. Final Recommendation

לאשר את ההחלטה הבאה:

> להתחיל את Minimal Runtime Slice במודל Hybrid, עם Local Runtime/ Codex Host כ־Control Authority, SQLite ל־Registry/State/Audit, ו־Filesystem לתוצרי Project Instance.

ChatGPT Project יישאר Workspace/Client ולא Project Instance או מקור אמת עצמאי.

הבחירה מספקת את האיזון הנכון בין שליטה, פשטות ויכולת מעבר עתידית ל־External Runtime Service.

## 11. Approval Criteria

יש לאשר לפני מימוש כאשר מוסכם כי:

- Local Runtime הוא Host ה־MVP.
- ChatGPT/Codex הם Clients בלבד.
- SQLite הוא Storage Authority ל־Registry, State ו־Audit.
- Filesystem משמש למסמכים, Evidence ו־Outputs.
- Project State אינו מנוהל ישירות מתוך Chat Context.
- Client ללא Gateway אינו Runtime נתמך.
- State Commit עובר Version Check, Actor, Timestamp ו־Audit.
- Minimal Slice אינו כולל Code Execution או Automation.
- Storage Adapter מאפשר החלפה עתידית של SQLite.

אישור מסמך זה אינו מאשר קוד, תשתית, בחירת ספרייה או Deployment.
