# Machine-readable Skill Contract

```skill-contract
{
  "identity": {
    "name": "UX/UI Skill",
    "version": "1.0.0",
    "purpose": "Translate approved goals and workflows into a usable, accessible, and testable UX/UI recommendation."
  },
  "inputs": {
    "required": [
      "project_context",
      "approved_goals",
      "approved_scope",
      "current_phase",
      "constraints",
      "target_users",
      "user_workflows",
      "existing_decisions",
      "resources"
    ],
    "optional": ["known_risks", "design_system", "user_needs", "interface_recommendations", "decisions_needed"]
  },
  "execution_rules": {
    "recommendations_require_label": true,
    "design_requires_human_approval": true,
    "do_not_change_scope_automatically": true,
    "do_not_commit_implementation_automatically": true,
    "accessibility_is_required": true
  },
  "outputs": {
    "required": [
      "findings",
      "user_needs",
      "information_architecture",
      "user_flows",
      "interface_recommendations",
      "accessibility_risks",
      "decisions_needed",
      "ux_ui_artifact"
    ]
  },
  "validation_rules": {
    "list_fields": [
      "findings",
      "user_needs",
      "information_architecture",
      "user_flows",
      "interface_recommendations",
      "accessibility_risks",
      "decisions_needed"
    ]
  }
}
```

# Skill Definition — UX/UI Skill

## Responsibility

הסקיל מתרגם מטרות, משתמשים וזרימות עבודה להמלצות UX/UI ישימות. הוא אינו משנה
Scope, אינו מאשר עיצוב סופי ואינו מבצע קוד או התחייבות למימוש.

## Outputs

- צרכי משתמש וממצאים.
- ארכיטקטורת מידע וזרימות משתמש.
- המלצות ממשק.
- סיכוני נגישות.
- החלטות נדרשות ותוצר UX/UI להערכה ואישור אנושי.
