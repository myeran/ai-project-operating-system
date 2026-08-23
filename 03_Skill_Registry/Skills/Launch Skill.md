# Machine-readable Skill Contract

```skill-contract
{
  "identity": {"name": "Launch Skill", "version": "1.0.0", "purpose": "Prepare a controlled launch recommendation with readiness checks, rollout steps, risks, and rollback considerations."},
  "inputs": {"required": ["project_context", "approved_goals", "approved_scope", "current_phase", "constraints", "resources", "owners", "release_artifact", "existing_decisions"], "optional": ["validation_results", "launch_requirements", "known_risks", "decisions_needed"]},
  "execution_rules": {"recommendations_require_label": true, "launch_requires_human_approval": true, "do_not_release_automatically": true, "rollback_plan_is_required": true},
  "outputs": {"required": ["findings", "readiness_checks", "rollout_plan", "rollback_plan", "risks", "decisions_needed", "launch_artifact"]},
  "validation_rules": {"list_fields": ["findings", "readiness_checks", "rollout_plan", "rollback_plan", "risks", "decisions_needed"]}
}
```

# Skill Definition — Launch Skill

הסקיל מכין המלצת השקה מבוקרת. הוא אינו משיק, מפרסם או משנה מערכת חיה ללא
אישור וסמכות נפרדים.
