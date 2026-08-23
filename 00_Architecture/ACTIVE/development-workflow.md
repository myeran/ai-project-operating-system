# Phase 0.7 — Development Workflow

**System:** AI Project Operating System  
**Status:** In Progress  
**Owner:** System Owner — ערן

## Purpose

להגדיר כיצד AI Project Operating System נבנית ומתפתחת בזמן ההקמה, עד שנגיע למערכת שבה Orchestrator יכול לנהל Workers באופן יעיל.

השלב נועד להחליף בהדרגה את תהליך העבודה הידני:

~~~text
User
↓
Prompt
↓
Worker
↓
Result
↓
Manual Transfer
~~~

בתהליך מבוקר:

~~~text
Task Definition
↓
Orchestrator
↓
Worker Assignment
↓
Execution
↓
Source of Truth Update
↓
Roadmap Update
↓
Next Action
~~~

## 1. Current Development Workflow

### מודל העבודה הנוכחי

- ChatGPT משמש כגורם מתכנן, מפרש ומבקר.
- Worker/Codex מבצע פעולות מוגדרות בסביבת העבודה.
- User משמש כגורם מאשר, מספק הקשר ומעביר החלטות.
- תוצרים נשמרים במסמכים, אך חלק מהעברת ההקשר והסטטוס נעשית ידנית.

### יתרונות

- מאפשר שליטה אנושית בהחלטות משמעותיות.
- גמיש ומתאים לשלב ההקמה.
- מאפשר בדיקה ישירה של תוצרים לפני אישור.
- מפחית סיכון לשינויים לא מאושרים.

### חסרונות

- תלות בהעברת הקשר ידנית.
- סכנת כפילות או עבודה מול גרסה לא קנונית.
- עדכון Roadmap ו־Decision Log אינו אוטומטי.
- קשה לנהל משימות מקבילות וסטטוסים לאורך זמן.
- Worker אינו מקבל תמיד Context מלא ואחיד.

## 2. Target Operating Model

### Orchestrator-driven execution

במודל היעד ה־Orchestrator הוא נקודת התיאום המרכזית:

1. מגדיר או מקבל Task Definition.
2. טוען Project Context, Current Phase, Constraints והחלטות קודמות.
3. בוחר Worker או Skill לפי Scope ויכולת.
4. מעביר Input Contract ותנאי קבלה.
5. עוקב אחר Execution וסטטוס המשימה.
6. בודק את התוצר ומזהה סיכונים או צורך באישור.
7. מעדכן את Source of Truth הקנוני.
8. מעדכן את Roadmap כאשר הסטטוס או השלב משתנים.
9. מגדיר Next Action או מסלים לאדם.

המודל נשען על ארכיטקטורת Orchestrator-Centered Layered Hybrid Architecture: ה־Orchestrator מנהל את הזרימה, בעוד Workers מבצעים עבודה בתחום מוגדר ואינם מחזיקים בבעלות על מצב קנוני.

## 3. Workflow States

| State | משמעות |
|---|---|
| Planned | משימה הוגדרה אך טרם הוקצתה |
| Assigned | Worker או Skill הוקצה |
| In Progress | העבודה מתבצעת |
| Review | התוצר מוכן לבדיקה |
| Approved | התוצר או ההחלטה אושרו |
| Completed | המשימה הושלמה ונשמרה במקור האמת |
| Blocked | לא ניתן להתקדם ללא מידע, החלטה או פתרון חסם |

כל משימה חייבת לכלול Owner, Scope, Expected Output, Current State ו־Next Action. מעבר State מתועד כאשר הוא משמעותי.

## 4. Human Role

האדם נשאר אחראי על:

- אישור תוצרים והחלטות משמעותיות.
- החלטות אסטרטגיות.
- שינויי כיוון, מטרות או Scope.
- בקרת איכות סופית.
- אישור מעבר Gates קריטיים.
- הכרעה במקרים של חוסר ודאות, סתירה או התנגשות ערכים.
- אישור שינויים במערכת, במתודולוגיה או במקור האמת.

בעל הפרויקט או המשתמש הראשי הוא הגורם המאשר. System Owner — ערן — אחראי על בעלות המתודולוגיה ואישור שינויי מערכת.

## 5. Worker Role

Worker מבצע עבודה מוגדרת תחת הקשר והרשאות שה־Orchestrator מספק:

- ביצוע משימות.
- יצירת תוצרים.
- עדכון מסמכים או הצעת עדכונים.
- בדיקות ואימות בתחום האחריות.
- דיווח סטטוס, ממצאים, סיכונים וחסמים.
- החזרת תוצר לפי Worker / Skill Contract.

Worker אינו:

- משנה Scope או מטרות באופן עצמאי.
- מאשר החלטה אסטרטגית או Gate קריטי.
- עוקף את ה־Orchestrator.
- קובע מהו מקור האמת.
- ממשיך כאשר חסר מידע קריטי או קיימת סתירה בלתי פתורה.

## 6. Future Automation Opportunities

הזדמנויות לאוטומציה עתידית:

- טעינת Context אוטומטית לפי Project ID ו־Current Phase.
- פתיחת Tasks מתוך בקשות משתמש.
- התאמת Worker או Skill למשימה.
- יצירת חבילת Input לפי Worker / Skill Contract.
- מעקב אחר Workflow States.
- בדיקת שלמות תוצרים ותנאי קבלה.
- עדכון Project State ו־Source of Truth.
- עדכון Roadmap לפי Completed Items ו־Next Step.
- שמירת Decision Logs.
- יצירת דוחות סטטוס והסלמות.
- זיהוי סיכונים ותלותים חוזרים.
- הפעלת Quality Checks לפני מעבר State.

כל אוטומציה עתידית תידרש לפעול תחת הרשאות, בעלות ומנגנוני עצירה מוגדרים.

## Canonical Workspace Enforcement

לפני ביצוע כל משימה:

1. יש לוודא שהעבודה מתבצעת מתוך:
   AI Project Operating System/
2. אין ליצור או לעדכן מסמכים מחוץ למבנה הרשמי.
3. תיקיות זמניות משמשות רק כ־Workspace זמני ולא כמקור אמת.
4. במקרה של מספר גרסאות, הגרסה הנמצאת במבנה הרשמי היא הקובעת.

## Operating Principle — Minimum Necessary Process

המטרה של Development Workflow היא לשפר זרימה, לא ליצור עומס ניהולי.

עקרונות:

- אין ליצור תיעוד שאין לו שימוש עתידי.
- אין להוסיף שלבי אישור ללא צורך.
- אין לשכפל מידע בין מסמכים.
- כל תהליך חדש חייב להצדיק את הערך שהוא מוסיף.
- המערכת צריכה לאפשר מהירות וגמישות לצד עקביות ובקרה.

## Anti-Bureaucracy Rules

המערכת לא תהפוך לבירוקרטית באמצעות:

- שמירה על מסמכים קצרים וממוקדים.
- יצירת Templates רק כאשר יש שימוש חוזר.
- הפעלת Gates רק בנקודות סיכון משמעותיות.
- התאמת עומק התהליך לרמת המורכבות של הפרויקט.

## 7. Architecture Impact

### Phase חדש

נוסף **Phase 0.7 — Development Workflow** כמסלול תשתיתי תומך, שמגדיר את המעבר מתפעול ידני ל־Orchestrated Execution.

### מסמכים מושפעים

- 00_Architecture/ACTIVE/roadmap.md
- 00_Architecture/ACTIVE/architecture-blueprint.md
- 00_Architecture/ACTIVE/system-contracts-and-state-model.md
- 00_Architecture/ACTIVE/decision-log.md
- 01_System_Core/Agent Identity.md

### האם נדרש עדכון ל־Architecture Blueprint

**לא נדרש עדכון מיידי.**

ה־Blueprint כבר מגדיר:

- Orchestrator כנקודת תיאום מרכזית.
- Workers ב־Execution Layer.
- החזרת תוצרים ל־Orchestrator.
- עדכון ידע ומצב קנוני.

Phase 0.7 מפרט את תהליך ההפעלה והעבודה, אך אינו משנה כרגע את גבולות השכבות או את הבעלות הארכיטקטונית.

עדכון Blueprint יידרש אם יוחלט על רכיב חדש, מנגנון אוטומציה עצמאי, שינוי בעלות על Project State או אינטגרציה שמשנה את זרימת המידע.

## 8. Next Step

- לאשר את Development Workflow.
- להגדיר Operating Rules עבור העבודה השוטפת.
- להגדיר Decision Framework.
- להמשיך בהשלמת Phase 1 — System Foundation.
