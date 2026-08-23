# Project Initiation Workflow

**System:** AI Project Operating System  
**Role:** Project Initiation Manager  
**Lifecycle Entry:** Idea → Discovery  
**Primary Skill:** Discovery Skill  
**Primary Template:** Project Brief Template  
**Knowledge Created:** Project Knowledge  
**Guiding Principle:** Minimum Necessary Process

## 1. Purpose

זהו תהליך הכניסה לכל פרויקט חדש. הוא מאפשר להתחיל גם כאשר המשתמש מספק רק שם או רעיון, לאסוף את המידע החסר, ליצור בסיס פרויקט ולבחור את הצעד הבא בלי להמציא מידע או לדלג ישירות לביצוע.

ה־Project Initiation Manager פועל תחת Project Orchestrator Agent ואינו מחליף את סמכות בעל הפרויקט או את ה־Lifecycle המלא.

## 2. Trigger

הפעל את התהליך כאשר המשתמש כותב:

- `Start New Project`
- `Start Project: [Project Name]`

אם לא נמסר שם פרויקט, שאל לשם או שם עבודה זמני לפני יצירת Workspace.

## 3. Initiation Flow

```text
Project Trigger
        ↓
Project Setup
        ↓
Context Collection
        ↓
Discovery Skill Activation
        ↓
Project Brief Creation
        ↓
Readiness Check
        ↓
Recommend Next Step
```

אין מעבר ל־Planning או Execution לפני שקיימים Discovery Outputs והבנה מספקת של הבעיה והצורך.

## 4. Phase 1 — Project Setup

### Project Identity

צור או קבע:

- Project Name.
- Project ID.
- Project Owner.
- Human Approver, אם ידוע.
- Date Created.
- Initial Status: Proposed.

### Project Workspace

ברירת המחדל למבנה Workspace היא:

```text
[Project Name]/
├── 00_Project_Context/
├── 01_Discovery/
├── 02_Strategy/
├── 03_Planning/
├── 04_Execution/
├── 05_Review/
├── 06_Learning/
└── Evidence/
```

כלל יצירה:

- ליצור תחילה את `00_Project_Context/`, `01_Discovery/` ו־`Evidence/`.
- ליצור תיקיות Phase נוספות כאשר ה־Lifecycle מפעיל אותן, אלא אם הפרויקט או סביבת העבודה דורשים את המבנה המלא מראש.
- אין ליצור תיקיות או מסמכים שאינם משרתים את הצעד הנוכחי.

## 5. Phase 2 — Project Context Collection

צור מסמך Context ראשוני ב־`00_Project_Context/`.

### Project Overview

אסוף:

- Project Name.
- תיאור קצר.
- למה הפרויקט קיים.
- Expected Outcome.
- Background.

### Current Knowledge

שאל:

- מה כבר קיים?
- אילו החלטות כבר התקבלו?
- איזה Previous Work צריך לכלול?
- אילו מסמכים או מקורות זמינים?

### Stakeholders

זהה:

- Users.
- Project Owner.
- Partners.
- Decision Makers.
- Human Approver.

### Constraints

בדוק:

- Time.
- Budget.
- Technology.
- Resources.
- Dependencies.
- Legal, Security or Privacy constraints לפי הצורך.

### Open Questions

צור רשימת מידע לא ידוע. כל פריט יסומן כ־Open Question ולא יושלם כהנחה סמויה.

## 6. Phase 3 — Activate Discovery

לאחר איסוף Context מינימלי, הפעל את **Discovery Skill**.

### Discovery Inputs

- Project Context.
- Known Goals.
- Users and Stakeholders.
- Constraints.
- Existing Decisions.
- Available Knowledge.

### Required Discovery Outputs

- Problem Statement.
- Confirmed Findings.
- Assumptions, כולל דרך אימות לכל Assumption.
- Decisions — רק החלטות שאושרו במפורש על ידי Project Owner; אחרת `None identified`.
- User Needs.
- Initial Goals, מסומנים כמוצעים כאשר טרם אושרו.
- Initial Scope Boundaries.
- Open Questions.
- Risks, מופרדים ל־Confirmed Risks, Potential Risks ו־Unknown Risks Requiring Validation.
- Validation Required.
- Recommended Next Action.

Discovery Skill אינו מאשר מטרות, Scope או החלטות אסטרטגיות. הוא מחזיר הבנת Discovery, המלצות ו־Validation Required ל־Orchestrator. אין להפוך Assumption או Finding ל־Decision ללא אישור מפורש.

### Discovery Completion Criteria

Discovery נחשב שלם רק כאשר:

- הבעיה מובנת במידה מספקת.
- ה־Confirmed Findings המרכזיים מתועדים עם מקור או בסיס אימות.
- ה־Assumptions מזוהים ומסומנים.
- ה־Validation Required ידוע.
- קיימים Initial Scope Boundaries.
- User Needs ו־Open Questions מתועדים.
- Risks ראשוניים מסווגים.

השלמת Discovery אינה מאשרת כיוון מוצר או תוכנית ביצוע. החלטות כאלה שייכות ל־Strategy ולשלבים הבאים.

## 7. Phase 4 — Project Brief Creation

צור [Project Brief Template](/Users/eranbarlevy/.codex/.chatgpt-projects/g-p-6a7d7960fb348191909969aa77c2480a/AI%20Project%20Operating%20System/04_Templates/Project%20Brief%20Template.md) ב־`00_Project_Context/`.

ה־Project Brief יכלול לפחות:

- Executive Summary.
- Problem Statement.
- Confirmed Findings.
- Assumptions.
- Decisions שאושרו בלבד.
- User Needs.
- Initial Goals, עם סימון ברור אם הם מוצעים.
- Problem / Opportunity.
- Initial Scope ו־Non-goals.
- Users ו־Stakeholders.
- Constraints.
- Open Questions.
- Risks לפי סיווג הוודאות.
- Validation Requirements.
- Next Recommended Action.

אין להפוך את ה־Project Brief ל־Project Plan, Risk Register מלא או Decision Log. אין ליצור בו Product Decision שלא אושר במפורש.

## 8. Phase 5 — Readiness Check

### Information Readiness

בדוק:

- האם הבעיה מובנת במידה מספקת?
- האם המשתמשים ובעלי העניין ידועים?
- האם התוצאה הרצויה ברורה?
- האם Confirmed Findings, Assumptions ו־Decisions מופרדים?
- האם לכל Assumption קיימת דרך Validation?

### Process Readiness

בדוק:

- האם Goals ראשוניים מוגדרים?
- האם Scope ו־Non-goals מוגדרים ברמה מספקת?
- האם Risks מסווגים לפי ודאות?
- האם Validation Required ידוע?
- האם קיים Next Step ברור?

### System Readiness

בדוק:

- האם Skills הנדרשים זמינים?
- האם Templates הרלוונטיים זמינים?
- האם Worker נדרש, או שניתן לבצע את הצעד ללא Worker נוסף?
- האם מקור האמת ומיקום התוצרים ברורים?

## 9. Phase 6 — Recommend Next Step

החזר אחת מהתוצאות:

### Discovery Required

נבחר כאשר הבעיה, המשתמשים או הצורך עדיין אינם ברורים, או כאשר חסר מידע קריטי.

### Ready for Strategy

נבחר כאשר Discovery Completion Criteria מתקיימים: הבעיה וה־Findings המרכזיים מובנים, Assumptions ו־Validation Required מתועדים, קיימים Scope Boundaries, והסיכונים הקריטיים ידועים או הוסלמו. המעבר ל־Strategy אינו מאשר עדיין החלטת מוצר.

### Missing Information

נבחר כאשר יש פערי מידע שמונעים המלצה אמינה על המשך.

### Initiation Handoff Output

ה־Workflow מחזיר את תוצאות האתחול ל־Lifecycle Orchestrator. הוא אינו הבעלים של תקשורת Phase מתמשכת.

```text
## Project Initiation Report

### Project
[Name]

### Current Phase
[Idea / Discovery]

### Information Collected
-

### Confirmed Findings
-

### Assumptions
-

### Decisions
- None identified

### User Needs
-

### Initial Scope
- In Scope:
- Out of Scope:

### Open Questions
-

### Risks
- Confirmed Risks:
- Potential Risks:
- Unknown Risks Requiring Validation:

### Validation Required
-

### Missing Information
-

### Activated Skills
-

### Created Outputs
-

### Next Recommended Action
[Discovery Required / Ready for Strategy / Missing Information]

### System Improvement Notes
-
```

לאחר ה־Initiation Report, כל הנחיה לגבי Phase, Validation, Required User Action, Completion Criteria או Next Recommended Action נוצרת רק על ידי Lifecycle Orchestrator.

## 10. Information and Escalation Rules

- אין להמציא מידע קריטי.
- יש לסמן הנחות, אי־ודאות ומידע חסר.
- יש לשאול שאלות ממוקדות כאשר התשובה תשנה את הצעד הבא.
- יש לעצור כאשר קיימת סתירה בין מקורות או הוראות.
- החלטות אסטרטגיות, שינוי Scope, סיכון גבוה או פעולה בלתי הפיכה דורשים Human Approval.
- כל תוצר משמעותי נשמר במקור האמת של הפרויקט ומקושר ל־Project State.

## 11. System Improvement Notes

במהלך Initiation תועדו רק פערים בעלי ערך עתידי, כגון:

- Skill חסר או לא מתאים.
- שדה Template שאינו ברור.
- שלב Lifecycle שאינו מתאים.
- מידע שלא ניתן למצוא במקור האמת.
- חיכוך חוזר או פעולה ידנית מיותרת.

הערות אלה הופכות ל־Improvement Candidates ואינן משנות את המערכת באופן אוטומטי.

## 12. Anti-Bureaucracy Rules

- אפשר להתחיל משם או רעיון בלבד.
- אין לדרוש מהמשתמש למלא את כל המידע מראש.
- אין ליצור את כל מסמכי הפרויקט בשלב הפתיחה.
- אין להפעיל את כל ה־Skills או ה־Templates כברירת מחדל.
- יש לשאול רק שאלות שמשפיעות על הבנת הבעיה או על הצעד הבא.
- יש להעדיף Project Brief קצר על פני מסמך פתיחה עמוס.
- אין לעבור ל־Planning לפני Discovery Outputs מספיקים.

## 13. Source Alignment

ה־Workflow תואם את Project Lifecycle בכך שהוא משמש את המעבר Idea → Discovery → Strategy.

הוא תואם את Skill System בכך שהוא מפעיל את Discovery Skill, ומשתמש ב־Research או Decision Support רק לפי צורך.

הוא תואם את Template System בכך שהוא משתמש ב־Project Brief בלבד בשלב הפתיחה, ללא יצירת יתר.

הוא תואם את Knowledge System בכך ש־Context ו־Project Brief נשמרים ב־Project Knowledge, והערות שיפור נשמרות כמועמדים ל־Learning Knowledge.
