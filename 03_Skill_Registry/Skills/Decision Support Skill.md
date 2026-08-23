# Skill Definition — Decision Support Skill

## 1. Skill Identity

- **Skill Name:** Decision Support Skill
- **Category:** Business / Risk & Governance
- **Purpose:** סיוע בניתוח החלטות לפי Decision Framework.
- **Responsibility:** הצגת עובדות, הנחות, חלופות, סיכונים והמלצה ברורה.
- **Owner:** Skill Owner; פועל תחת Project Orchestrator.

## 2. Activation Rules

- **Lifecycle Phases:** כל Phase שבו נדרשת בחירה בין אפשרויות.
- **Project Types:** כל פרויקט עם החלטה בעלת אי־ודאות, השפעה או חלופות.
- **Activation Need:** החלטה לא ברורה, סיכון בינוני או גבוה, התנגשות בין מטרות או צורך בהשוואה.
- **Do Not Activate When:** הפעולה תפעולית, הפיכה וברורה ואינה דורשת ניתוח נוסף.

## 3. Inputs

- Project Context.
- Decision Question.
- Current Phase and Project State.
- Facts and Existing Knowledge.
- Goals, Scope and Constraints.
- Existing Decisions.
- Risk and Dependency Context.

## 4. Process

1. ניסוח שאלת ההחלטה וההקשר.
2. הפרדת Facts, Assumptions ו־Recommendations.
3. זיהוי חלופות וקריטריונים להשוואה.
4. ניתוח השפעה, סיכון, הפיכות ותלותים.
5. הצגת המלצה, החלטה נדרשת ודרך תיעוד.

## 5. Outputs

- Findings.
- Decision analysis.
- Options Considered.
- Recommendations.
- Risks.
- Decisions Needed.
- Decision Record draft.

## 6. Dependencies

- **Skills:** Risk Assessment, Research, Product Strategy לפי צורך.
- **Documents:** Decision Framework, Decision Log, Project State.
- **External Tools:** כלי ניתוח מאושרים.
- **Human Experts:** בעל הפרויקט או מומחה תחום לפי סוג ההחלטה.

## 7. Limitations

- **Does Not Do:** אינו מקבל החלטות אסטרטגיות, כספיות או משפטיות במקום האדם.
- **Escalate When:** נדרש אישור אנושי, הסיכון גבוה, המידע סותר או הפעולה בלתי הפיכה.
- **Responsibility Boundaries:** מסייע בניתוח ומציג המלצה; ה־Human Owner מאשר החלטות שבסמכותו.

## 8. Quality Criteria

- שאלת ההחלטה ברורה.
- Facts, Assumptions ו־Recommendations מופרדים.
- חלופות וסיכונים מוצגים באופן מאוזן.
- רמת הסיכון וסמכות האישור מזוהות.
- ניתן לתעד את ההחלטה ב־Decision Log.
