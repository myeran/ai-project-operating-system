# Phase 0.5 — System Contracts & Canonical State Model

**System:** AI Project Operating System  
**Architecture:** Orchestrator-Centered Layered Hybrid Architecture  
**Status:** Completed — Approved  
**Current Phase:** Phase 0.5 — System Contracts & Canonical State Model

## מטרת המסמך

להגדיר חוזי עבודה, בעלות על מידע, מודל מצב וכללי מעבר אחידים לכל רכיבי המערכת. המסמך הוא חוזה ארכיטקטוני; הוא אינו מגדיר עדיין DNA, Skills מפורטים או Templates.

## 1. Worker / Skill Contract

### 1.1 Skill Definition

כל Skill או Expert Worker חייב להצהיר על:

| שדה | דרישה |
|---|---|
| Skill Name | שם ייחודי ויציב |
| Purpose | הבעיה או הערך שה־Skill מספק |
| Responsibility | סוגי העבודה שבאחריותו |
| Scope | גבולות העבודה ומה אינו כלול |
| Version | גרסת החוזה או היכולת |
| Dependencies | ידע, Skills או כלים נדרשים |

### 1.2 Input Contract

ה־Orchestrator מעביר ל־Skill חבילת הקשר הכוללת, לפי הרלוונטיות:

- Project Context — תיאור הפרויקט, בעלי עניין והקשר עסקי.
- Current Phase — שלב ומצב נוכחיים.
- Goals — מטרות ותוצאות רצויות.
- Constraints — Scope, זמן, תקציב, מדיניות והרשאות.
- Existing Knowledge — מסמכים, תוצרים, סיכונים והיסטוריה רלוונטיים.
- Previous Decisions — החלטות ואישורים קודמים.
- Task Request — השאלה או התוצר הנדרש.
- Expected Output — פורמט ותנאי קבלה לתוצר.

Skill אינו רשאי להניח שהקשר חסר הוא עובדה. עליו לסמן שדות חסרים או לא ודאיים.

### 1.3 Execution Rules

#### Skill רשאי

- לנתח את הקלט שבתחום אחריותו.
- להפיק Findings, Analysis, Recommendations ותוצרי תחום.
- לזהות סיכונים, תלותים, חוסרים והחלטות נדרשות.
- להשתמש בכלים שאושרו עבורו וב־Scope שהוגדר.
- להציע שינוי או פעולה להחלטת ה־Orchestrator.

#### Skill אינו רשאי

- לשנות Phase, Status, Scope או מטרות באופן עצמאי.
- לאשר החלטה אסטרטגית, משפטית או כספית.
- לאשר Gate קריטי.
- לעקוף את ה־Orchestrator או לכתוב מצב קנוני ללא הרשאה מפורשת.
- להציג הנחה או המלצה כעובדה מאושרת.
- להפעיל Worker נוסף ללא אישור והקשר שהוגדרו.

#### Skill חייב לעצור ולהסלים כאשר

- חסר מידע קריטי לביצוע אמין.
- יש סתירה בין מקורות או הוראות.
- המשימה חורגת מה־Scope או מההרשאות.
- נדרשת החלטה אנושית.
- התוצאה עלולה ליצור שינוי בלתי הפיך או סיכון מהותי.

### 1.4 Output Contract

כל Skill מחזיר תשובה במבנה הבא:

~~~yaml
skill:
  name: <Skill Name>
  version: <Version>
  task_id: <Task ID>
status: completed | partial | blocked | escalated
findings: []
analysis: []
recommendations: []
decisions_required: []
risks: []
dependencies: []
created_artifacts: []
assumptions: []
uncertainties: []
next_steps: []
handoff:
  requested_orchestrator_action: <action>
  state_updates_proposed: []
~~~

כל פריט משמעותי צריך לכלול מקור או סימון מפורש שהוא ניתוח, הנחה או המלצה. ה־Orchestrator מאמת את הפלט לפני שילובו במצב הקנוני.

## 2. Skill Lifecycle

1. Activation — ה־Orchestrator מזהה צורך, בוחר Skill, יוצר Task ID ומגדיר תוצר מצופה.
2. Context Loading — ה־Skill מקבל את Input Contract ואת המידע הרלוונטי בלבד.
3. Execution — ה־Skill מבצע ניתוח או עבודה בתחום האחריות וההרשאות שלו.
4. Output Generation — ה־Skill מחזיר את Output Contract, כולל אי־ודאות וסיכונים.
5. Validation — ה־Orchestrator בודק שלמות, התאמה ל־Scope, מקורות, סתירות ותנאי קבלה.
6. Handoff back to Orchestrator — הפלט נמסר ל־Orchestrator; רק הוא מחליט אם לעדכן מצב, ליצור תוצר או להסלים.

כשל בכל שלב עוצר את המעבר האוטומטי ומייצר סטטוס blocked או escalated.

## 3. Canonical State Model

Project State הוא הרשומה הקנונית היחידה המתארת את מצב הפרויקט בזמן נתון. מסמכים, Notes, Logs ותוצרי Skill אינם מחליפים אותו.

~~~yaml
project_state:
  project_identity:
    project_id: <stable unique id>
    name: <name>
    description: <description>
    owner: <human owner>
    stakeholders: []
  current_status:
    current_phase: <lifecycle phase>
    status: proposed | active | blocked | awaiting_approval | completed | cancelled
    progress: <0-100 or defined scale>
    blockers: []
  planning_data:
    goals: []
    scope:
      in_scope: []
      out_of_scope: []
      change_history: []
    timeline: {}
    resources: []
  decision_management:
    decisions: []
    pending_decisions: []
    approvals: []
  risk_management:
    risks: []
    dependencies: []
    issues: []
  knowledge:
    documents: []
    outputs: []
    lessons_learned: []
  next_actions:
    tasks: []
    owners: []
    due_dates: []
  audit:
    last_updated_at: <timestamp>
    last_updated_by: <actor>
    version: <monotonic version>
    history_ref: <history reference>
~~~

### כללי תקינות למודל

- project_id יציב ואינו משתנה במהלך חיי הפרויקט.
- לכל Project State יש Version ו־History.
- status ו־current_phase חייבים להיות ערכים מוכרים.
- אין לעדכן שדה ללא Actor, Timestamp והקשר למשימה או החלטה.
- שדות חסרים, לא מוכרים או סותרים אינם מקודמים למצב קנוני.

## 4. State Ownership

| תחום מידע | בעלים מעדכן | אחרים רשאים |
|---|---|---|
| Phase, Status, Workflow | Orchestrator | להציע שינוי בלבד |
| Goals ו־Scope | Human Owner | Orchestrator ו־Skills מציעים |
| Timeline, Resources, Tasks | Orchestrator במסגרת אישור | Workers מדווחים ביצוע |
| Findings ו־Analysis | Skill המתאים | Orchestrator מאמת ומשלב |
| Recommendations | Skill / Orchestrator | Human Owner מאשר החלטה |
| Strategic Decisions | Human Owner | Orchestrator מתעד ומציג חלופות |
| Approvals | Human Owner | Orchestrator מתעד |
| Risks, Dependencies, Issues | Orchestrator; Skills מציפים | כל רכיב רשאי להציע |
| Documents ו־Outputs | Orchestrator או Worker מורשה | Skill יוצר הצעה או תוצר בתחום |
| Lessons Learned | Orchestrator | כל רכיב רשאי להציע |
| Rules, DNA, Registry | System Owner בתהליך מבוקר | Orchestrator מציע שינוי |

## 5. State Transition Rules

### 5.1 עקרונות

- מעבר מצב מתבצע רק על ידי ה־Orchestrator, או באמצעות אישור אנושי במקום שהוגדר.
- כל מעבר דורש תנאי כניסה, Required Outputs, בדיקת חסמים ורישום ב־History.
- כשל באימות מוביל ל־blocked או awaiting_approval; אין מעבר שקט.
- ניתן לחזור לשלב קודם כאשר Validation מזהה פער, תוך תיעוד סיבת החזרה.

### 5.2 Lifecycle Transition Map

| מעבר | תנאי מעבר | Required Outputs | אישור |
|---|---|---|---|
| Proposed → Discovery | קיימת בקשת פרויקט מזוהה | Project Identity, שאלת עבודה ראשונית | לא נדרש |
| Discovery → Strategy | הבעיה, המשתמשים, בעלי העניין והמטרות מובנים | Discovery Findings, Goals, Open Questions | Human Owner מאשר מטרות |
| Strategy → Planning | כיוון, ערך וסדרי עדיפויות מוגדרים | Strategy Summary, Decision Log, Risks | אישור אסטרטגי |
| Planning → Design | Scope, משאבים, זמן ותלותים מוגדרים | Project Plan, Scope, Risk Register | אישור Scope משמעותי |
| Design → Execution | פתרון או תכנון מספיקים לביצוע | Design Output, Acceptance Criteria | לפי Gate |
| Execution → Validation | תוצרי הביצוע זמינים לבדיקה | Execution Outputs, Updated Tasks | לא בהכרח |
| Validation → Launch | התוצר עומד בתנאי הקבלה ואין חסם קריטי | Validation Report, Open Issues | אישור Launch אם נדרש |
| Launch → Improvement | ההשקה הושלמה והמדידה פעילה | Launch Record, Metrics Setup | בעל הפרויקט |
| Improvement → Completed | היעדים והסגירה הושלמו | Lessons Learned, Closure Summary | בעל הפרויקט |

### 5.3 מצבי חסימה והסלמה

- כל שלב יכול לעבור ל־blocked כאשר אין אפשרות להתקדם בבטחה.
- blocked מחייב Blocker, Owner, Next Review או Decision Needed.
- awaiting_approval משמש כאשר התוצר מוכן אך חסרה החלטה או חתימה אנושית.
- cancelled מחייב סיבת ביטול ותיעוד החלטת בעל הפרויקט.

## 6. Open Questions

### החלטות חסרות

- האם progress יהיה אחוז רציף, מדד שלבים או שילוב ביניהם.
- מהו פורמט האישור האנושי המחייב והיכן נשמר בפועל.
- מי מוגדר System Owner המאשר שינויי DNA, Rules ו־Registry.
- האם יש לאפשר מספר Workstreams במקביל בתוך Project State אחד.
- מהם תנאי הקבלה המדויקים לכל Gate.

### סיכונים

- עדכונים מקבילים עלולים ליצור Race Conditions או דריסת מידע.
- Skills עלולים להחזיר תוצרים תקינים חלקית ללא סימון ברור.
- שינויי Scope עלולים להיכנס דרך מסמכים במקום דרך State קנוני.
- מודל סטטוס גמיש מדי עלול לפגוע בעקביות בין פרויקטים.

### המלצות

1. לאשר את החוזה ואת Project State כמקורות קנוניים.
2. להגדיר Schema פורמלי ו־Validation Rules לפני מימוש.
3. להגדיר מנגנון Versioning ו־Concurrency לעדכוני מצב.
4. להגדיר Gate Criteria מפורטים בשלב Process Layer.
5. רק לאחר מכן לחזור לבניית Phase 1 — System Foundation / Agent DNA.

## 7. Phase 0.5 Completion Check

- **Worker/Skill Contract:** מוגדר ומאושר.
- **Canonical State Model:** מוגדר ומאושר.
- **State Ownership:** מוגדר.
- **State Transition Rules:** מוגדרים ברמת־על.
- **Phase 0.5:** Completed.

## 8. Approval Record

- **Approval:** אושר על ידי בעל הפרויקט / המשתמש הראשי.
- **Scope:** Worker/Skill Contract, Canonical State Model, State Ownership ו־State Transition Rules.
- **Date:** 2026-08-18.
