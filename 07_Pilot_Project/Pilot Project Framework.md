# Pilot Project Framework

**System:** AI Project Operating System  
**Agent:** Project Orchestrator Agent  
**Phase:** Phase 7 — Pilot Project  
**Status:** Draft for structure approval  
**Architecture:** Orchestrator-Centered Layered Hybrid Architecture  
**Guiding Principle:** Minimum Necessary Process  
**System Owner:** ערן

## 1. Pilot Purpose

Pilot Project הוא ניסוי מבוקר של מערכת ההפעלה על פרויקט אמיתי ראשון. הוא בודק לא רק את תוצאת הפרויקט, אלא גם את שימושיות המערכת עצמה.

### What the Pilot Tests

- האם ה־Lifecycle ברור ושימושי.
- האם Orchestrator מנהל את הזרימה באופן עקבי.
- האם Skills מופעלים רק כאשר נדרש.
- האם Templates חוסכים זמן ומייצרים תוצרים טובים.
- האם Knowledge נשמר במקום הנכון ונמצא בזמן.
- האם Workers יכולים לבצע משימות בלי ליצור בעלות כפולה.
- האם המערכת נשארת פשוטה ולא בירוקרטית.

### Pilot Success

ה־Pilot מצליח כאשר:

- הפרויקט מתקדם לפי Lifecycle מתאים.
- החלטות, סיכונים ותוצרים נשמרים באופן עקבי.
- המערכת מספקת ערך בלי עומס לא מוצדק.
- פערים וחוסרים מזוהים ומתועדים.
- נוצרים Lessons שמובילים, לפי הצורך, לשיפורים מאושרים.

## 2. Pilot Selection Criteria

פרויקט מתאים ל־Pilot צריך להיות:

- אמיתי ובעל בעלים אנושי ברור.
- בעל התחלה וסיום מוגדרים.
- מספיק מורכב כדי לבחון Lifecycle, Skills, Templates ו־Knowledge.
- בעל סיכון נמוך או בינוני, ללא השפעה קריטית שאינה מתאימה לניסוי ראשון.
- תחום שבו ניתן לקבל מידע ומשוב במהלך העבודה.
- ניתן לתחום ב־Scope ברור ובזמן סביר.

### Avoid as First Pilot

- פרויקט בעל סיכון משפטי, כספי, אבטחתי או רגולטורי קריטי.
- פרויקט ללא בעל החלטה זמין.
- פרויקט גדול מדי מכדי לבודד פערים.
- פרויקט חד־פעמי ללא תוצר שניתן לבדיקה.

## 3. Pilot Setup

לפני התחלה יש לוודא:

- Project Brief נוצר ונשמר ב־Project Knowledge.
- Project Owner ו־Human Approver מזוהים.
- Lifecycle ומסלול השלבים נבחרו.
- Skills רלוונטיים זוהו, בלי להפעילם מראש ללא צורך.
- Templates רלוונטיים נטענו לפי מורכבות וסיכון.
- Context ראשוני, Goals, Scope, Constraints ו־Assumptions נשמרו.
- Risks ראשוניים והחלטות פתוחות זוהו.
- תנאי הצלחה ו־Exit Criteria ראשוניים הוגדרו.

### Setup Decision

ה־Orchestrator מאשר שהפרויקט מתאים ל־Pilot ומציג לבעל הפרויקט את היקף הניסוי, הסיכונים והציפיות.

## 4. Pilot Execution Model

```text
Project Start
      ↓
Project Brief
      ↓
Lifecycle Execution
      ↓
Skills Activation
      ↓
Templates Usage
      ↓
Reviews
      ↓
Lessons Learned
```

### Operating Rules

- ה־Orchestrator מנהל Phase, State, Decisions ו־Next Actions.
- Skills ו־Workers מופעלים לפי צורך מוגדר.
- Context נטען לפי Phase, Task, Skill וסיכון.
- תוצרים עוברים Review לפני שילוב במקור האמת.
- החלטות משמעותיות וסיכונים מתועדים בזמן ולא בדיעבד בלבד.
- ניתן לקצר, לאחד או לדלג על שלבים שאינם רלוונטיים.
- כל חריגה מהמודל מתועדת כהחלטה או כהנחת עבודה כאשר היא משמעותית.

## 5. What To Measure

המדידה היא איכותית וממוקדת; אין ליצור Metrics Dashboard בשלב זה.

### Process

- האם השלבים היו ברורים?
- האם המעברים היו מובנים?
- האם נוצרו חסמים או עצירות לא צפויות?
- האם ה־Orchestrator סיפק את ההקשר הנכון?

### Usability

- האם המסמכים עזרו לקבל החלטות או לבצע עבודה?
- האם היה עומס תיעודי?
- האם היה קל למצוא מידע?
- אילו שדות או שלבים לא היו בשימוש?

### Skills and Workers

- האם Skill או Worker הופעלו בזמן הנכון?
- האם התוצר היה שימושי ואיכותי?
- האם חסר Skill או Worker?
- האם הופעלו יכולות שאפשר היה להימנע מהן?

### Knowledge

- האם החלטות, סיכונים ותוצרים נשמרו במקור הנכון?
- האם ה־Context שנשלף היה רלוונטי?
- האם נוצרה כפילות?
- האם הידע היה שימושי בשלב הבא?

### Evidence

כל ממצא משמעותי צריך לכלול דוגמה, מקור או אירוע מה־Pilot. אין להסיק מסקנות מערכתיות מאירוע יחיד ללא הקשר.

## 6. Pilot Review

### Review Points

Review מתבצע בנקודות בעלות ערך:

- לאחר Setup ראשוני.
- במעבר משמעותי בין Phases.
- כאשר מתגלה חסם או סיכון גבוה.
- בסיום הפרויקט.

אין לבצע Review עמוק לכל פעולה קטנה.

### Closing Review

בסיום מתעדים:

- מה עבד.
- מה לא עבד.
- מה היה חסר.
- מה יצר עומס ללא ערך.
- אילו החלטות היו עקביות או בעייתיות.
- אילו Skills, Templates או Workers נדרשים לשינוי.
- אילו Lessons ראויים לקידום.

## 7. Improvement Loop

```text
Pilot Completed
        ↓
Lessons Learned
        ↓
Review
        ↓
Approved Improvements
        ↓
System Update
```

### Improvement Rules

- Lesson נשאר Project Knowledge עד שנבדק.
- שיפור מוצע מקבל Owner, Rationale והשפעה צפויה.
- שינוי ב־System Knowledge דורש Review ואישור לפי Knowledge System.
- שיפור שאינו מצדיק שינוי נשמר כתובנה בלבד או לא נשמר.
- לאחר עדכון מערכת יש לבדוק אם השינוי אכן פתר את הבעיה.

## 8. Anti-Bureaucracy Rules

- Pilot אינו מקום להוסיף תהליכים ללא צורך.
- כל שינוי חייב להוכיח ערך ברור.
- עדיפות לפישוט לפני הרחבה.
- אין ליצור Automation לפני שמבינים כאבים אמיתיים.
- אין להפעיל את כל ה־Skills או ה־Templates רק כדי לבדוק שהם קיימים.
- אין להפוך כל תצפית ל־Rule או ל־System Improvement.
- משוב קצר וממוקד עדיף על דוח שאינו נקרא.

# Baseline Measurement

מטרת ה־Baseline היא לתעד את מצב העבודה לפני הרצת ה־Pilot, כדי לזהות שיפור, עומס או פערים לאחר השימוש במערכת. המדידה יכולה להיות איכותית או הערכה פשוטה; אין ליצור Dashboard או מנגנון Metrics מתקדם.

## Process Baseline

תעד לפני תחילת ה־Pilot:

- זמן פתיחת פרויקט.
- זמן מעבר משלב רעיון לתוכנית.
- כמות איטרציות או העברות ידניות.
- נקודות חוסר בהירות.

## Knowledge Baseline

תעד:

- היכן נשמר מידע כיום.
- כמה קל למצוא החלטות קודמות.
- האם קיימת כפילות מידע.

## Workflow Baseline

תעד:

- כמה צעדים ידניים קיימים.
- היכן יש צווארי בקבוק.
- היכן חסרה מתודולוגיה.

# Pilot Success Criteria

ה־Pilot נחשב מוצלח כאשר מתקיימים התנאים הבאים:

## Process

- ניתן לפתוח פרויקט לפי המערכת.
- נבחר Lifecycle מתאים לצורך.
- השלבים והמעברים ברורים.

## Usability

- Templates עוזרים ואינם מעמיסים.
- אין בירוקרטיה מיותרת.
- המשתמש מבין היכן נמצא הפרויקט ומה הצעד הבא.

## Skills

- Skills מופעלים בזמן הנכון ולפי צורך.
- Outputs שימושיים וניתנים לשילוב.

## Knowledge

- החלטות נשמרות במקור הנכון.
- לקחים מופקים ומתועדים.
- ידע ניתן לשימוש עתידי.

## System Improvement

- נקודות לשיפור מזוהות עם Evidence.
- ניתן להציע ולעדכן את המערכת בעקבות ניסיון, בכפוף ל־Review ואישור.

## גבולות השלב

בשלב זה לא נוצרים:

- Automation.
- Worker Instances.
- Integrations.
- Metrics מתקדמים.
- Project Workspace של פרויקט אמיתי.

## Alignment with Existing System

ה־Pilot משתמש ב־Lifecycle, Skills, Templates, Knowledge System ו־Worker Operating Model שכבר הוגדרו.

ה־Orchestrator נשאר בעל השליטה על Project State, החלטות, מעברים ו־Source of Truth.

Lessons Learned מוזנים ל־Learning Knowledge רק לאחר Review, ושינויי מערכת דורשים אישור. כך ה־Pilot בודק את המערכת בלי לעקוף את כללי הסמכות והבקרה שלה.
