# Skill Definition — Risk Assessment Skill

## 1. Skill Identity

- **Skill Name:** Risk Assessment Skill
- **Category:** Risk & Governance
- **Purpose:** זיהוי, הערכה ותיעוד של סיכונים העלולים להשפיע על הפרויקט.
- **Responsibility:** ניתוח הסתברות, השפעה, דחיפות, תלות ואפשרויות mitigation.
- **Owner:** Skill Owner; פועל תחת Project Orchestrator.

## 2. Activation Rules

- **Lifecycle Phases:** Discovery, Strategy, Planning, Validation, Launch; לפי צורך בכל Phase.
- **Project Types:** כל פרויקט; בעומק לפי רמת הסיכון.
- **Activation Need:** שינוי משמעותי, אי־ודאות, תלות קריטית, רגולציה, כסף, אבטחה או פעולה בלתי הפיכה.
- **Do Not Activate When:** אין שינוי או סיכון חדש והבדיקה הקיימת עדיין תקפה.

## 3. Inputs

- Project Context.
- Goals, Scope and Constraints.
- Current Phase.
- Existing Decisions.
- Dependencies and Issues.
- Available Knowledge.
- Known legal, financial, security or operational context.

## 4. Process

1. איתור סיכונים ואיומים.
2. הערכת הסתברות, השפעה ודחיפות.
3. זיהוי בעלים ופעולות mitigation.
4. דירוג רמת הסיכון.
5. הצפת סיכונים המחייבים החלטה או הסלמה.

## 5. Outputs

- Findings.
- Risk analysis and rating.
- Recommendations and mitigation actions.
- Risks.
- Decisions Needed.
- Risk assessment artifact.

## 6. Dependencies

- **Skills:** Security, Legal, Compliance, Privacy לפי צורך.
- **Documents:** Risk Register, Project State, Decision Log.
- **External Tools:** כלי ניתוח או בדיקה מאושרים.
- **Human Experts:** מומחי סיכון רלוונטיים.

## 7. Limitations

- **Does Not Do:** אינו מאשר סיכון גבוה ואינו מחליף ייעוץ משפטי, כספי או מקצועי.
- **Escalate When:** הסיכון גבוה, בלתי הפיך, חסר מידע קריטי או דורש אישור אנושי.
- **Responsibility Boundaries:** מזהה וממליץ; ה־Orchestrator מנהל וה־Human Owner מאשר החלטות משמעותיות.

## 8. Quality Criteria

- סיכונים מנוסחים באופן ברור ומבוסס.
- הסתברות והשפעה מופרדות.
- קיימים בעלים ופעולות מוצעות.
- סיכונים גבוהים מסומנים ומוסלמים בזמן.
