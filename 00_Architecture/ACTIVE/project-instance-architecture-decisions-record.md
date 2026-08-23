# Project Instance Architecture Decisions Record

**System:** AI Project Operating System  
**Record Status:** Approved  
**Architecture:** Independent Project Instances on Shared Operating System  
**Scope:** Architecture only — no implementation workflow, Workers or automation

## 1. Decision Summary

הוחלט שכל פרויקט חדש יפעל כ־Project Instance עצמאי על גבי AI Project Operating System משותף.

המודל הסופי מבוסס על:

- OS Version Binding היברידי עם גרסת יצירה נעולה ושדרוגים מבוקרים.
- Project Registry קנוני לכל הפרויקטים.
- עדכוני OS שאינם אוטומטיים.
- בידוד מלא של Project Knowledge כברירת מחדל.
- קנוניזציה של מונחי Lifecycle.

## 2. Decision Log

### DEC-PI-001 — OS Versioning Model

**Decision:** Adopt a Hybrid Version Binding Model.

כל Project Instance שומר:

- `os_version_at_creation` — גרסת OS שאושרה בעת יצירת הפרויקט.
- `os_version_current` — הגרסה המאושרת שהפרויקט משתמש בה בפועל.
- `os_upgrade_status` — מצב שדרוג כאשר קיים.

Project Instance משתמש בגרסה הנוכחית המאושרת שלו, ולא בגרסה גלובלית משתנה בזמן אמת.

#### Creation-Time Version

בעת יצירת Project Instance נקבעת גרסת OS התחלתית. היא משמשת כבסיס להשוואת שינויים, תאימות ו־Migration.

#### Upgrade Policy

- פרויקט חדש מתחיל בגרסה הנוכחית המאושרת.
- פרויקט קיים אינו משודרג אוטומטית.
- שדרוג דורש Compatibility Assessment, החלטת Upgrade ואישור לפי רמת ההשפעה.
- ניתן להישאר בגרסה קודמת כאשר שדרוג אינו נדרש או אינו בטוח.

#### Compatibility Handling

כל שינוי OS שמוצע לפרויקט קיים חייב להיבדק לגבי:

- השפעה על Project State.
- השפעה על Lifecycle, Skills, Workers ו־Templates.
- צורך ב־Migration.
- שינויי Output או Contract.

#### Alternatives Considered

- **Snapshot בלבד:** יציב אך מקשה על קבלת שיפורים עתידיים.
- **Reference חי בלבד:** פשוט אך יוצר שינוי לא מבוקר בפרויקטים פעילים.
- **Hybrid:** משלב יציבות עם שדרוג מבוקר.

**Rationale:** Hybrid שומר על יציבות Project Instance ומאפשר Controlled Evolution.  
**Impact:** נדרש בעתיד מנגנון Versioning ו־Compatibility, אך אין צורך באוטומציה בשלב זה.  
**Status:** Approved.

### DEC-PI-002 — Canonical Project Registry

**Decision:** Project Registry יהיה מקור האמת הקנוני לרשימת כל ה־Project Instances.

#### Purpose

- לזהות פרויקטים קיימים.
- למנוע כפילויות.
- לנתב Continue, Status ו־Project Existence Check.
- לספק אינדקס, לא להחליף את Project State של כל פרויקט.

#### Required Fields

```yaml
project_registry_entry:
  project_id: <stable unique id>
  project_name: <name>
  owner: <human owner>
  status: <canonical project status>
  current_phase: <canonical lifecycle phase>
  os_version: <current bound OS version>
  location: <canonical project workspace reference>
  created_date: <date>
  last_activity: <timestamp>
```

#### Source of Truth

Project Registry הוא אינדקס קנוני ברמת מערכת. Project State המלא נשאר מקור האמת של הפרויקט עצמו. Registry אינו מכיל את כל Project Knowledge, Decisions או Evidence.

#### Alternatives Considered

- חיפוש בכל תיקיות הפרויקטים: אינו יציב ואינו מספיק למניעת כפילויות.
- Registry בתוך כל Project Instance: אינו מאפשר אינדקס גלובלי.
- Registry מרכזי: מאפשר איתור וניתוב תוך שמירה על הפרדת State.

**Rationale:** נדרש מקור אמת אחד לגילוי וניתוב Projects.  
**Impact:** מימוש עתידי יידרש, אך מבנה טכני אינו מוגדר ברשומה זו.  
**Status:** Approved.

### DEC-PI-003 — Controlled OS Update Propagation

**Decision:** OS changes do not propagate automatically to existing Project Instances.

#### Required Process

כל עדכון OS מועמד לפרויקט קיים רק לאחר:

1. Compatibility Assessment.
2. זיהוי רכיבים מושפעים.
3. קביעת צורך ב־Migration.
4. הצגת Impact ו־Risks.
5. Approval של בעל הסמכות המתאים.
6. עדכון גרסת ה־Project Instance ותיעוד השינוי.

#### Approval Requirements

- שינוי מקומי שאינו משנה Contract: אישור בעל הרכיב או ה־Orchestrator לפי הסמכות הקיימת.
- שינוי שחוצה רכיב או משפיע על התנהגות: Review ואישור מתאים.
- שינוי ארכיטקטוני או System Core: System Owner Approval ותיעוד ב־Decision Log.

#### Rollback Considerations

לפני שדרוג יש לשמר את גרסת ה־OS הקודמת ואת מצב הפרויקט. אם השדרוג פוגע בתאימות או באיכות, ניתן להחזיר את ה־Project Instance לגרסה הקודמת בכפוף לתיעוד ואימות.

#### Alternatives Considered

- עדכון אוטומטי: נדחה בשל סיכון לשינוי בלתי מבוקר.
- חסימת כל עדכון: נדחתה משום שהיא מונעת שיפור.
- עדכון מבוקר לפי צורך: נבחר.

**Rationale:** Controlled Evolution שומרת על יציבות ומאפשרת שיפור.  
**Status:** Approved.

### DEC-PI-004 — Project Knowledge Sharing Model

**Decision:** Project Knowledge remains isolated by default.

#### Project-Specific by Default

- Project Context.
- Project State.
- Goals and Scope.
- Decisions and Approvals.
- Risks, Dependencies and Issues.
- Evidence.
- Documents and Outputs.
- Project History.

#### Eligible for System Promotion

רק מידע מופשט, מזוהה כ־Learning או Improvement Candidate, ושאינו חושף מידע פרויקטלי רגיש, יכול להיות מועמד ל־Learning Knowledge או System Knowledge.

#### Promotion Process

```text
Project Learning
        ↓
Evidence and Review
        ↓
Sanitization / Abstraction
        ↓
Improvement Candidate
        ↓
Approval
        ↓
System Knowledge Update
```

אין להעביר Project Decisions, User Data, Evidence או Project History לפרויקט אחר או ל־System Knowledge ללא אישור מפורש ותהליך מתאים.

#### Alternatives Considered

- שיתוף מלא: נדחה בשל דליפת Context והחלטות.
- בידוד מוחלט: נדחה משום שמונע למידה מערכתית.
- Promotion מבוקר: נבחר.

**Rationale:** מאפשר Learning ללא ערבוב בין Projects.  
**Status:** Approved.

### DEC-PI-005 — Canonical Lifecycle Naming

**Decision:** Use the following canonical terminology:

| Term | Canonical Meaning |
|---|---|
| **Validation** | פעילות או שלב שבודק מידע, תוצר, Assumption, Risk או תנאי קבלה. |
| **Review** | מנגנון בקרה רוחבי, במיוחד לפני מעבר משמעותי; אינו בהכרח Phase עצמאי. |
| **Learning** | שלב/פעילות שבהם לוכדים Project Learnings ו־Lessons Learned. |
| **Improvement** | תהליך הפיכת Learning או Observation לשיפור מערכת מבוקר. |
| **Completed** | ערך קנוני של `current_status.status` המציין שהפרויקט או העבודה הושלמו. |

#### Alignment Rules

- `Validation` אינו שם נרדף ל־Review.
- `Review` הוא Gate או פעילות בקרה, בעוד `Validation` בודק אמיתות, תוצרים או תנאים.
- `Learning` מתייחס ללמידה מהפרויקט.
- `Improvement` מתייחס להתפתחות המערכת או לתהליך שיפור מאושר.
- `Completed` נשאר Status קנוני ולא Phase.
- Project State ממשיך להשתמש בשדות הקנוניים `current_status.current_phase` ו־`current_status.status`.

#### Alternatives Considered

- שימוש ב־Review כ־Phase קבוע: נדחה כי Review הוא רוחבי.
- איחוד Learning ו־Improvement: נדחה כי Learning הוא ידע ו־Improvement הוא שינוי מבוקר.
- שימוש ב־Completed כ־Phase: נדחה כי הוא Status.

**Rationale:** מונחים נפרדים מונעים ערבוב בין בדיקה, למידה, שינוי וסיום.  
**Status:** Approved.

## 3. Final Architecture Rules

1. כל Project Instance עצמאי ומבודד כברירת מחדל.
2. AI Project Operating System משותף, אך אינו מחזיק את כל Project State בתוך State גלובלי אחד.
3. כל Project Instance קשור לגרסת OS מאושרת.
4. שינוי OS אינו מתפשט אוטומטית לפרויקטים קיימים.
5. Project Registry הוא מקור האמת לגילוי ואינדוקס Projects.
6. Project State הוא מקור האמת המלא למצב של Project Instance.
7. Project Knowledge אינו משותף אוטומטית.
8. Promotion ל־System Knowledge דורש Evidence, Review, Abstraction ואישור.
9. `Review`, `Validation`, `Learning`, `Improvement` ו־`Completed` נשמרים כמונחים בעלי משמעות נפרדת.
10. אין שינוי מערכת, Workflow או הרשאה טכנית הנגזרים אוטומטית מרשומה זו.

## 4. Implementation Constraints

רשומה זו מגדירה החלטות ארכיטקטוניות בלבד. לפני מימוש יש לשמור על האילוצים הבאים:

- אין ליצור Project Instance ללא Project Existence Check.
- אין לשנות את Canonical State Model ללא החלטה נפרדת.
- אין להפעיל OS Upgrade ללא Compatibility Assessment ואישור.
- אין לשתף Project Knowledge ללא Promotion מבוקר.
- אין להוסיף Automation, Workers או APIs כחלק מהחלטות אלה.
- אין לשנות Project Data קיים כתוצאה מאישור הרשומה בלבד.

## 5. Open Items Remaining

החלטות הארכיטקטורה הושלמו. פריטי מימוש עתידיים שנותרו:

- הגדרת Schema טכני ל־Project Registry.
- בחירת מנגנון Versioning בפועל.
- הגדרת Migration ו־Rollback Workflow.
- הגדרת פורמט שיתוף ידע והסרת מידע רגיש.
- מיפוי גרסאות OS לפרויקטים פעילים.

פריטים אלה אינם פתוחים ברמת ההחלטה הארכיטקטונית; הם יטופלו בשלבי מימוש ייעודיים.

## 6. Approval Recommendation

המלצה: **Approved**.

רשומת החלטות זו יכולה לשמש בסיס ארכיטקטוני רשמי למימוש Project Instance Creation בעתיד.

האישור אינו מאשר עדיין Workflow מימוש, אוטומציה, APIs, הרשאות טכניות או שינויי Project State.
