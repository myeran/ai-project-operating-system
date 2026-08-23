# Template System Framework

**System:** AI Project Operating System  
**Agent:** Project Orchestrator Agent  
**Phase:** Phase 5 — Template System  
**Status:** Draft for structure approval  
**Architecture:** Orchestrator-Centered Layered Hybrid Architecture  
**Guiding Principle:** Minimum Necessary Process  
**System Owner:** ערן

## 1. Template System Philosophy

Template הוא כלי עבודה חוזר שמספק מבנה התחלתי לתוצר או לתהליך. הוא אינו מסמך חובה ואינו מחליף חשיבה, התאמה או החלטה.

Templates קיימים כדי:

- להפחית התחלה מאפס.
- לשמור עקביות בין פרויקטים.
- להבטיח ששאלות ותוצרים חשובים לא יישכחו.
- לחסוך זמן ביצירת מסמכים חוזרים.
- לאפשר ל־Orchestrator להתאים תהליך לפי סוג הפרויקט.

### מתי משתמשים

משתמשים ב־Template כאשר:

- התוצר חוזר ביותר מפרויקט אחד.
- מבנה אחיד משפר איכות או החלטה.
- יש צורך בתיאום בין אדם, Orchestrator ו־Skills.
- קיים ערך ברור לשמירת מידע במבנה קבוע.

### מתי לא משתמשים

לא משתמשים ב־Template כאשר:

- הפעולה חד־פעמית ואינה מצדיקה מבנה חוזר.
- Template יוצר יותר עבודה מהערך שהוא מוסיף.
- ניתן לבצע את העבודה בפשטות ללא תבנית.
- קיים Template מתאים שכבר מכסה את הצורך.

Template הוא נקודת התחלה גמישה: ניתן לקצר, להרחיב או לדלג עליו לפי מורכבות, סיכון ו־Lifecycle.

## 2. Template Definition Model

כל Template עתידי יוגדר במבנה אחיד.

### Template Identity

- **Template Name** — שם יציב וברור.
- **Purpose** — הבעיה או הערך שה־Template משרת.
- **Lifecycle Phase** — השלב או השלבים שבהם הוא רלוונטי.
- **Owner** — הגורם האחראי על איכות ותחזוקה.

### Usage Rules

- מתי משתמשים ב־Template.
- מי משתמש בו.
- באילו סוגי פרויקטים הוא רלוונטי.
- באילו תנאים ניתן לקצר, להרחיב או לדלג עליו.

### Required Inputs

המידע הנדרש למילוי ה־Template, לפי הצורך:

- Project Context.
- Goals ו־Scope.
- Current Phase.
- Constraints.
- Existing Decisions.
- Relevant Risks and Dependencies.
- Available Knowledge.

### Expected Outputs

- איזה תוצר מתקבל.
- מי משתמש בו.
- היכן הוא נשמר במקור האמת.
- אילו החלטות, פעולות או מעברים הוא תומך בהם.

### Maintenance

- מי מעדכן את ה־Template.
- מתי בודקים את השימושיות שלו.
- כיצד מתעדים שינוי משמעותי.
- מתי מאחדים, מפשטים, מעבירים לארכיון או מוחקים.

## 3. Template Categories

הקטגוריות הבאות הן קבוצות ברמה גבוהה בלבד. הן אינן מחייבות יצירת Template בכל קטגוריה.

### Project Templates

- Project Brief.
- Project Plan.

מטרתם להגדיר את הפרויקט, מטרותיו, Scope, התוכנית והמשאבים.

### Decision Templates

- Decision Record.

מטרתם לתעד Context, חלופות, החלטה, נימוק, סיכון, בעלים ואישור.

### Risk Templates

- Risk Register.

מטרתו לשמור סיכונים, הסתברות, השפעה, בעלים ופעולות טיפול.

### Review Templates

- Phase Review.
- Retrospective.

מטרתם לבדוק שלמות, איכות, התאמה, לקחים ומוכנות להמשך.

### Communication Templates

- Status Update.

מטרתו לספק עדכון קצר ועקבי לגבי מצב, חסמים, סיכונים, החלטות והצעד הבא.

## 4. Template Lifecycle

```text
Create
   ↓
Use
   ↓
Validate
   ↓
Improve
   ↓
Archive / Remove
```

### Create

יוצרים Template רק לאחר זיהוי צורך חוזר, Purpose ברור ובעלות מוגדרת.

### Use

מפעילים אותו לפי Phase, Project Type, Complexity ו־Risk Level, וממלאים רק שדות רלוונטיים.

### Validate

בודקים אם הוא חסך זמן, שיפר איכות, תמך בהחלטה והפיק תוצר שימושי.

### Improve

מעדכנים בעקבות שימוש, Feedback, Lessons Learned או שינוי ב־Lifecycle וב־Knowledge System.

### Archive / Remove

מאחדים, מפשטים, מעבירים לארכיון או מסירים כאשר אין שימוש חוזר, קיימת כפילות או שה־Template אינו מוסיף ערך.

## 5. Template Ownership

### Template Owner

אחראי על:

- איכות התבנית.
- תחזוקת המבנה והתוכן.
- בדיקת שימושיות.
- הצעת עדכונים, איחוד או הסרה.

### Project Orchestrator

אחראי על:

- בחירת Template מתאים.
- הפעלתו בזמן הנכון.
- התאמת עומק התבנית לפרויקט.
- שילוב התוצר ב־Project Knowledge או ב־Project State.

### System Owner

System Owner — ערן — אחראי על:

- שינויי Framework.
- אישור שינוי מבני משמעותי במערכת Templates.
- הכרעה כאשר שינוי משפיע על כל המערכת.

## 6. Template Selection Model

ה־Orchestrator בוחר Template לפי שילוב של:

- **Lifecycle Phase** — באיזה שלב נדרש התוצר.
- **Project Type** — סוג הפרויקט והתחום.
- **Complexity** — עומק המבנה הנדרש.
- **Risk Level** — רמת הבקרה והפירוט הנדרשים.
- **Required Output** — התוצר או ההחלטה שיש להפיק.
- **Existing Knowledge** — מידע שכבר קיים ואין צורך לשכפל.

### Selection Process

1. זיהוי התוצר או ההחלטה הנדרשים.
2. בדיקה אם קיים Template מתאים.
3. בדיקה אם ניתן לבצע את העבודה ללא Template.
4. בחירת הגרסה הקלה ביותר שמספקת ערך מספיק.
5. התאמת השדות לפרויקט ולסיכון.
6. שמירת התוצר במקור האמת המתאים.

אין להפעיל מספר Templates עבור אותו צורך כאשר Template אחד מספיק.

## 7. Relationship With Other System Components

- **Lifecycle:** קובע מתי Template עשוי להיות רלוונטי.
- **Skills:** יכולים למלא, להציע או להשתמש ב־Template בתחום אחריותם.
- **Knowledge System:** שומר את ה־Template כ־System Knowledge ואת התוצרים כ־Project Knowledge.
- **Quality Gates:** יכולים להשתמש בתוצר Template כראיה, אך Template אינו Gate בפני עצמו.
- **Orchestrator:** בוחר, מתאים, מאמת ומשלב את התוצר.

## 8. Anti-Bureaucracy Rules

- אין ליצור Template עבור פעולה חד־פעמית.
- אין לשכפל Templates או מידע בין Templates.
- אין להשתמש ב־Template אם הוא מוסיף עומס ללא ערך.
- Templates צריכים לחסוך זמן, לא ליצור עבודה.
- יש להעדיף Template קיים ומתאים על פני יצירת חדש.
- יש לאפשר שדות אופציונליים ודילוג על חלקים שאינם רלוונטיים.
- עומק ה־Template מותאם למורכבות ולסיכון.
- בכל Review משמעותי בודקים אם Template עדיין נחוץ, ברור וקל לתחזוקה.

## גבולות השלב

בשלב זה לא נוצרים:

- Templates בפועל.
- Automation.
- UI.
- Integrations.

נושאים אלה יטופלו בשלבים ייעודיים לאחר אישור ה־Framework.

## Alignment with Existing System

המסגרת תואמת את Architecture Blueprint בכך ש־Templates הם System Knowledge ושה־Orchestrator מנהל את בחירתם והפעלתם.

המסגרת תואמת את Knowledge System בכך שה־Templates נשמרים כמבנה מערכתי, בעוד תוצרים מלאים נשמרים ב־Project Knowledge.

המסגרת תואמת את Lifecycle בכך שהבחירה נעשית לפי Phase, Project Type, Complexity, Risk ו־Required Output.

המסגרת תואמת את Minimum Necessary Process בכך ש־Template הוא כלי אופציונלי, ממוקד וגמיש — לא מסמך חובה.
