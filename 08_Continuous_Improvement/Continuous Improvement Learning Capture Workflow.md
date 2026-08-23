# Continuous Improvement Learning Capture Workflow

**System:** AI Project Operating System  
**Role:** Continuous Improvement Learning Capture  
**Parent:** Project Orchestrator Agent  
**Source Framework:** Continuous Improvement Framework.md  
**Guiding Principle:** Minimum Necessary Process

## 1. Purpose

Workflow זה לוכד למידה מפרויקטים, מפריד בין למידה ייחודית לפרויקט לבין שיפור מערכתי, ומנתב שיפורים מועמדים למחזור השיפור הקיים.

ה־Workflow אינו משנה את AI Project Operating System ישירות ואינו יוצר מודל State חדש.

## 2. Triggers

הפעל כאשר:

- Pilot מזהה פער בתהליך.
- משתמש מדווח על חיכוך.
- Worker או Skill מתנהג באופן הדורש שיפור.
- מתגלה יכולת חסרה.
- מופיעה תבנית חוזרת ביותר מפרויקט אחד.
- Phase Review או Lessons Learned מצביעים על שינוי אפשרי.

## 3. Capture Flow

```text
Observation
    ↓
Classify: Project Learning / System Learning
    ↓
Capture Evidence
    ↓
Create Improvement Item, אם נדרש
    ↓
Impact Assessment
    ↓
Recommendation
    ↓
Existing Improvement Lifecycle
```

## 4. Step 1 — Classify Learning

### Project Learning

למידה שחלה רק על הפרויקט הנוכחי, כגון:

- העדפת משתמש.
- תובנת מוצר או עסק.
- החלטת פרויקט.
- תוצאה או לקח שאינם רלוונטיים לפרויקטים אחרים.

**Store:** Project Learning / Project Knowledge.

Project Learning אינו נכנס אוטומטית ל־System Knowledge.

### System Learning

למידה שעשויה לשפר את AI Project Operating System, כגון:

- Skill חסר או לא שימושי.
- Worker חסר.
- Workflow לא ברור.
- Template לא יעיל.
- Process Gap.
- בעיה חוזרת בין פרויקטים.

**Store:** Improvement Backlog כ־Improvement Item.

הסיווג הוא המלצה ראשונית. כאשר לא ברור אם הלמידה מערכתית, יש לסמן Uncertainty ולהעדיף שמירה כ־Project Learning עד לבחינה.

## 5. Step 2 — Capture Evidence

לכל Observation שמור:

- מקור.
- פרויקט.
- תאריך.
- תיאור עובדתי.
- תוצר, החלטה או אירוע תומך.
- האם מדובר באירוע יחיד או בתבנית חוזרת.

יש להפריד בין Observation, Analysis ו־Recommendation. אין להציג הצעה כאילו היא עובדה.

## 6. Step 3 — Create Improvement Item

עבור System Learning צור את הרשומה הבאה ב־Improvement Backlog:

```text
Improvement Item

ID:
Source:
Pilot Project:

Observation:

Evidence:

Problem:

Impact:

Affected Component:
- Framework
- Skill
- Worker
- Template
- Knowledge
- Process
- System

Recommendation:

Priority:
- Low
- Medium
- High

Status:
- Identified
- Analyzed
- Proposed
- Approved
- Implemented
- Validated
```

`Improvement Item` הוא מועמד לשיפור בלבד. הוא אינו אישור ואינו מעדכן רכיב מערכת.

## 7. Step 4 — Impact Assessment

לפני Recommendation, בדוק:

### Scope of Impact

- האם ההשפעה מוגבלת לפרויקט אחד?
- האם היא רלוונטית לכל הפרויקטים העתידיים?
- האם היא משפיעה על Workflow קיים?
- האם היא משפיעה על Skills או Templates קיימים?
- האם היא דורשת שינוי ב־System Core?

### Risk and Cost

- מורכבות שתתווסף.
- עלות תחזוקה.
- כפילויות אפשריות.
- תופעות לוואי.
- סיכון לפגיעה בעקביות או במהירות.

### Evidence Strength

- אירוע יחיד.
- משוב חוזר.
- תבנית ביותר מפרויקט אחד.
- בעיה שמונעת מעבר או יוצרת סיכון משמעותי.

אין להמליץ על שינוי מערכתי כאשר פתרון מקומי או פישוט מספיקים.

## 8. Step 5 — Route Through Existing Improvement Lifecycle

השתמש במחזור הקיים:

```text
Identify
↓
Analyze
↓
Assess Impact
↓
Recommend
↓
Approve
↓
Implement
↓
Validate
```

כללי ניתוב:

- **Project Learning:** נשמר ב־Project Knowledge ואינו מתקדם ל־System Improvement ללא Evidence נוסף.
- **Local Improvement:** עובר Review ואישור של בעל הרכיב או ה־Orchestrator, לפי הסמכות הקיימת.
- **Component Improvement:** דורש Review ממוקד והערכת השפעה.
- **System Improvement:** דורש Review משמעותי ואישור System Owner.

שינוי ארכיטקטוני מתועד ב־Decision Log רק לאחר שהתקבלה החלטה ארכיטקטונית.

## 9. Ownership and Storage

- **Project Orchestrator:** מסווג, מתעד, מעריך השפעה ומנתב.
- **Project Knowledge:** שומר Project Learning והקשר המקורי.
- **Improvement Backlog:** שומר Improvement Items שטרם אושרו או יושמו.
- **Improvement History:** שומר מה השתנה, למה, מי אישר ומה הייתה התוצאה.
- **System Owner:** מאשר שינויי Framework, System Core ושינויים שחוצים שכבות.
- **Component Owner:** אחראי לשיפור רכיב בתחום שלו.

ה־Workflow משתמש במבני ה־Continuous Improvement Framework הקיימים ואינו יוצר מאגר חדש.

## 10. User Communication

כאשר למידה נלכדה, החזר:

```text
## Learning Captured

Source:
Project:

Type:
Project Learning / System Improvement

Observation:

Evidence:

Recommended Action:

Current Status:

Next Step:
```

אם מדובר ב־Project Learning, ציין שהוא נשמר ב־Project Knowledge ואינו משנה את המערכת.

אם מדובר ב־System Improvement, ציין שהוא נרשם כ־Improvement Item וממתין ל־Review/Approval.

## 11. Anti-Bureaucracy Rules

- לא כל רעיון הופך ל־Improvement Item.
- לא כל Lesson הופך לשינוי מערכת.
- אין לשנות את ה־OS ישירות מתוך Pilot.
- יש לשמר Evidence לפני Recommendation.
- יש להעדיף שיפור רכיב קיים על פני יצירת רכיב חדש.
- יש להעדיף פישוט לפני הרחבה.
- Improvement Item ללא שימוש עתידי ברור ניתן לסגור או להשאיר כ־Project Learning.

## 12. Validation Examples

### Example 1 — Project-Specific Learning

```text
Observation: Users prefer shorter recipes.
Classification: Project Learning
Store: Project Knowledge
System Change: None
Next Step: Use the insight in the current project and record it in Lessons Learned if relevant.
```

### Example 2 — System Improvement

```text
Observation: Projects need a structured Change Request process.
Classification: System Learning / Improvement Candidate
Affected Component: Process / Framework
Store: Improvement Backlog as Improvement Item
Next Step: Analyze recurrence, impact and a minimal solution before requesting approval.
System Change: None until Review and Approval are complete.
```

## 13. Success Criteria

ה־Workflow הצליח כאשר:

- Observation סווגה נכון כ־Project Learning או System Learning.
- Evidence נשמר.
- Project Learning לא שינה את המערכת.
- System Learning נרשם כ־Improvement Item.
- Recommendation נפרדת מאישור.
- כל שינוי עובר את מחזור השיפור הקיים.
- המשתמש יודע מה נתפס, מה הסטטוס ומה הצעד הבא.
