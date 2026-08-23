# Machine-readable Skill Contract

```skill-contract
{
  "identity": {"name": "Documentation Skill", "version": "1.0.0", "purpose": "Organize project information into a focused, maintainable record with a clear source of truth."},
  "inputs": {"required": ["project_context", "current_phase", "source_material", "existing_decisions", "available_knowledge", "destination", "document_purpose"], "optional": ["known_artifacts", "recommendations", "decisions_needed"]},
  "execution_rules": {"recommendations_require_label": true, "source_of_truth_is_required": true, "do_not_create_document_without_purpose": true, "do_not_overwrite_authoritative_content_automatically": true},
  "outputs": {"required": ["findings", "documentation_analysis", "recommendations", "knowledge_risks", "decisions_needed", "documentation_artifact"]},
  "validation_rules": {"list_fields": ["findings", "recommendations", "knowledge_risks", "decisions_needed"]}
}
```

# Skill Definition — Documentation Skill

## 1. Skill Identity

- **Skill Name:** Documentation Skill
- **Category:** Operational
- **Purpose:** יצירת ושמירת ידע בצורה עקבית, קצרה ושימושית.
- **Responsibility:** הפיכת מידע, החלטות ותוצרים למסמכים במבנה ובמיקום הנכונים.
- **Owner:** Skill Owner; פועל תחת Project Orchestrator.

## 2. Activation Rules

- **Lifecycle Phases:** כל ה־Phases כאשר נדרש תיעוד בעל ערך.
- **Project Types:** כל פרויקט, בעומק המותאם לצורך.
- **Activation Need:** החלטה, תוצר, סיכון, הנחה, שינוי או לקח שדורשים שמירה.
- **Do Not Activate When:** אין שימוש עתידי ברור או שהמידע כבר מתועד במקור אמת מתאים.

## 3. Inputs

- Project Context.
- Current Phase.
- Source material and Outputs.
- Existing Decisions.
- Available Knowledge.
- Required destination and document purpose.

## 4. Process

1. זיהוי מטרת התיעוד ומקור האמת.
2. בדיקת כפילויות ומידע מיושן.
3. ארגון המידע במבנה המתאים.
4. הפרדת עובדות, הנחות, החלטות והמלצות.
5. יצירה או עדכון של מסמך ממוקד.

## 5. Outputs

- Findings לגבי איכות התיעוד.
- Documentation analysis.
- Recommendations.
- Risks של חוסר או כפילות ידע.
- Decisions Needed.
- Updated or created artifacts.

## 6. Dependencies

- **Skills:** Review, Decision Support לפי צורך.
- **Documents:** Templates, Project Documents, Decision Log, Knowledge Structure.
- **External Tools:** מערכת הקבצים או מאגר הידע הרשמי.
- **Human Experts:** בעלי המסמך או מומחי תוכן לפי צורך.

## 7. Limitations

- **Does Not Do:** אינו יוצר מסמך ללא מטרה ואינו משנה מקור אמת ללא סמכות.
- **Escalate When:** קיימות גרסאות סותרות, בעלות לא ברורה או צורך בשינוי מערכת.
- **Responsibility Boundaries:** מציע או מעדכן תיעוד; ה־Orchestrator מאמת מיקום ותוכן.

## 8. Quality Criteria

- לכל מסמך יש מטרה ברורה.
- אין כפילות מיותרת.
- מקור האמת והמיקום נכונים.
- התיעוד קצר, ברור וניתן לתחזוקה.
