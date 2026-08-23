# Machine-readable Skill Contract

```skill-contract
{
  "identity": {"name": "Review Skill", "version": "1.0.0", "purpose": "Assess an artifact or phase against requirements, acceptance criteria, risks, and transition conditions."},
  "inputs": {"required": ["project_context", "current_phase", "requirements", "acceptance_criteria", "existing_decisions", "architecture_rules", "artifact", "risks_and_constraints"], "optional": ["review_scope", "decisions_needed"]},
  "execution_rules": {"recommendations_require_label": true, "approval_authority_is_human": true, "do_not_change_state_automatically": true, "block_on_critical_gaps": true},
  "outputs": {"required": ["findings", "quality_analysis", "recommendations", "risks_and_open_issues", "decisions_needed", "review_artifact"]},
  "validation_rules": {"list_fields": ["findings", "recommendations", "risks_and_open_issues", "decisions_needed"]}
}
```

# Skill Definition — Review Skill

## 1. Skill Identity

- **Skill Name:** Review Skill
- **Category:** Technical / Risk & Governance
- **Purpose:** בדיקת איכות, שלמות ותאימות של תוצר או שלב.
- **Responsibility:** בדיקת תוצרים מול דרישות, ארכיטקטורה, סיכונים ותנאי מעבר.
- **Owner:** Skill Owner; פועל תחת Project Orchestrator.

## 2. Activation Rules

- **Lifecycle Phases:** Validation; Phase Reviews; לפני Gates לפי צורך.
- **Project Types:** פרויקטים או תוצרים שבהם בדיקה מוסיפה ערך או מפחיתה סיכון.
- **Activation Need:** תוצר מוכן לבדיקה, מעבר Phase, סיכון משמעותי או צורך באימות.
- **Do Not Activate When:** הפעולה הפיכה, פשוטה ובסיכון נמוך ללא ערך ביקורת נוסף.

## 3. Inputs

- Project Context.
- Current Phase.
- Requirements and Acceptance Criteria.
- Existing Decisions.
- Architecture and Project Rules.
- Artifact under review.
- Known Risks and Constraints.

## 4. Process

1. הגדרת היקף הבדיקה וקריטריוני הקבלה.
2. בדיקת שלמות, בהירות, עקביות ושימושיות.
3. בדיקת התאמה למסמכי המקור ול־Scope.
4. זיהוי פערים, סיכונים וחסמים.
5. החזרת תוצאה והמלצה: Approved, Approved with Notes, Needs Revision או Blocked.

## 5. Outputs

- Findings.
- Quality analysis.
- Recommendations.
- Risks and Open Issues.
- Decisions Needed.
- Review artifact or review record.

## 6. Dependencies

- **Skills:** Risk Assessment, Documentation, Domain Review לפי צורך.
- **Documents:** Requirements, Phase Review Gate Framework, Decision Log.
- **External Tools:** כלי בדיקה רלוונטיים.
- **Human Experts:** מומחי תחום כאשר נדרשת סמכות מקצועית.

## 7. Limitations

- **Does Not Do:** אינו מאשר החלטה אסטרטגית ואינו מחליף בעל אישור אנושי.
- **Escalate When:** קיים חסם, סיכון גבוה, סתירה או חסר קריטי.
- **Responsibility Boundaries:** מספק ממצאי ביקורת; ה־Orchestrator קובע את פעולת ההמשך.

## 8. Quality Criteria

- הבדיקה קשורה לקריטריונים מוגדרים.
- הממצאים ספציפיים וניתנים לפעולה.
- חסמים מופרדים מהמלצות עתידיות.
- עומק הבדיקה מותאם לסיכון ואינו יוצר בירוקרטיה.
