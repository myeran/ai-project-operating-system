# Project Instance Architecture Decision

**System:** AI Project Operating System  
**Decision Status:** Proposed for Approval  
**Architecture:** Independent Project Instances on Shared Operating System  
**Source of Truth:** `AI Project Operating System/`

## 1. Decision Summary

כל פרויקט חדש נוצר כ־**Project Instance** עצמאי המשתמש ב־AI Project Operating System כתשתית משותפת.

ה־Operating System מספק Frameworks, Lifecycle, Skills, Workers, Templates, Contracts, Governance ו־Continuous Improvement. כל Project Instance מחזיק את ההקשר, המצב, הידע, ההחלטות, הראיות והתוצרים הייחודיים שלו.

העיקרון המרכזי:

```text
Shared Operating System
          ↓
Independent Project Instance
          ↓
Project Execution and Knowledge
```

## 2. System Layers

### 2.1 AI Project Operating System Layer

שכבה גלובלית ומשותפת לכל הפרויקטים.

כוללת:

- Architecture and System Contracts.
- Agent DNA and System Core.
- Lifecycle Framework.
- Quality and Review Frameworks.
- Skills Registry and Skill Contracts.
- Worker Operating Model and Worker Definitions.
- Templates.
- Governance and Decision Rules.
- Knowledge Structure and Source of Truth Rules.
- Continuous Improvement Framework.

#### אחריות

- להגדיר כיצד פרויקטים מתנהלים.
- לספק יכולות, חוזים ותבניות משותפים.
- לשמור על עקביות בין פרויקטים.
- לאשר ולבקר שינויים מערכתיים.
- ללמוד מפרויקטים ולשפר רכיבים משותפים באופן מבוקר.

#### מה גלובלי ומשותף

כללים, הגדרות, Contracts, Skills, Workers, Templates, Lifecycle ו־Governance. שינויים בשכבה זו עשויים להשפיע על פרויקטים עתידיים ולעיתים על פרויקטים פעילים, ולכן נדרשים Review ואישור לפי ההשפעה.

### 2.2 Project Instance Layer

שכבה מבודדת לכל פרויקט.

כוללת:

- Project Context.
- Canonical Project State.
- Project Knowledge.
- Project Decisions and Approvals.
- Project Risks, Dependencies and Issues.
- Project Evidence.
- Project Outputs and Artifacts.
- Project Tasks, Owners and Due Dates.
- Project History and Lessons Learned.

#### אחריות

- לשמור את המציאות וההחלטות של הפרויקט.
- לאפשר ל־Orchestrator לנהל את הפרויקט לפי ה־Lifecycle.
- לשמור הפרדה בין מידע פרויקטלי לבין ידע מערכת.
- לספק Context רלוונטי ל־Skills ול־Workers.

### 2.3 Execution Layer

שכבת ההפעלה היומיומית של Project Instance.

כוללת:

- Project Agent או Workspace של הפרויקט.
- User Interaction.
- Project Entry Point.
- Project Launcher ו־Lifecycle Orchestrator.
- Worker Execution.
- Skill Activation.
- שימוש ב־Templates וב־Project Knowledge.

#### אחריות

- לקבל בקשות משתמש.
- לטעון את Project State וה־Context הרלוונטיים.
- להפעיל Skills ו־Workers מתוך היכולות המשותפות.
- להחזיר תוצרים והנחיות דרך חוזי הפלט הקיימים.
- לעדכן את Project Instance דרך ה־Orchestrator בלבד.

## 3. Inheritance Model

כל Project Instance מקבל Reference או גישה מבוקרת ליכולות ה־Operating System. הוא אינו מקבל עותק עצמאי של סמכות המערכת.

### Inherited from the Operating System

- Lifecycle Rules.
- Available Skills.
- Worker Definitions.
- Templates.
- Input and Output Contracts.
- Decision and Escalation Rules.
- Quality and Review Rules.
- Source of Truth Rules.
- Continuous Improvement Rules.

היכולות המורשות מופעלות לפי סוג הפרויקט, ה־Phase, רמת הסיכון והצורך בפועל. אין להפעיל את כל היכולות כברירת מחדל.

### Not Inherited

Project Instance אינו מקבל:

- Project Knowledge של פרויקטים אחרים.
- Project Decisions או Approvals של פרויקטים אחרים.
- Project Data או Evidence של פרויקטים אחרים.
- Project History או Lessons ייחודיים של פרויקט אחר.
- סמכות לשנות את ה־Operating System.

#### Reason

הפרדה זו מונעת דליפת מידע, ערבוב החלטות, זיהום Context והסקת מסקנות שגויות מפרויקט אחד לאחר. Lessons ו־Best Practices יכולים להפוך לידע מערכת רק דרך Continuous Improvement, Review ואישור.

## 4. Project Creation Model

יצירת Project Instance מתבצעת ברמה ארכיטקטונית כך:

```text
Project Request
        ↓
Project Existence Check
        ↓
Create Project Instance Identity
        ↓
Initialize Canonical Project State
        ↓
Attach Shared OS Capabilities
        ↓
Start Discovery
        ↓
Operate Through Lifecycle
```

### Creation Principles

- לכל Project Instance יש `project_id` יציב וייחודי.
- כל Project Instance מתחיל ב־`current_phase: Discovery`.
- סטטוס התחלתי משתמש בערך הקנוני `proposed`.
- Project Owner ובעלי עניין נשמרים ברמת הפרויקט.
- Project State נוצר לפי המודל הקנוני הקיים בלבד.
- Project Workspace נוצר לפי Minimum Necessary Process.
- אין להעתיק ידע מפרויקט אחר ללא בחירה מפורשת, מקור ואישור מתאים.

## 5. Project Isolation Model

### Isolated by Default

הפריטים הבאים מבודדים לחלוטין בין Projects:

- Project State.
- Goals and Scope.
- Decisions and Approvals.
- Risks and Dependencies.
- Documents and Outputs.
- Evidence.
- Tasks and Owners.
- Project History.

### Shared by Default

הפריטים הבאים משותפים דרך ה־Operating System:

- Frameworks.
- Skills and Contracts.
- Worker Definitions.
- Templates.
- Governance Rules.
- Output Contracts.

### Controlled Knowledge Promotion

ידע מפרויקט יכול להפוך ל־Learning Knowledge או System Improvement Candidate, אך אינו משנה את ה־Operating System אוטומטית:

```text
Project Learning
        ↓
Review and Evidence
        ↓
Improvement Candidate
        ↓
Approval
        ↓
System Knowledge Update
```

## 6. Runtime and Authority Model

### Project Entry Point

מקבל כל בקשה הקשורה לפרויקט ומזהה Intent. אין תגובה ישירה מתוך Chat Context.

### Project Launcher

יוצר Project Instance חדש רק לאחר Project Existence Check ומאתחל את ה־Project State הקנוני.

### Lifecycle Orchestrator

מנהל את ה־Project Instance ביום־יום:

- קורא Project State.
- מזהה Current Phase.
- מפעיל Skills ו־Workers משותפים.
- מנהל Transitions ו־Guidance.
- משלב תוצרים ב־Project Knowledge וב־Project State.

### Skills and Workers

מבצעים ניתוח או משימה בתחום מוגדר. אין להם סמכות לשנות את ה־Operating System או לקבל החלטות פרויקטליות סופיות.

### Human Owner

מאשר מטרות, Scope משמעותי, החלטות אסטרטגיות, החלטות משפטיות/כספיות ושינויים מערכתיים לפי הסמכות הרלוונטית.

## 7. Project-to-System Interaction

```text
Project Request
        ↓
Project Instance State
        ↓
Relevant OS Context
        ↓
Skill / Worker Execution
        ↓
Validated Project Output
        ↓
Project Knowledge / State Update
        ↓
Learning Candidate, אם רלוונטי
```

ה־Orchestrator טוען רק Context רלוונטי. Project Instance אינו קורא או משנה את כל ה־Operating System ללא צורך והרשאה.

## 8. System Evolution Rules

- שינוי ב־Project Instance נשאר מקומי כברירת מחדל.
- שינוי ב־Operating System דורש Improvement Review ואישור לפי ההשפעה.
- שינוי ארכיטקטוני מתועד ב־Decision Log לאחר אישור.
- עדכון OS אינו מוחק או משנה היסטוריית Project Instance.
- שינוי OS עתידי צריך להגדיר כיצד הוא חל על Projects קיימים וחדשים.
- אין להעתיק Project State בין Projects.

## 9. Architecture Boundaries

### Project Instance אינו

- עותק עצמאי של ה־Operating System.
- מקור אמת ל־Frameworks או Skills.
- בעל סמכות לשנות Rules או Contracts.
- מאגר משותף לפרויקטים אחרים.

### Operating System אינו

- מחזיק את כל פרטי הפרויקטים בתוך State גלובלי אחד.
- מערבב החלטות בין Projects.
- מעביר Project Knowledge אוטומטית בין Projects.
- עוקף את Project Owner בהחלטות פרויקטליות.

## 10. Open Questions

- האם Project Instance יקבל Snapshot או Reference לגרסת OS בזמן יצירתו?
- כיצד יטופלו עדכוני OS עבור פרויקטים פעילים?
- האם ניתן לאשר שיתוף ידע בין שני Projects, ובאיזה פורמט?
- היכן נשמרת רשימת Project Instances הקנונית?
- האם נדרש Project Registry נפרד בעתיד?

## 11. Decision Recommendation

לאשר את מודל **Independent Project Instances on Shared Operating System** כמודל הארכיטקטוני הרשמי, בכפוף להחלטות הפתוחות לגבי Versioning, Project Registry ושיתוף ידע.

אישור מודל זה אינו מאשר עדיין Workflow מימוש, אוטומציה או הרשאות טכניות.
