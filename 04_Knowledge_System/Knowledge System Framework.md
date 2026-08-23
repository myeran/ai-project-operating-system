# Knowledge System Framework

**System:** AI Project Operating System  
**Agent:** Project Orchestrator Agent  
**Phase:** Phase 4 — Knowledge System  
**Status:** Draft for structure approval  
**Architecture:** Orchestrator-Centered Layered Hybrid Architecture  
**Guiding Principle:** Minimum Necessary Process  
**System Owner:** ערן

## 1. Knowledge System Philosophy

Knowledge System הוא מנגנון לניהול מידע, הקשר, החלטות, ניסיון ולמידה — לא רק מאגר מסמכים.

המערכת קיימת כדי:

- לשמור ידע במקום הנכון ובמקור אמת ברור.
- לספק ל־Orchestrator ול־Skills Context רלוונטי בזמן הנכון.
- לאפשר שימוש חוזר בידע ובהחלטות מפרויקטים קודמים.
- לשמור עקביות בין פרויקטים.
- להפוך ניסיון ולקחים לשיפור מאושר של המערכת.

### Information, Knowledge and Learning

- **Information** — עובדות, נתונים, מסמכים או תוצרים.
- **Knowledge** — מידע מאורגן עם הקשר, משמעות, בעלות ושימוש מוגדר.
- **Learning** — תובנה שהופקה מניסיון, נבדקה ויכולה להוביל לשיפור.

לא כל מידע הופך לידע, ולא כל לקח הופך אוטומטית לכלל מערכת.

## 2. Knowledge Layers

### System Knowledge

ידע קבוע או מנחה של המערכת:

- Architecture.
- Agent DNA.
- Rules.
- Skills ו־Skill Registry.
- Templates.

System Knowledge מגדיר כיצד המערכת עובדת. שינוי בו מתבצע בתהליך מבוקר ובאישור הגורם המוסמך.

### Project Knowledge

ידע ייחודי לפרויקט:

- Project Brief.
- Project State.
- Goals ו־Scope.
- Decisions ו־Approvals.
- Risks, Dependencies ו־Issues.
- Documents ו־Outputs.
- Tasks ו־History.

Project Knowledge מתאר מה ידוע, הוחלט ונעשה בפרויקט מסוים.

### Learning Knowledge

ידע מצטבר מפרויקטים ומפעילות המערכת:

- Lessons Learned.
- Best Practices.
- System Improvements.
- Patterns and Reusable Insights.

Learning Knowledge מציע שיפור. הוא אינו משנה System Knowledge באופן אוטומטי.

## 3. Knowledge Ownership

### System Owner

System Owner — ערן — אחראי על:

- בעלות על System Knowledge.
- אישור שינויים מבניים וכללי מערכת.
- אישור הפיכת Learning ל־System Knowledge.

### Project Orchestrator

ה־Orchestrator אחראי על:

- ניהול Project Knowledge.
- שמירת הקשר רלוונטי ועדכני.
- שילוב תוצרי Skills בידע הפרויקט.
- עדכון Project State, החלטות, סיכונים ותוצרים.
- הבחנה בין עובדה, הנחה, המלצה והחלטה מאושרת.

### Skills

Skills אחראים על:

- יצירת ידע מקצועי בתחום אחריותם.
- ציון מקורות, הנחות, אי־ודאות וסיכונים.
- החזרת תוצרים בפורמט שניתן לשלב ב־Project Knowledge.

Skill אינו בעלים של Project State ואינו משנה System Knowledge באופן עצמאי.

## 4. Knowledge Lifecycle

מחזור החיים של ידע:

```text
Create
   ↓
Store
   ↓
Validate
   ↓
Use
   ↓
Update
   ↓
Archive / Improve
```

### Create

יצירת מידע, תוצר, החלטה, סיכון או לקח עם מטרה ברורה.

### Store

שמירה בשכבת הידע ובמיקום המתאימים, עם בעלות ומקור ברורים.

### Validate

בדיקת שלמות, אמינות, התאמה, כפילויות וסתירות.

### Use

שימוש בידע לקבלת החלטה, ביצוע עבודה, הפעלת Skill או עדכון מצב.

### Update

עדכון כאשר המידע השתנה, התיישן או נלמד מידע חדש.

### Archive / Improve

ארכוב מידע שאינו פעיל, או הפיכת למידה מאושרת לשיפור שימושי. אין לארכב מידע פעיל או מקור אמת רק כדי לצמצם קבצים.

## 5. Source of Truth Model

### Official Source

מקור העבודה הרשמי הוא:

```text
AI Project Operating System/
```

מסמכי המערכת נשמרים במבנה הרשמי בלבד. תיקיות זמניות, Working Notes או עותקים מקומיים אינם מקור אמת כאשר קיימת גרסה רשמית.

### Information Hierarchy

כאשר קיימת התנגשות, סדר העדיפויות הוא:

1. Agent DNA / System Core ו־Architecture.
2. Project Rules.
3. Approved Decisions Log.
4. Project Documents ו־Project State.
5. Working Notes.

יש להתחשב גם בכך ש־Project State הוא הרשומה הקנונית של מצב הפרויקט בזמן נתון.

### Duplicate Prevention

- לכל מידע מהותי יש מקור אמת אחד.
- מסמכים מפנים למקור במקום להעתיק אותו.
- לפני יצירה או עדכון בודקים אם המידע כבר קיים.
- גרסאות שונות מסומנות, נבדקות ומוכרעות מול המקור הרשמי.

### Version Conflicts

כאשר קיימות גרסאות סותרות:

1. עוצרים עד שהסתירה מובנת.
2. מזהים את מקור, הבעלות ותאריך העדכון של כל גרסה.
3. משתמשים בהיררכיית מקור האמת.
4. מתעדים את ההחלטה או מסלימים ל־Human Owner כאשר נדרשת הכרעה.

## 6. Knowledge Retrieval Principles

המערכת משתמשת בידע לפי צורך:

- טוענים Context רלוונטי בלבד.
- לא קוראים את כל מאגר הידע בכל משימה.
- בוחרים ידע לפי Current Phase, Project State, Task ו־Risk Level.
- מפעילים Skill עם Input מצומצם אך מספיק.
- טוענים System Knowledge כאשר נדרשת הבנת כללים או חוזים.
- טוענים Project Knowledge כאשר נדרשת הבנת הפרויקט.
- טוענים Learning Knowledge כאשר יש ערך מניסיון קודם או צורך בשיפור.
- מציינים מה נטען ומה לא נבדק כאשר הדבר משפיע על הוודאות.

### Retrieval Output

Context שנשלף למשימה צריך לכלול, לפי הצורך:

- מקור ומיקום.
- רלוונטיות למשימה.
- סטטוס או גרסה.
- החלטות קשורות.
- סיכונים, אי־ודאות וחוסרים.

## 7. Learning Loop

```text
Project Completed
        ↓
Lessons Captured
        ↓
Reviewed
        ↓
Approved Improvements
        ↓
System Update
```

### Project Completed

מזהים מה קרה, מה הושג ומה נשאר פתוח.

### Lessons Captured

מתעדים מה עבד, מה לא עבד, מה הפתיע ומה כדאי לשמר.

### Reviewed

בודקים שהלקח ברור, מבוסס, חוזר או בעל ערך עתידי, ואינו רק תיאור חד־פעמי.

### Approved Improvements

מנסחים שינוי אפשרי ל־Rule, Skill, Template, Lifecycle או Workflow ומזהים את בעל האישור.

### System Update

רק שיפור שאושר מתורגם לעדכון System Knowledge, עם תיעוד השינוי וההשפעה.

## 8. Anti-Bureaucracy Rules

- לא לשמור מידע שאין בו שימוש נוכחי או עתידי ברור.
- לא לשכפל ידע בין מסמכים.
- לא ליצור מסמך ללא מטרה ובעלות ברורה.
- להעדיף ידע פעיל, נגיש ומתוחזק על פני ארכיון לא שימושי.
- לבצע ניקוי תקופתי של כפילויות ומידע מיושן.
- לא לדרוש תיעוד כאשר אין החלטה, פעולה או למידה בעלות ערך.
- להתאים את עומק התיעוד למורכבות ולסיכון.
- Learning Knowledge מציע שיפור אך אינו משנה את המערכת ללא אישור.

## גבולות השלב

בשלב זה לא מוגדרים:

- מבנה Database.
- Automation.
- Version Control טכני.
- Integrations.
- Storage Rules מפורטים.

נושאים אלה יטופלו רק לאחר אישור מבנה הידע ובשלבים ייעודיים.

## Alignment with Existing System

המסגרת תואמת את Architecture Blueprint בכך שהיא מפרידה בין System Knowledge, Project Knowledge ו־Learning Knowledge ושומרת את ה־Orchestrator כנקודת התיאום.

המסגרת תואמת את Canonical State Model בכך ש־Project State נשאר הרשומה הקנונית של מצב הפרויקט, בעוד מסמכים ותוצרי Skills מספקים ידע תומך.

המסגרת תואמת את Operating Rules באמצעות Single Source of Truth, Documentation With Purpose ו־Minimum Necessary Process.

המסגרת תואמת את Skill System בכך ש־Skills יוצרים ידע מקצועי וה־Orchestrator מאמת ומשלב אותו.
