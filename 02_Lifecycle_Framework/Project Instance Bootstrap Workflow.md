# Project Instance Bootstrap Workflow

**System:** AI Project Operating System  
**Role:** Project Instance Bootstrap Workflow  
**Entry:** Start New Project → New Project Confirmed  
**Handoff:** Lifecycle Orchestrator Worker  
**Canonical State:** `00_Architecture/ACTIVE/system-contracts-and-state-model.md`
**Architecture Decision:** `00_Architecture/ACTIVE/project-instance-architecture-decisions-record.md`
**Guiding Principle:** Minimum Necessary Process

## 1. Purpose

Workflow זה יוצר Project Instance חדש על גבי AI Project Operating System, מאתחל את סביבת העבודה ואת ה־Project State הקנוני, רושם את הפרויקט ב־Project Registry ומקשר אליו את יכולות ה־OS המאושרות.

ה־Workflow אינו מבצע Discovery, אינו יוצר Skills או Workers חדשים ואינו משנה את מודל ה־Project State.

## 2. Trigger

הפעל לאחר שכל התנאים הבאים מתקיימים:

1. התקבלה בקשת `Start New Project: [Name]` או בקשה טבעית מקבילה.
2. Project Entry Point זיהה Intent של New Project.
3. Project Existence Check הסתיים.
4. לא נמצא פרויקט קיים, או שהמשתמש אישר במפורש יצירת Project Instance נפרד במקרה של Similar Project.
5. קיים Project Name או שם עבודה זמני.

אם נמצא פרויקט קיים ללא החלטת משתמש, אין להפעיל Bootstrap.

## 3. Bootstrap Flow

```text
New Project Request
        ↓
Project Existence Check
        ↓
User Confirmation, אם נדרש
        ↓
Create Project Identity
        ↓
Bind OS Version
        ↓
Create Project Registry Entry
        ↓
Create Minimal Project Workspace
        ↓
Initialize Canonical Project State
        ↓
Attach Shared OS Capabilities
        ↓
Handoff to Lifecycle Orchestrator
        ↓
Discovery / Project Initiation Workflow
```

## 4. Step 1 — Create Project Identity

צור:

- `project_id` יציב וייחודי.
- Project Name.
- Description, רק אם סופק.
- Project Owner, רק אם ידוע או אושר.
- Created Date.

אין להמציא Owner, Goals, Scope, Stakeholders, Risks או Dependencies.

## 5. Step 2 — Bind OS Version

קבע את גרסת ה־OS של ה־Project Instance לפי המודל ההיברידי המאושר:

- `os_version_at_creation` — גרסת ה־OS בעת יצירת הפרויקט.
- `os_version_current` — הגרסה שהפרויקט משתמש בה בפועל.
- `os_upgrade_status` — ללא שדרוג פעיל בעת יצירה.

הפרויקט מקבל Reference או גישה מבוקרת ל־Frameworks, Skills, Workers, Templates, Contracts ו־Governance. אין להעתיק סמכות מערכת או Project Knowledge מפרויקטים אחרים.

## 6. Step 3 — Register Project

צור רשומת Project Registry קנונית עם השדות שהוגדרו בהחלטת הארכיטקטורה:

```yaml
project_registry_entry:
  project_id: <stable unique id>
  project_name: <name>
  owner: <human owner or pending confirmation>
  status: proposed
  current_phase: Discovery
  os_version: <current bound OS version>
  location: <canonical project workspace reference>
  created_date: <date>
  last_activity: <timestamp>
```

Project Registry הוא אינדקס ואינו מחליף את Project State המלא או את Project Knowledge.

## 7. Step 4 — Create Minimal Workspace

צור רק את מבנה הבסיס הנדרש:

```text
[Project Name]/
├── 00_Project_Context/
├── 01_Discovery/
└── Evidence/
```

תיקיות נוספות נוצרות כאשר Lifecycle Orchestrator מפעיל את השלבים הרלוונטיים. אין ליצור מראש מסמכים או תיקיות שאינם נדרשים.

## 8. Step 5 — Initialize Canonical Project State

אתחל Project State לפי המודל הקיים בלבד. ערכי הכניסה הם:

- `project_identity.project_id`: ה־ID שנוצר.
- `project_identity.name`: שם הפרויקט.
- `project_identity.description`: תיאור שסופק, או ריק.
- `project_identity.owner`: Owner שסופק, או Pending Confirmation.
- `project_identity.stakeholders`: ריק עד לאיסוף.
- `current_status.current_phase`: `Discovery`.
- `current_status.status`: `proposed`.
- `current_status.progress`: `0`.
- `current_status.blockers`: ריק, אלא אם קיים Blocker אמיתי.
- `planning_data.goals`: ריק עד Discovery או אישור.
- `planning_data.scope.in_scope`: ריק.
- `planning_data.scope.out_of_scope`: ריק.
- `planning_data.scope.change_history`: ריק.
- `planning_data.timeline`: ריק.
- `planning_data.resources`: ריק.
- `decision_management.decisions`: ריק.
- `decision_management.pending_decisions`: ריק.
- `decision_management.approvals`: ריק.
- `risk_management.risks`: רק Risks שסופקו או זוהו; אחרת ריק.
- `risk_management.dependencies`: רק Dependencies שסופקו או זוהו; אחרת ריק.
- `risk_management.issues`: ריק.
- `knowledge.documents`: תוצרי Bootstrap בלבד, אם נוצרו.
- `knowledge.outputs`: תוצרי Bootstrap בלבד, אם נוצרו.
- `knowledge.lessons_learned`: ריק.
- `next_actions.tasks`: Handoff ל־Lifecycle Orchestrator / Discovery.
- `next_actions.owners`: Owner ידוע בלבד.
- `next_actions.due_dates`: תאריך ידוע או מאושר בלבד.
- `audit`: Actor, Timestamp, Version ו־History Reference.

אין להוסיף שדות ל־Project State ואין להשתמש בשדות Registry במקום שדות State.

## 9. Step 6 — Attach Shared OS Capabilities

קשר את ה־Project Instance ליכולות קיימות בלבד:

- Lifecycle Framework.
- Project Initiation Workflow.
- Discovery Skill.
- Project Brief Template.
- Phase Guidance Output Contract.
- Decision, Risk, Knowledge ו־Review Rules לפי הצורך.

הקישור אינו מפעיל Discovery בתוך Bootstrap. הוא מכין את ה־Context וה־Handoff להפעלה על ידי Lifecycle Orchestrator.

## 10. Step 7 — Handoff to Lifecycle Orchestrator

לאחר Bootstrap החזר ל־Lifecycle Orchestrator:

```yaml
bootstrap_handoff:
  status: completed | partial | blocked | escalated
  project_id: <project id>
  project_name: <project name>
  current_phase: Discovery
  project_status: proposed
  os_version: <current bound OS version>
  registry_entry_created: true | false
  workspace_created: true | false
  project_state_initialized: true | false
  attached_capabilities:
    - Lifecycle Framework
    - Project Initiation Workflow
    - Discovery Skill
    - Project Brief Template
  missing_information: []
  risks: []
  next_action: Activate Project Initiation Workflow and Discovery
```

Lifecycle Orchestrator הוא בעל התגובה למשתמש לגבי Phase, Validation, Required User Action ו־Completion Criteria.

## 11. Bootstrap Completion Criteria

Bootstrap נחשב שלם כאשר:

- Project Existence Check עבר.
- נוצר Project ID יציב.
- נקשרה גרסת OS.
- נוצר Project Registry Entry.
- נוצר Workspace מינימלי.
- נוצר Project State קנוני תקין.
- ה־Project Instance מתחיל ב־Discovery עם `status: proposed`.
- לא הועתק Project Knowledge מפרויקט אחר.
- Handoff ל־Lifecycle Orchestrator נוצר.

## 12. Escalation Rules

עצור והסלם כאשר:

- קיימת התאמה לפרויקט קיים ולא התקבלה החלטת משתמש.
- לא ניתן ליצור Project ID ייחודי.
- לא ניתן לקבוע OS Version תקפה.
- Project Registry אינו זמין או מכיל סתירה.
- לא ניתן ליצור Project State קנוני תקין.
- קיימת סתירה בין Project Registry, Project State או מקור אמת.
- נדרש שיתוף מידע מפרויקט אחר.
- נדרש שינוי ב־OS, Contract או State Model.

פורמט הסלמה:

```text
Issue:
Context:
Impact:
Options:
Recommendation:
Decision Needed:
```

## 13. User-Facing Bootstrap Response

Bootstrap מחזיר ל־Entry Point נתוני אתחול בלבד:

```text
## Project Bootstrap

Project: [Name]
Project ID: [ID]
Status: proposed
Current Phase: Discovery
OS Version: [Version]
Workspace: Created / Partial / Blocked
Project Registry: Registered / Pending / Blocked

Handoff:
Lifecycle Orchestrator will now start Project Initiation and Discovery.
```

התגובה אינה מחליפה את Phase Guidance Output Contract. כל הנחיה למשתמש לגבי מה לעשות ב־Discovery נוצרת לאחר ה־Handoff על ידי Lifecycle Orchestrator.

## 14. Boundaries

Bootstrap אינו:

- Discovery Process.
- Project Brief מלא.
- Project Planning.
- OS Upgrade.
- Knowledge Sharing Process.
- שינוי Project State Model.
- יצירת Skill או Worker.
