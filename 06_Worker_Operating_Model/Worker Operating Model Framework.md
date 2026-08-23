# Worker Operating Model Framework

**System:** AI Project Operating System  
**Agent:** Project Orchestrator Agent  
**Phase:** Phase 6 — Worker Operating Model  
**Status:** Draft for structure approval  
**Architecture:** Orchestrator-Centered Layered Hybrid Architecture  
**Guiding Principle:** Minimum Necessary Process  
**System Owner:** ערן

## 1. Worker Philosophy

Worker הוא יחידת ביצוע שמבצעת Task מוגדר תחת Context, Scope ותנאי עצירה שסופקו על ידי ה־Orchestrator.

Workers קיימים כדי:

- לבצע עבודה מוגדרת באופן יעיל.
- לאפשר חלוקת עבודה לפי יכולת או Skill.
- להחזיר תוצרים שניתן לבדוק ולשלב.
- לתמוך בפרויקטים פשוטים ומורכבים בלי לפצל את בעלות המערכת.

### Worker מול Orchestrator

ה־Orchestrator:

- מנהל Lifecycle ו־Project State.
- מסווג משימה ובוחר Worker או Skill.
- מגדיר Context, Scope, Expected Output ותנאי קבלה.
- מאמת את התוצאה ומחליט על המשך, עדכון או הסלמה.

ה־Worker:

- מבצע Task בתחום שהוגדר.
- משתמש ב־Skill וב־Knowledge שסופקו.
- מדווח מצב, ממצאים, סיכונים ותוצרים.
- אינו מנהל את הפרויקט ואינו בעלים של המצב הקנוני.

## 2. Worker Types

הסוגים הבאים הם קטגוריות ברמה גבוהה בלבד. אין ליצור עדיין Worker Instances.

### Execution Worker

מבצע משימות מוגדרות ויוצר תוצר או שינוי בתחום Scope מאושר.

### Analysis Worker

מבצע מחקר, ניתוח, השוואה או עיבוד מידע ומחזיר Findings ו־Recommendations.

### Review Worker

מבצע בדיקות איכות, שלמות, התאמה וסיכון לפי קריטריונים מוגדרים.

### Specialist Worker

מופעל לפי Skill או תחום ידע מוגדר, כגון Product, Technical, Legal או Finance.

Worker אחד יכול להשתייך ליותר מסוג אחד כאשר הדבר מוסיף בהירות ואינו יוצר בעלות כפולה.

## 3. Worker Lifecycle

```text
Task Created
      ↓
Assigned
      ↓
Context Loaded
      ↓
Execution
      ↓
Output Generated
      ↓
Review
      ↓
Knowledge Update
      ↓
Completed
```

### Task Created

ה־Orchestrator מגדיר Task ID, מטרה, Scope ותוצר מצופה.

### Assigned

נבחר Worker מתאים ונקבע Owner תפעולי ותנאי דיווח.

### Context Loaded

ה־Worker מקבל את המידע הרלוונטי בלבד, בהתאם ל־Input Contract.

### Execution

ה־Worker מבצע את העבודה בתחום האחריות ובהתאם למגבלות.

### Output Generated

ה־Worker מחזיר Output Contract הכולל מצב, תוצרים, אי־ודאות וסיכונים.

### Review

ה־Orchestrator או Reviewer מתאים בודק שלמות, התאמה ל־Scope, מקורות ותנאי קבלה.

### Knowledge Update

רק ה־Orchestrator או גורם מורשה משלב את התוצאה ב־Project Knowledge או ב־Project State.

### Completed

המשימה מסומנת Completed רק לאחר אימות או מסומנת Partial, Blocked או Escalated כאשר נדרש.

## 4. Context Loading Model

ה־Worker מקבל Context רלוונטי בלבד:

- Project Context.
- Current Phase.
- Task Definition ו־Task ID.
- Relevant Skill.
- Relevant Knowledge.
- Goals ו־Scope.
- Constraints.
- Previous Decisions.
- Risks and Dependencies.
- Expected Output ו־Acceptance Criteria.

### Context Rules

- אין לטעון את כל מאגר הידע ללא צורך.
- יש להעדיף מקור אמת רשמי וגרסה עדכנית.
- יש לסמן מידע חסר, סותר או לא ודאי.
- יש להפריד בין עובדות, הנחות, ניתוח והמלצות.
- Context שאינו נחוץ למשימה אינו מועבר כברירת מחדל.

## 5. Worker Input / Output Contract

### Input Contract

כל משימה ל־Worker תכלול, לפי הרלוונטיות:

- **Task** — מה לבצע.
- **Goal** — למה לבצע.
- **Context** — ההקשר הנדרש.
- **Expected Output** — התוצר ותנאי הקבלה.
- **Constraints** — גבולות, איסורים ותלויות.
- **Current State** — Phase, Status ו־Blockers רלוונטיים.

### Output Contract

ה־Worker מחזיר:

- **Status:** Completed / Partial / Blocked / Escalated.
- **Findings.**
- **Analysis.**
- **Recommendations.**
- **Created Artifacts.**
- **Risks.**
- **Decisions Needed.**
- **Assumptions and Uncertainties.**
- **Next Actions.**
- **Handoff:** פעולה נדרשת מה־Orchestrator.

כל תוצר משמעותי כולל מקור או סימון מפורש שהוא ניתוח, הנחה או המלצה.

## 6. Orchestrator ↔ Worker Relationship

### User-Facing Handoff Rule

Workers מחזירים תוצאות ביצוע ל־Orchestrator בלבד. Worker אינו מייצר Phase Guidance, אינו מנחה את המשתמש מה לעשות בשלב ואינו מקבל החלטת השלמה או מעבר.

ה־Orchestrator ממיר את תוצאת ה־Worker ל־Phase Guidance Output Contract לפני הצגה למשתמש.

### Orchestrator Responsibilities

- לזהות צורך ולנסח Task.
- לבחור Worker ו־Skill מתאימים.
- להקצות Scope, Context ותנאי קבלה.
- לעקוב אחר Status ו־Blockers.
- לאמת את התוצאה.
- לשלב Output ב־Project State או Knowledge.
- לנהל החלטות, אישורים, Gates והסלמות.

### Worker Responsibilities

- לבצע את ה־Task שהוקצה.
- להישאר בתוך Scope ו־Constraints.
- להשתמש ב־Context וב־Skill שנמסרו.
- לדווח באופן שקוף על מצב, חוסרים וסיכונים.
- ליצור תוצרים בתחום האחריות.
- להחזיר Handoff ברור.

### Canonical State Rule

Worker אינו מעדכן Project State, Scope, Phase או Rules באופן עצמאי. כל שינוי קנוני עובר דרך ה־Orchestrator או גורם מורשה שהוגדר מראש.

## 7. Human Approval Model

Worker חייב לעצור ולהסלים כאשר:

- נדרשת החלטה אסטרטגית.
- נדרש שינוי Scope או מטרות.
- קיים סיכון גבוה או השפעה עסקית משמעותית.
- חסר מידע קריטי.
- קיימת סתירה בין מקורות או הוראות.
- נדרשת פעולה משפטית, כספית, רגולטורית, אבטחתית או פרטיות.
- הפעולה בלתי הפיכה או חורגת מהסמכות שהוגדרה.

### Escalation Output

```text
Issue:
Context:
Impact:
Options:
Recommendation:
Decision Needed:
```

האישור האנושי נשאר באחריות Human Owner או בעל האישור שהוגדר לפרויקט. Worker אינו מאשר את ההחלטה בעצמו.

## 8. Worker Quality Criteria

Worker נחשב איכותי כאשר:

- ביצע לפי ה־Task וה־Context שנמסרו.
- התוצר עומד ב־Expected Output ובתנאי הקבלה.
- ה־Output Contract מולא באופן עקבי.
- עובדות, הנחות, ניתוח והמלצות מופרדים.
- מקורות, סיכונים וחוסרים מתועדים.
- לא הייתה חריגה מ־Scope, Constraints או סמכות.
- התוצר ניתן לשילוב ב־Project Knowledge או Project State.
- ה־Handoff מאפשר ל־Orchestrator לבצע את הצעד הבא.

## 9. Anti-Bureaucracy Rules

- אין ליצור Worker ללא צורך חוזר או משמעותי.
- אין ליצור Worker לכל משימה קטנה.
- Worker אינו מחליף Process.
- Worker אינו מחליף Decision Authority.
- יש להעדיף יכולת או Skill קיימים לפני יצירת Worker חדש.
- אין להפעיל Worker כאשר ניתן לבצע את העבודה בפשטות ללא Worker נוסף.
- אין להעביר Context או ליצור דיווחים שאין להם שימוש ברור.
- מספר Workers ועומק התיאום מותאמים למורכבות ולסיכון.

## גבולות השלב

בשלב זה לא מוגדרים או נוצרים:

- Automation.
- Integrations.
- APIs.
- Worker Instances.
- Agent Teams.

נושאים אלה יטופלו בשלבים ייעודיים לאחר אישור ה־Framework.

## Alignment with Existing System

המסגרת תואמת את Architecture Blueprint בכך ש־Workers נמצאים ב־Execution Layer וה־Orchestrator נשאר נקודת התיאום המרכזית.

המסגרת תואמת את Worker / Skill Contract ואת Canonical State Model בכך שה־Worker מקבל Input מוגדר, מחזיר Output מובנה, ורק ה־Orchestrator משלב את התוצאה במצב הקנוני.

המסגרת תואמת את Lifecycle, Knowledge System ו־Skill System בכך שהקצאת Worker נקבעת לפי Phase, Task, Skill, Context, סיכון ותוצר נדרש.

המסגרת תואמת את Minimum Necessary Process בכך שהיא מגדירה Worker כיחידת ביצוע לפי צורך, ולא כשכבת ניהול נוספת.
