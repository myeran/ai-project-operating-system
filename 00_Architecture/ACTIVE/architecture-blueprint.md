# AI Project System — Architecture Blueprint

**Phase:** Phase 0 — Architecture Blueprint  
**Status:** Completed  
**Scope:** ארכיטקטורת־על בלבד; ללא פירוט DNA, Skills או Templates

## 1. System Overview

AI Project System היא מערכת הפעלה לניהול פרויקטים, המלווה פרויקט מהרעיון ועד סיום, השקה ושיפור מתמשך.

המערכת:

- מסווגת בקשות ומזהה את הקשר הפרויקט.
- בוחרת ומנהלת Lifecycle מתאים.
- מפעילה Skills ו־Workers לפי צורך.
- מייצרת תוצרים ושומרת החלטות, סיכונים, משימות והיסטוריה.
- אוכפת Quality Gates וסמכויות החלטה.
- לומדת מתוצאות הפרויקט ומשפרת את המערכת.

### רכיבים מרכזיים

1. **Orchestration Layer** — מנהל התהליך והקשרים.
2. **Process Layer** — מגדיר איך פרויקט מתקדם.
3. **Capability Layer** — מספק יכולות מקצועיות באמצעות Skills ו־Expert Agents.
4. **Knowledge Layer** — שומר ידע מערכתי, ידע פרויקטלי וידע למידה.
5. **Execution Layer** — מבצע פעולות באמצעות Workers, Tools, מערכות קבצים ואינטגרציות.

### עקרון תקשורת

ה־Orchestrator הוא נקודת התיאום המרכזית. Skills ו־Workers אינם משנים ישירות את כללי המערכת או את מצב הפרויקט הקנוני; הם מחזירים תוצרים, ממצאים והמלצות ל־Orchestrator, והוא מעדכן את הידע ומנהל את המעברים.

## 2. Architecture Layers

### Layer 1 — Orchestration Layer

**רכיב:** Project Orchestrator Agent

**אחריות:**

- ניהול Lifecycle.
- זיהוי השלב הנוכחי.
- הפעלת Skills ו־Workers.
- ניהול החלטות, אישורים והסלמות.
- שמירה על עקביות, סטטוס ותיעוד.
- ניהול מעבר בין שכבות המערכת.

**גבול:** אינו מחליף החלטות אנושיות ואינו מבצע פעולה מחוץ להרשאות או ל־Scope המאושר.

### Layer 2 — Process Layer

מכיל:

- Project Lifecycle.
- Phases.
- Quality Gates.
- Decision Rules.

**מטרה:** להגדיר את סדר ההתקדמות, תנאי המעבר, הבקרות והחלטות הנדרשות בכל שלב.

### Layer 3 — Capability Layer

מכיל Skills ו־Expert Agents, לדוגמה:

- Discovery.
- Product.
- Marketing.
- Legal.
- Finance.
- Engineering.
- QA.
- Security.
- Analytics.

**הפעלת Skills:** ה־Orchestrator מזהה פער או צורך, בוחר Capability מתאים, מעביר לו Input מוגדר ומקבל Output מתועד.

**תקשורת עם Orchestrator:** באמצעות חוזה עבודה אחיד הכולל מטרה, הקשר, Input, מגבלות, תוצר, אי־ודאות וסיכונים. Skill אינו מאשר Gate ואינו משנה Scope בעצמו.

### Layer 4 — Knowledge Layer

#### System Knowledge

- Agent DNA.
- Rules.
- Skills Registry.
- Templates.

#### Project Knowledge

- Documents.
- Decisions.
- Risks.
- Tasks.
- History.

#### Learning Knowledge

- Lessons Learned.
- Best Practices.
- Improvements.

**עקרון בעלות:** System Knowledge מגדיר את כללי המערכת; Project Knowledge מתאר את הפרויקט; Learning Knowledge מציע שיפורים עתידיים ואינו משנה את המערכת ללא אישור ותהליך מבוקר.

### Layer 5 — Execution Layer

מכיל:

- Workers.
- Tools.
- File Systems.
- External Integrations.
- Automation.

**מטרה:** לבצע עבודה בפועל לפי משימה מאושרת, הרשאות, Scope ותנאי עצירה. תוצאות הביצוע חוזרות ל־Orchestrator לצורך אימות, תיעוד ועדכון מצב.

## 3. Data Flow

```text
Project Request
      ↓
Orchestrator
      ↓
Classification & Context Understanding
      ↓
Select Lifecycle / Current Phase
      ↓
Check Rules, Risks & Required Approvals
      ↓
Activate Skills / Workers
      ↓
Review and Validate Outputs
      ↓
Create or Update Project Outputs
      ↓
Store Decisions, Risks, Tasks and History
      ↓
Pass Quality Gate or Escalate
      ↓
Capture Learning
```

ה־Orchestrator הוא בעל הבעלות על זרימת המידע. כל עדכון משמעותי צריך להיות ניתן למעקב אל מקורו, התוצר שהוביל אליו והאישור הרלוונטי.

## 4. Project Lifecycle Model

ברמת־על, כל פרויקט עובר את השלבים הבאים:

1. **Discovery** — הבנת הבעיה, הצורך, המשתמשים ובעלי העניין.
2. **Strategy** — הגדרת מטרות, ערך, כיוון וסדרי עדיפויות.
3. **Planning** — הגדרת Scope, תכנית עבודה, משאבים, תלותים וסיכונים.
4. **Design** — תכנון הפתרון, חוויית המשתמש, המודל התפעולי או התוצר.
5. **Execution** — ביצוע העבודה וניהול השינויים.
6. **Validation** — בדיקת איכות, התאמה למטרות ונכונות התוצרים.
7. **Launch** — הכנה, אישור והשקה.
8. **Improvement** — מדידה, למידה ושיפור מתמשך.

ה־Lifecycle הוא ברירת המחדל. פרויקטים יכולים לדלג, לאחד או להרחיב שלבים רק כאשר ההתאמה מנומקת, מתועדת ומאושרת לפי הצורך.

## 5. Decision Authority Model

### הסוכן מחליט

- מהו השלב הנוכחי.
- אילו שאלות, תוצרים או בדיקות חסרים.
- איזה Skill או Worker רלוונטי להפעלה.
- כיצד לנהל את סדר העבודה במסגרת Scope מאושר.
- מתי לעצור, לסמן חסם או לבקש החלטה.

### נדרש אישור אדם

בעל הפרויקט או המשתמש הראשי מאשר:

- שינוי מטרות.
- שינוי משמעותי ב־Scope.
- החלטות אסטרטגיות.
- החלטות משפטיות או כספיות.
- מעבר Gates קריטיים.

כל אישור משמעותי נשמר ב־Decision Log.

### הסלמה

הסוכן עוצר ומסלים כאשר חסר מידע קריטי, קיימת סתירה בין מקורות, קיימת התנגשות בין הוראות או נדרשת החלטה בעלת השפעה עסקית משמעותית.

## 6. Ownership, State and Invariants

### בעלות על מצב

| מצב או מידע | בעלים קנוני |
|---|---|
| שלב הפרויקט והסטטוס | Orchestrator / Process Layer |
| כללי המערכת | System Knowledge |
| החלטות ואישורים | Approved Decisions Log |
| תוצרים ומסמכי פרויקט | Project Knowledge |
| ביצוע בפועל | Execution Layer, תחת משימה מאושרת |
| לקחים והצעות שיפור | Learning Knowledge |

### Invariants

- לכל מצב קנוני יש בעלים אחד.
- Worker או Skill אינם עוקפים את ה־Orchestrator.
- אין מעבר Gate ללא תנאי המעבר והאישור הנדרש.
- מידע סותר, חסר או לא ודאי מסומן ומוסלם במקום להיטמע כעובדה.
- שינוי משמעותי ניתן למעקב דרך Decision Log ו־History.
- Learning Knowledge אינה משנה Rules או DNA באופן אוטומטי.

## 7. Architectural Decision

הארכיטקטורה שנבחרה היא **Orchestrator-Centered Layered Hybrid Architecture**:

- Orchestrator מרכזי מנהל את התהליך והמצב.
- שכבות מופרדות לפי אחריות.
- Capabilities ניתנות להחלפה ולהרחבה בלי לשנות את ליבת התהליך.
- Lifecycle אחיד משמש בסיס, עם התאמות מבוקרות.
- Knowledge מופרד לפי System, Project ו־Learning.

חלופות שנדחו בשלב זה:

- **Worker-led model** — יוצר בעלות מפוצלת וחוסר עקביות.
- **Fully rigid model** — אינו מתאים למגוון סוגי פרויקטים.
- **Fully autonomous model** — אינו מתאים לרמת הסמכות שאושרה.

## 8. Open Questions

### החלטות שעדיין חסרות

- מהו פורמט החוזה האחיד בין Orchestrator, Skills ו־Workers.
- מהו מודל ההרשאות הטכני בין שכבות.
- היכן נשמר המידע הקנוני בפועל.
- כיצד נמדדת הצלחת Lifecycle ו־Quality Gates.
- מי מאשר שינויים ב־System Knowledge.

### סיכונים ארכיטקטוניים

- כפילות בעלות בין Orchestrator, Workers ומערכות חיצוניות.
- הצטברות ידע לא מובנה או לא מתויג.
- התאמות רבות מדי ל־Lifecycle שעלולות ליצור כאוס.
- שינוי אוטומטי ולא מבוקר של Rules או DNA.
- תלות באינטגרציות חיצוניות ללא מנגנון כשל מבוקר.

### המלצות להמשך

1. להגדיר חוזה Worker/Skill אחיד.
2. להגדיר מודל מצב וסטטוס קנוני לפרויקט.
3. לבנות את Lifecycle ואת Quality Gates ברמת פירוט הבאה.
4. לאחר מכן להגדיר את סדר בניית ה־DNA, ה־Skills וה־Templates.
5. להוסיף בדיקות עקביות, הרשאות ו־fail-closed לכל מעבר משמעותי.

## 9. Phase 0 Completion Check

- **רכיבי המערכת:** מוגדרים.
- **קשרים בין הרכיבים:** מוגדרים.
- **זרימת מידע:** מוגדרת.
- **גבולות אחריות:** מוגדרים.
- **Phase 0:** Completed.

