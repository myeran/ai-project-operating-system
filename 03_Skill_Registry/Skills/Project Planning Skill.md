# Machine-readable Skill Contract

```skill-contract
{
  "identity": {
    "name": "Project Planning Skill",
    "version": "1.0.0",
    "purpose": "Turn an approved direction into an actionable plan with work breakdown, sequencing, dependencies, resources, risks, and decisions needed."
  },
  "inputs": {
    "required": [
      "project_context",
      "approved_goals",
      "approved_scope",
      "current_phase",
      "constraints",
      "resources",
      "owners",
      "existing_decisions",
      "risks",
      "dependencies"
    ],
    "optional": ["available_knowledge", "work_breakdown", "milestones", "recommendations", "decisions_needed"]
  },
  "execution_rules": {
    "recommendations_require_label": true,
    "plan_requires_human_approval": true,
    "do_not_change_scope_automatically": true,
    "do_not_commit_resources_automatically": true
  },
  "outputs": {
    "required": [
      "findings",
      "work_breakdown",
      "sequencing",
      "recommendations",
      "risks_and_dependencies",
      "decisions_needed",
      "project_plan_artifact"
    ]
  },
  "validation_rules": {
    "list_fields": [
      "findings",
      "work_breakdown",
      "sequencing",
      "recommendations",
      "risks_and_dependencies",
      "decisions_needed"
    ]
  }
}
```

# Skill Definition — Project Planning Skill

## 1. Skill Identity

- **Skill Name:** Project Planning Skill
- **Category:** Business / Operational
- **Purpose:** הפיכת כיוון מאושר לתוכנית עבודה ישימה.
- **Responsibility:** פירוק עבודה, תלויות, משאבים, סדרי עדיפויות ותכנון זמנים.
- **Owner:** Skill Owner; פועל תחת Project Orchestrator.

## 2. Activation Rules

- **Lifecycle Phases:** Planning; Execution לפי צורך בעדכון התוכנית.
- **Project Types:** כל פרויקט הדורש תיאום, תלויות או הקצאת משאבים.
- **Activation Need:** יש כיוון מאושר אך אין דרך עבודה ברורה.
- **Do Not Activate When:** מדובר במשימה פשוטה וישירה שאינה דורשת תוכנית נפרדת.

## 3. Inputs

- Project Context.
- Approved Goals and Scope.
- Current Phase.
- Constraints.
- Resources and Owners.
- Existing Decisions.
- Risks and Dependencies.

## 4. Process

1. פירוק המטרה לתוצרים ומשימות.
2. זיהוי בעלים, תלויות ומשאבים.
3. הצעת סדר ביצוע ואבני דרך.
4. שילוב סיכונים וחסמים צפויים.
5. הכנת תוכנית ברמת עומק התואמת לפרויקט.

## 5. Outputs

- Findings.
- Work breakdown and sequencing.
- Recommendations.
- Risks and Dependencies.
- Decisions Needed.
- Project plan artifact.

## 6. Dependencies

- **Skills:** Risk Assessment, Domain Planning לפי צורך.
- **Documents:** Project Brief, Project State, Decision Log.
- **External Tools:** כלי ניהול משימות מאושרים.
- **Human Experts:** בעלי משימות ומשאבים.

## 7. Limitations

- **Does Not Do:** אינו מאשר תקציב, Scope או התחייבויות של בעלי משאבים.
- **Escalate When:** אין משאבים, קיימת תלות קריטית או נדרשת החלטה אסטרטגית.
- **Responsibility Boundaries:** מציע תוכנית; ה־Orchestrator מנהל סטטוסים ומעברים.

## 8. Quality Criteria

- התוכנית מחוברת למטרות ול־Scope המאושרים.
- משימות, בעלים ותלויות ברורים.
- סיכונים וחסמים מרכזיים נכללים.
- עומק התוכנית אינו גדול מהנדרש.
