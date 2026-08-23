# Machine-readable Skill Contract

```skill-contract
{
  "identity": {
    "name": "Discovery Skill",
    "version": "1.1.0",
    "purpose": "Understand and validate the problem, users, assumptions, and unknowns before product direction is defined."
  },
  "inputs": {
    "required": ["project_name", "current_phase", "project_context"],
    "optional": ["project_description", "known_information", "missing_information", "open_questions", "goals", "constraints", "existing_decisions", "confirmed_findings", "assumptions", "decisions", "user_needs", "initial_scope", "risks", "validation_required"]
  },
  "execution_rules": {
    "initial_discovery_priorities": ["understand_problem", "understand_users", "identify_assumptions", "identify_unknowns", "define_validation_needs"],
    "do_not_propose_final_product_direction_before_validation": true,
    "default_problem_statement": "Not yet established; user validation is required.",
    "default_recommended_next_action": "Answer the Discovery questions and provide evidence before defining product direction.",
    "initial_validation_required": [
      "Validate the problem with evidence from users or the existing workflow.",
      "Validate the first target user and the situation in which the problem occurs.",
      "Define the minimum evidence required before product direction is considered."
    ],
    "initial_discovery_questions": [
      {"question": "What problem are we trying to solve?", "why_it_matters": "A clear problem is required before evaluating solutions.", "required_validation": "Describe the current problem using project evidence or user input."},
      {"question": "Who experiences this problem first?", "why_it_matters": "The affected user determines whose needs must be validated.", "required_validation": "Identify the first target user and their context."},
      {"question": "How is the problem solved today?", "why_it_matters": "The current alternative provides the baseline for understanding the problem.", "required_validation": "Document the existing workflow or workaround."},
      {"question": "What is frustrating or insufficient about the current approach?", "why_it_matters": "The unmet need must be understood before defining scope.", "required_validation": "Provide evidence of the current limitation or friction."},
      {"question": "What would count as evidence that the problem was solved?", "why_it_matters": "Success must be testable before strategy or execution begins.", "required_validation": "Define the minimum evidence needed to validate the problem and outcome."}
    ]
  },
  "outputs": {
    "required": ["problem_statement", "confirmed_findings", "assumptions", "decisions", "user_needs", "initial_scope", "open_questions", "risks", "validation_required", "recommended_next_action"]
  },
  "validation_rules": {
    "list_fields": ["confirmed_findings", "assumptions", "decisions", "user_needs", "open_questions", "validation_required"],
    "decisions_require_explicit_approval": true,
    "open_questions_require_fields": ["question", "why_it_matters", "required_validation"]
  }
}
```

# Skill Definition — Discovery Skill

## 1. Skill Identity

- **Skill Name:** Discovery Skill
- **Category:** Discovery
- **Purpose:** הבנת הבעיה, המשתמשים והצורך לפני ביצוע פתרון.
- **Responsibility:** ניסוח הבעיה, זיהוי משתמשים ובעלי עניין, והצפת שאלות פתוחות.
- **Owner:** Skill Owner; פועל תחת Project Orchestrator.

## 2. Activation Rules

- **Lifecycle Phases:** Discovery; לפי צורך גם Strategy.
- **Project Types:** כל סוגי הפרויקטים, בעומק המותאם למורכבות.
- **Activation Need:** מטרה לא ברורה, בעיה לא מאומתת, משתמשים לא ידועים או צורך בהבנת הקשר.
- **Do Not Activate When:** הבעיה, המשתמשים והצורך כבר מתועדים ומאומתים במידה מספקת.

## 3. Inputs

- Project Context.
- Goals.
- Stakeholders and known users.
- Constraints.
- Current Phase.
- Existing Decisions.
- Available Knowledge.

## 4. Process

1. איסוף המידע הקיים.
2. ניסוח הבעיה והצורך על בסיס מידע נתמך בלבד.
3. הפרדה בין Confirmed Findings, Assumptions ו־Decisions.
4. זיהוי משתמשים, בעלי עניין והנחות.
5. איתור פערי מידע ושאלות פתוחות.
6. סיווג סיכונים לפי רמת הוודאות.
7. הגדרת Validation Required וגיבוש המלצה להמשך.

## 5. Outputs

כל Discovery Output חייב לכלול את המבנה הבא:

```markdown
Discovery Summary

1. Problem Statement

2. Confirmed Findings

3. Assumptions

4. Decisions

5. User Needs

6. Initial Scope

7. Open Questions

8. Risks

9. Validation Required

10. Recommended Next Action
```

### 5.1 Confirmed Findings

כלול רק מידע הנתמך על ידי User Input, Project Evidence, Research או מידע מאומת אחר.

לכל Finding יש לציין מקור או בסיס אימות. לדוגמה:

- Users save recipes from multiple sources. **Source:** user interview.
- Existing workflow requires manual copying. **Source:** project evidence.

### 5.2 Assumptions

כלול טענות שטרם אומתו. כל Assumption חייב לכלול:

- **Assumption** — מה מניחים.
- **Why It Exists** — על מה היא נשענת.
- **How to Validate** — כיצד ניתן לאמת או להפריך אותה.

אין להציג Assumption כ־Finding או כ־Decision.

### 5.3 Decisions

כלול רק החלטות שאושרו במפורש על ידי Project Owner או בעל הסמכות שהוגדר.

לכל Decision יש לתעד:

- **Decision**
- **Owner**
- **Date**
- **Reason**
- **Impact**

אם לא התקבלה החלטה מאושרת, יש לכתוב `None identified` או להעביר את הנושא ל־Open Questions / Decisions Needed. Discovery אינו הופך Finding או Assumption ל־Decision.

### 5.4 Open Questions

כל שאלה פתוחה כוללת:

- **Question**
- **Why It Matters**
- **Required Validation**

### 5.5 Risks

יש להפריד בין:

- **Confirmed Risks** — סיכון הנתמך במידע או באירוע קיים.
- **Potential Risks** — סיכון אפשרי שטרם אומת.
- **Unknown Risks Requiring Validation** — תחום שבו חסר מידע כדי להעריך סיכון.

### 5.6 Validation Required

רשום את הבדיקות, המקורות או האישור הנדרשים כדי להפוך Assumption לידע מאומת או כדי לאפשר החלטה.

### 5.7 Recommended Next Action

המלצה תפעולית ברורה להמשך. היא אינה Decision ואינה מחליפה אישור אנושי.

## 6. Dependencies

- **Skills:** Research, Customer Insight לפי צורך.
- **Documents:** Project Brief, Project State, Decision Log.
- **External Tools:** כלי מחקר שאושרו לפרויקט.
- **Human Experts:** משתמשים או בעלי עניין לפי צורך.

## 7. Limitations

- **Does Not Do:** אינו מאשר מטרות אסטרטגיות ואינו בוחר פתרון סופי.
- **Decision Boundary:** אינו יוצר Decision מתוך Finding, Assumption או Recommendation. Decision נרשם רק לאחר אישור מפורש.
- **User-Facing Boundary:** אינו מנחה את המשתמש לגבי פעולת Phase, אינו מנהל מעבר Phase ואינו מחזיר Phase Guidance ישירות. הוא מחזיר Structured Output ל־Lifecycle Orchestrator.
- **Escalate When:** חסר מידע קריטי או קיימת סתירה בין מקורות.
- **Responsibility Boundaries:** מחזיר הבנה והמלצות; ה־Orchestrator משלב ומנהל מעבר Phase.

## 8. Quality Criteria

- הבעיה והמשתמשים מנוסחים בבירור.
- Confirmed Findings, Assumptions ו־Decisions מופרדים ללא ערבוב.
- כל Assumption כולל דרך אימות.
- כל Decision כולל Owner, Date, Reason ו־Impact ואישור מפורש.
- בעלי עניין ופערי מידע מזוהים.
- Risks מסווגים לפי רמת הוודאות.
- ההמלצה להמשך ניתנת להסבר ואינה מחליפה אישור אנושי.

## 9. Classification Examples

הדוגמאות הבאות ממחישות את הגבול בין סוגי המידע:

| Category | Example | Meaning |
|---|---|---|
| Finding | “Users save recipes from multiple sources.” | מידע שנצפה או אומת. |
| Assumption | “Users want automatic import from social networks.” | השערה שדורשת Validation. |
| Decision | “We will build Instagram import in MVP.” | החלטה רק לאחר אישור מפורש של בעל הפרויקט. |

אין להעביר את ה־Assumption או את ה־Finding ל־Decisions ללא אישור מתאים.
