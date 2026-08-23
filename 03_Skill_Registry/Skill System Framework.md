# Skill System Framework

**System:** AI Project Operating System  
**Agent:** Project Orchestrator Agent  
**Phase:** Phase 3 — Skill System  
**Status:** Ready for Framework Review  
**Architecture:** Orchestrator-Centered Layered Hybrid Architecture  
**Guiding Principle:** Minimum Necessary Process  
**System Owner:** ערן

## 1. Skill System Philosophy

Skill הוא יחידת יכולת מקצועית שמספקת ידע, ניתוח או ביצוע בתחום מוגדר.

Skills קיימים כדי:

- להוסיף מומחיות לפי צורך.
- לאפשר ל־Orchestrator להתאים את העבודה לסוג הפרויקט.
- להפריד בין תיאום הפרויקט לבין ביצוע עבודה מקצועית.
- להחזיר תוצרים, ממצאים והמלצות שניתן לאמת ולשלב.
- לאפשר שימוש חוזר ביכולת בלי ליצור בעלות מפוצלת על הפרויקט.

### Skill מול Orchestrator

ה־Orchestrator:

- מנהל את ה־Lifecycle.
- מזהה צורך ומפעיל Skill.
- מספק Context, Scope ותנאי קבלה.
- מאמת את הפלט ומעדכן את המצב הקנוני.
- מנהל החלטות, אישורים והסלמות.

ה־Skill:

- מבצע עבודה בתחום אחריותו.
- מחזיר Findings, Analysis, Recommendations ותוצרים.
- מציף סיכונים, חוסרים ואי־ודאות.
- אינו מנהל את הפרויקט ואינו משנה Scope, Phase או Project State באופן עצמאי.

## 2. Skill Definition Model

כל Skill עתידי יוגדר במבנה אחיד. בשלב זה מוגדר המודל בלבד, לא Skill מלא.

### Skill Identity

- **Name** — שם ייחודי וברור.
- **Purpose** — הערך או הבעיה שה־Skill מספק.
- **Domain** — תחום המומחיות.
- **Responsibility** — סוגי העבודה שבאחריותו.
- **Scope** — מה כלול ומה אינו כלול.
- **Dependencies** — ידע, כלים או יכולות נדרשים.

### Activation Context

- מתי מפעילים את ה־Skill.
- באיזה Lifecycle Phase הוא רלוונטי.
- איזה מצב, פער, סיכון או צורך בפרויקט מצדיקים הפעלה.
- מהו התוצר המצופה מההפעלה.

### Inputs

ה־Skill מקבל, לפי הרלוונטיות:

- Project Context.
- Current Phase ו־Project State.
- Goals ו־Scope.
- Constraints.
- Existing Knowledge.
- Existing Decisions.
- Risk and Dependency Context.
- Task Request.
- Expected Output ו־Acceptance Criteria.

מידע חסר או לא ודאי חייב להיות מסומן ולא מוצהר כעובדה.

### Activities

ה־Skill מתאר את סוג העבודה שהוא מבצע, לדוגמה:

- איסוף או ניתוח מידע.
- הערכת אפשרויות.
- יצירת תוצר מקצועי.
- בדיקת איכות או סיכון בתחום.
- הצגת המלצות והחלטות נדרשות.

### Outputs

ה־Skill מחזיר, לפי הצורך:

- Findings.
- Analysis.
- Recommendations.
- Risks.
- Deliverables.
- Decisions Needed.
- Assumptions.
- Uncertainties.
- Next Steps.
- Handoff ל־Orchestrator.

הפלט חוזר ל־Orchestrator לפי Worker / Skill Contract. רק ה־Orchestrator משלב אותו במצב הקנוני.

## 3. Skill Categories

הקטגוריות הבאות הן קבוצות יכולת ברמה גבוהה בלבד.

### Discovery Skills

- Research.
- Customer Insight.
- Stakeholder Analysis.
- Domain Discovery.

### Business Skills

- Strategy.
- Finance.
- Market Analysis.
- Business Operations.

### Product Skills

- Product Management.
- UX/UI.
- Requirements Analysis.
- Service Design.

### Technical Skills

- Architecture.
- Engineering.
- QA.
- Data or Analytics.

### Risk & Governance Skills

- Legal.
- Compliance.
- Security.
- Privacy.

### Operational Skills

- Marketing.
- Sales.
- Customer Success.
- Launch or Operations.

קטגוריה אינה מחייבת הפעלה. Skill נבחר רק כאשר קיים צורך מוגדר.

## 4. Skill Activation Model

ה־Orchestrator בוחר Skill לפי שילוב של:

- Project Type.
- Lifecycle Phase.
- Risk Level.
- Missing Knowledge.
- Required Output.
- Complexity and Constraints.
- Skill Scope and Dependencies.

### תהליך הפעלה

1. זיהוי פער, צורך או תוצר נדרש.
2. בדיקה האם ניתן לפתור אותו ללא Skill נוסף.
3. בחירת Skill מתאים לפי תחום, Scope ויכולת.
4. הגדרת Task, Context, Input ו־Expected Output.
5. הפעלת ה־Skill תחת ההרשאות והגבולות המתאימים.
6. קבלת הפלט ובדיקתו.
7. שילוב תוצרים רלוונטיים ב־Project Knowledge או Project State.
8. החלטה על המשך, אישור או הסלמה.

### כללי הפעלה

- אין להפעיל Skill רק משום שהוא קיים ברשימה.
- אין להפעיל מספר Skills כאשר אחד מספיק.
- ניתן להפעיל מספר Skills כאשר יש תחומי מומחיות נפרדים או צורך באימות משלים.
- הפעלה חוזרת צריכה להצדיק את הערך הנוסף שלה.
- Skill אינו מאשר Gate או החלטה אסטרטגית בעצמו.

## 5. Skill Relationship With Lifecycle

### Discovery

Skills אפשריים:

- Research.
- Customer Insight.
- Stakeholder Analysis.

מטרתם לספק הבנה, נתונים, נקודות מבט ושאלות פתוחות.

### Strategy

Skills אפשריים:

- Strategy.
- Product Management.
- Market Analysis.
- Finance.

מטרתם לתמוך בהגדרת ערך, כיוון, חלופות וסדרי עדיפויות.

### Planning

Skills אפשריים:

- Project Planning.
- Risk Analysis.
- Resource Planning.
- Domain Planning.

מטרתם לתמוך ב־Scope, תכנית עבודה, משאבים, תלותים וסיכונים.

### Design

Skills אפשריים:

- UX/UI.
- Product Design.
- Architecture.
- Process Design.

מטרתם לתכנן את הפתרון או התהליך כאשר Design נדרש.

### Execution

Skills אפשריים:

- Engineering.
- Content or Operations.
- Domain Execution.
- Project Coordination.

מטרתם ליצור את התוצרים ולנהל את העבודה בתחום הרלוונטי.

### Validation

Skills אפשריים:

- QA.
- Security.
- User Validation.
- Domain Review.
- Analytics.

מטרתם לבדוק איכות, התאמה, סיכונים ותנאי קבלה.

### Launch

Skills אפשריים:

- Release or Launch Management.
- Operations.
- Marketing.
- Communications.
- Customer Success.

מטרתם להכין ולבצע מעבר לשימוש או השפעה חיצונית.

### Learning

Skills אפשריים:

- Retrospective.
- Analysis.
- Knowledge Management.
- Domain Review.

מטרתם להפיק Lessons Learned, Best Practices והצעות שיפור.

## 6. Skill Governance

### הוספת Skill

Skill חדש מוצע כאשר:

- קיים צורך חוזר או משמעותי.
- האחריות אינה מכוסה היטב על ידי Skill קיים.
- קיימת הגדרה ברורה של Purpose, Scope, Inputs ו־Outputs.
- יש ערך שימושי לפרויקטים נוספים.

System Owner מאשר הוספה ל־Skill Registry. ה־Orchestrator יכול להציע Skill חדש אך אינו מאשר אותו לבדו.

### בדיקת איכות Skill

לפני שימוש חוזר יש לבדוק:

- אחריות ברורה.
- גבולות ללא חפיפה.
- Input ו־Output שימושיים.
- התאמה ל־Lifecycle ולחוזה העבודה.
- יכולת להחזיר אי־ודאות, סיכונים והחלטות נדרשות.
- שמירה על בעלות ה־Orchestrator על Project State.

### עדכון Skill

עדכון נדרש כאשר:

- האחריות השתנתה.
- הפלט אינו שימושי.
- נוצרה חפיפה עם Skill אחר.
- השתנו כללי המערכת או ה־Lifecycle.
- נלמד לקח שמצדיק שיפור.

שינוי משמעותי מתועד ומאושר לפי תהליך שינוי System Knowledge.

### הסרת Skill

ניתן להסיר או לאחד Skill כאשר:

- אין בו שימוש חוזר.
- האחריות שלו כפולה.
- הוא אינו מייצר ערך ברור.
- ניתן להשיג את אותה תוצאה בצורה פשוטה יותר.
- הוא אינו עומד בחוזה או יוצר סיכון.

אין להסיר Skill רק בגלל שלא הופעל בפרויקט יחיד.

## 7. Skill Ownership

### Skill Owner

אחראי על:

- איכות ה־Skill.
- תחזוקת הידע הרלוונטי.
- עדכון שיטות העבודה בתחום.

### Project Orchestrator

אחראי על:

- זיהוי הצורך.
- בחירת Skill מתאים.
- הפעלת Skill בזמן הנכון.
- וידוא שהתוצר משתלב בפרויקט.

### System Owner

אחראי על:

- אישור שינויי Framework.
- אישור הוספה או הסרה של Skills מערכתיים.

## 8. Skill Maturity

Skills יכולים להתפתח ברמות שונות לאורך זמן:

- **Level 1 — Basic Capability:** יכולת בסיסית לביצוע משימה מוגדרת.
- **Level 2 — Defined Professional Capability:** יכולת מקצועית עם אחריות, Input ו־Output מוגדרים.
- **Level 3 — Advanced Capability:** יכולת מתקדמת הנשענת גם על ידע וניסיון מצטבר.

זהו עיקרון הרחבה עתידי בלבד. בשלב זה לא מוגדרת מערכת דירוג מלאה, ואין להשתמש ברמה כתנאי אוטומטי להפעלת Skill.

## 9. Anti-Bureaucracy Rules

- לא ליצור Skill ללא צורך חוזר.
- לא ליצור Skill עבור משימה חד־פעמית.
- לא לשכפל אחריות בין Skills.
- כל Skill חייב להחזיר ערך ברור.
- מספר ה־Skills יישמר מינימלי אך מספיק לצורכי המערכת.
- אין להפעיל Skill כאשר ניתן לבצע את העבודה בפשטות ללא מומחיות נוספת.
- אין ליצור קטגוריות או Registry entries ללא שימוש מעשי.
- יש להעדיף Skill קיים ומתאים על פני יצירת Skill חדש.
- עומק ההפעלה מותאם למורכבות ולסיכון של הפרויקט.

## גבולות השלב

בשלב זה לא נוצרים:

- Skill Definitions מלאים.
- Templates.
- Automation.
- Worker Implementation.

נושאים אלה יטופלו בשלבים הבאים.

## Alignment with Existing System

המסגרת תואמת ל־Architecture Blueprint בכך שה־Capability Layer מספק יכולות, בעוד ה־Orchestrator נשאר נקודת התיאום ובעל המצב הקנוני.

המסגרת תואמת ל־System Contracts בכך שכל Skill מקבל Input מוגדר ומחזיר Output לפי חוזה עבודה אחיד.

המסגרת תואמת ל־Lifecycle בכך שהפעלת Skill נקבעת לפי Phase, צורך, סיכון ותוצר נדרש.

המסגרת תואמת ל־Operating Rules ול־Minimum Necessary Process בכך שאין מפעילים או יוצרים Skills ללא ערך ברור.

המסגרת תואמת ל־Decision Framework בכך ש־Skills מציעים, מנתחים ומציפים; החלטות אסטרטגיות ואישורים נשארים באחריות האדם וה־Orchestrator.
