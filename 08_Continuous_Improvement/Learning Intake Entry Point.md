# Learning Intake Entry Point

**System:** AI Project Operating System  
**Role:** Learning Intake Entry Point  
**Routes to:** Project Knowledge / Continuous Improvement Learning Capture Workflow  
**Parent:** Project Orchestrator Agent  
**Guiding Principle:** Minimum Necessary Process

## 1. Purpose

Learning Intake Entry Point הוא נקודת הכניסה ללכידת Observations, Learnings ו־Improvement Opportunities במהלך עבודה על פרויקטים.

הוא מסווג את הלמידה, שומר Evidence ומנתב אותה למקום הנכון. הוא אינו מיישם שיפורים ואינו משנה את מערכת AI Project Operating System ישירות.

## 2. Triggers

הפעל כאשר המשתמש כותב:

- `Capture Learning`
- `Add Learning`
- `Record Improvement`
- `I found a problem in the process`
- `Something should change in the system`

הפעל גם כאשר:

- Phase Review מזהה Learning.
- Pilot מזהה בעיה חוזרת.
- Worker או Skill מדווחים על Capability חסרה.

## 3. Intake Flow

```text
Observation
    ↓
Capture Learning Item
    ↓
Classify: Project Learning / System Improvement
    ↓
Capture Evidence
    ↓
Assess Impact, אם מערכתי
    ↓
Route to Correct Destination
    ↓
Report Status and Next Step
```

## 4. Step 1 — Capture Observation

צור Learning Item ראשוני:

```yaml
learning_item:
  id: <stable learning id>
  source: Project | Review | User Feedback | System Observation
  date: <date>
  observation: <what was observed>
  context: <relevant context>
  evidence: []
  related_project: <project id or name if known>
```

אם פרט אינו ידוע, סמן אותו כחסר. אין להמציא Context, Evidence או קשר לפרויקט.

## 5. Step 2 — Classification

### Project Learning

סווג כ־Project Learning כאשר התובנה חלה על הפרויקט הנוכחי בלבד, כגון:

- User Behavior.
- Product Insight.
- Business Discovery.
- Project Decision.

**Destination:** Project Learning / Project Knowledge.

Project Learning עונה על השאלה: **What did we learn about this project?**

### System Improvement

סווג כ־System Improvement כאשר התובנה עשויה לשפר את אופן ניהול הפרויקטים, כגון:

- Skill חסר.
- Worker חסר.
- Workflow לא ברור.
- Template בעייתי.
- חיכוך משתמשים חוזר.
- Process Inefficiency.

**Destination:** Continuous Improvement Backlog.

System Improvement עונה על השאלה: **What should improve in the AI Project Operating System?**

כאשר הסיווג אינו ודאי, שמור את ה־Observation כ־Project Learning זמני, ציין את אי־הוודאות ובקש רק את ההבהרה הנדרשת.

## 6. Step 3 — Evidence and Impact Assessment

### Evidence Rules

הפרד בין:

- Observation — מה קרה או נאמר.
- Evidence — מה תומך בתצפית.
- Recommendation — מה מוצע לעשות.
- Decision — מה אושר.
- Implementation — מה בוצע בפועל.

אין להפוך Suggestion ל־Improvement Item מערכתי ללא ערך פוטנציאלי או Evidence מינימלי.

### System Improvement Assessment

עבור System Improvement הערך:

#### Scope

- Single Project.
- Multiple Projects.
- Entire System.

#### Affected Component

- Lifecycle.
- Framework.
- Skill.
- Worker.
- Template.
- Knowledge System.
- Automation.
- Process.

#### Impact

תאר בקצרה:

- Benefit.
- Risk.
- Complexity.
- Maintenance Cost.

הערכת ההשפעה אינה אישור לשינוי. היא משמשת לניתוב ולתעדוף.

## 7. Step 4 — Routing

### Project Learning Route

צור Project Learning Record:

```text
Project Learning Record

Learning:
Impact:
Action:
Owner:
```

שמור את הרשומה ב־Project Knowledge וקשר אותה לפרויקט הרלוונטי. אין לעדכן System Knowledge אוטומטית.

### System Improvement Route

צור Improvement Item:

```yaml
improvement_item:
  id: <improvement id>
  source: <source>
  observation: <observation>
  problem: <problem statement>
  evidence: []
  affected_component: <component>
  recommendation: <recommendation>
  priority: Low | Medium | High
  status: Identified
```

שלח את ה־Improvement Item ל־Continuous Improvement Process. הוא נשאר `Identified` עד Analysis, Impact Assessment, Recommendation ואישור לפי המסגרת הקיימת.

## 8. User Response Format

החזר תמיד:

```text
## Learning Captured

Type:
[Project Learning / System Improvement]

Source:
[Project / Review / User Feedback / System Observation]

Observation:

Evidence:

Destination:
[Project Knowledge / Continuous Improvement Backlog]

Recommended Next Step:

Status:
[Captured / Identified / Needs Clarification]
```

אם נדרש מידע נוסף, ציין שאלה ממוקדת אחת והסבר מדוע היא משפיעה על הסיווג או הניתוב.

## 9. Escalation Rules

עצור והסלם כאשר:

- לא ניתן להבין את התצפית.
- אין אפשרות לקבוע לאיזה פרויקט היא קשורה, כאשר הקשר נדרש.
- קיימת סתירה בין Evidence או מקורות.
- נדרש שינוי ישיר ב־System Knowledge.
- נדרש אישור לשינוי Framework, Lifecycle, Skill, Worker או System Core.
- מוצע Merge, מחיקה או שינוי בלתי הפיך.

הסלמה אינה יישום. היא מעבירה את הנושא ל־Review או Approval המתאימים.

## 10. Integration

ה־Entry Point מחובר ל:

- **Continuous Improvement Framework** — למחזור Identify → Analyze → Assess Impact → Recommend → Approve → Implement → Validate.
- **Continuous Improvement Learning Capture Workflow** — לסיווג וליצירת Improvement Item.
- **Improvement Backlog** — לשמירת מועמדי שיפור.
- **Improvement History** — לתיעוד שינויים שאושרו ויושמו.
- **Project Learning / Project Knowledge** — לשמירת למידה ייחודית לפרויקט.

אין ליצור מאגר, Workflow או State Model חדש.

## 11. Anti-Bureaucracy Rules

- לא כל הערה הופכת ל־Improvement Item.
- לא כל Project Learning הופך לשינוי מערכתי.
- יש לשמור רק Learning בעל ערך עתידי ברור.
- יש להעדיף עדכון רכיב קיים על יצירת רכיב חדש.
- יש להעדיף פישוט לפני הרחבה.
- אין ליישם שינוי ללא Review ואישור נדרשים.

## 12. Validation Examples

### Example 1 — Project Learning

```text
Observation: Users want shorter recipes.
Classification: Project Learning
Reason: התובנה מתייחסת להעדפת משתמשים בפרויקט המסוים.
Destination: Project Knowledge
System Change: None
```

### Example 2 — System Improvement

```text
Observation: Users don't know what to do after each phase.
Classification: System Improvement
Reason: הבעיה מתייחסת להכוונת המערכת ועלולה לחזור בפרויקטים נוספים.
Destination: Continuous Improvement Backlog
Next Step: Analyze evidence and propose a minimal Phase Guidance improvement.
System Change: None until Review and Approval.
```

## 13. Success Criteria

Learning Intake Entry Point הצליח כאשר:

- Observation נקלטה עם מקור והקשר.
- Project Learning ו־System Improvement הופרדו נכון.
- Evidence נשמר.
- Project Learning נותב ל־Project Knowledge.
- System Improvement נותב ל־Improvement Backlog.
- לא בוצע שינוי מערכת אוטומטי.
- המשתמש קיבל Destination, Status ו־Next Step ברורים.
