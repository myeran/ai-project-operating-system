# Skill Definition — Product Strategy Skill

## 1. Skill Identity

- **Skill Name:** Product Strategy Skill
- **Category:** Product / Business
- **Purpose:** הגדרת כיוון מוצר, ערך, מטרות וסדרי עדיפויות.
- **Responsibility:** חיבור בין בעיית המשתמש, ערך עסקי, חלופות ומטרות מוצר.
- **Owner:** Skill Owner; פועל תחת Project Orchestrator.

## 2. Activation Rules

- **Lifecycle Phases:** Strategy; Discovery או Planning לפי צורך.
- **Project Types:** פרויקטים הכוללים מוצר, שירות או שינוי בעל ערך למשתמש.
- **Activation Need:** נדרש כיוון, בחירת חלופה, הגדרת ערך או תיעדוף מטרות.
- **Do Not Activate When:** המטרות והכיוון אושרו ואינם דורשים ניתוח נוסף.

## 3. Inputs

- Project Context.
- Discovery Findings.
- Goals and Stakeholder Needs.
- Constraints and Scope.
- Existing Decisions.
- Research and Available Knowledge.

## 4. Process

1. סיכום הבעיה והערך המבוקש.
2. גיבוש חלופות אסטרטגיות.
3. ניתוח יתרונות, חסרונות וסיכונים.
4. הצעת מטרות, עקרונות וסדרי עדיפויות.
5. הכנת המלצה לאישור אנושי.

## 5. Outputs

- Findings.
- Strategic analysis.
- Options considered.
- Recommendations.
- Risks.
- Decisions Needed.
- Product strategy artifact.

## 6. Dependencies

- **Skills:** Discovery, Research, Market Analysis, Finance לפי צורך.
- **Documents:** Project Brief, Discovery Summary, Decision Log.
- **External Tools:** כלי ניתוח מאושרים.
- **Human Experts:** בעלי עניין עסקיים או מוצריים.

## 7. Limitations

- **Does Not Do:** אינו מאשר שינוי מטרות או Scope ואינו מחליף את בעל הפרויקט.
- **Escalate When:** קיימת בחירה אסטרטגית משמעותית, השפעה כספית או סתירה במטרות.
- **Responsibility Boundaries:** מציע כיוון; Human Owner מאשר החלטות אסטרטגיות.

## 8. Quality Criteria

- הערך והבעיה מחוברים.
- קיימות חלופות והשוואה ביניהן.
- מטרות ניתנות להבנה ולתיעוד.
- סיכונים והנחות גלויים.

```skill-contract
{
  "identity": {
    "name": "Product Strategy Skill",
    "version": "1.0.0",
    "purpose": "Define product direction, value, goals, and strategic options from validated project context."
  },
  "inputs": {
    "required": [
      "project_context",
      "discovery_findings",
      "goals",
      "constraints",
      "existing_decisions",
      "available_knowledge"
    ]
  },
  "execution_rules": {
    "recommendations_require_label": true,
    "decisions_require_explicit_approval": true,
    "do_not_change_scope_automatically": true
  },
  "outputs": {
    "required": [
      "findings",
      "strategic_analysis",
      "options_considered",
      "recommendations",
      "risks",
      "decisions_needed",
      "strategy_artifact"
    ]
  },
  "validation_rules": {
    "list_fields": [
      "findings",
      "options_considered",
      "recommendations",
      "risks",
      "decisions_needed"
    ]
  }
}
```
