# Machine-readable Skill Contract

```skill-contract
{
  "identity": {"name": "Engineering Skill", "version": "1.0.0", "purpose": "Turn an approved plan into an implementation-ready technical recommendation without committing code or changing scope automatically."},
  "inputs": {"required": ["project_context", "approved_goals", "approved_scope", "current_phase", "constraints", "resources", "owners", "project_plan", "existing_decisions"], "optional": ["architecture", "technical_context", "risks", "decisions_needed"]},
  "execution_rules": {"recommendations_require_label": true, "implementation_requires_human_approval": true, "do_not_change_scope_automatically": true, "do_not_commit_code_automatically": true},
  "outputs": {"required": ["findings", "implementation_plan", "work_items", "technical_recommendations", "risks", "decisions_needed", "engineering_artifact"]},
  "validation_rules": {"list_fields": ["findings", "work_items", "technical_recommendations", "risks", "decisions_needed"]}
}
```

# Skill Definition — Engineering Skill

הסקיל הופך תוכנית מאושרת להמלצה טכנית, פירוק עבודה וקריטריוני ביצוע. הוא אינו
כותב קוד, אינו משנה Scope ואינו מתחייב למשאבים ללא אישור אנושי.
