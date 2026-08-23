# Project Instance Bootstrap Package Document

**System:** AI Project Operating System  
**Package:** Project Instance Bootstrap Package  
**Applies to:** Every new Project Instance  
**Canonical State:** `system-contracts-and-state-model.md`  
**Architecture:** Independent Project Instances on Shared Operating System  
**Guiding Principle:** Minimum Necessary Process

## 1. Purpose

Bootstrap Package מגדירה את חבילת היכולות, הכללים וההפניות שכל Project Instance חדש מקבל בעת יצירתו.

המטרה היא להבטיח שכל פרויקט מתחיל כחלק מ־AI Project Operating System, עם Lifecycle, Entry Behavior, Project State, Governance ויכולות מאושרות — ולא כשיחת ChatGPT מבודדת.

החבילה אינה יוצרת Skills, Workers או מודל State חדש ואינה מפעילה Automation.

## 2. Bootstrap Philosophy

- **OS is Shared Capability:** Frameworks, Contracts, Skills, Workers, Templates ו־Governance נשארים גלובליים.
- **Project Instance is Isolated Execution:** Context, State, Knowledge, Decisions, Evidence ו־Outputs נשארים ייחודיים לפרויקט.
- **Reference Before Duplication:** Project Instance מקבל References ו־Access מבוקר ל־OS, לא עותקים מיותרים.
- **Entry Point First:** כל בקשה הקשורה לפרויקט עוברת דרך Project Entry Point.
- **Orchestrator as Response Authority:** רק Lifecycle Orchestrator מייצר Phase Guidance למשתמש.
- **Minimum Necessary Process:** נוצרים רק Artifacts ו־Folders הנדרשים לצעד הנוכחי.

## 3. Components Included

### 3.1 System Identity

כל Project Instance מקבל Project OS Reference:

```yaml
project_os_reference:
  os_name: AI Project Operating System
  os_version: <bound approved OS version>
  version_at_creation: <creation-time version>
  current_version: <current bound version>
  loaded_capabilities:
    - Project Entry Point
    - Project Launcher
    - Lifecycle Orchestrator
    - Project Initiation Workflow
    - Approved Skills
    - Approved Workers
    - Approved Templates
  governance_rules:
    - Canonical State Model
    - Phase Guidance Output Contract
    - Decision and Approval Rules
    - Source of Truth Rules
    - Continuous Improvement Rules
```

### 3.2 Project Operating Rules

כל Project Instance יורש References לכללים הבאים:

- Lifecycle Rules ו־Phase Progression Rules.
- Phase Guidance Output Contract.
- Decision Management ו־Human Approval Rules.
- Risk, Escalation ו־Review Rules.
- Project Knowledge ו־Source of Truth Rules.
- Learning ו־Continuous Improvement Rules.
- Project/OS Isolation Rules.

הכללים אינם מועתקים ל־Project Knowledge כמקור חדש; ה־OS נשאר מקור האמת שלהם.

### 3.3 Entry Behavior

כל בקשה הקשורה לפרויקט עוברת דרך:

```text
User Request
      ↓
Project Entry Point
      ↓
Intent Detection
      ↓
Project State
      ↓
Lifecycle Orchestrator
      ↓
Skills / Workers
      ↓
Phase Guidance Output Contract
      ↓
User
```

אין להחזיר Project Status, Continuation, Validation או Next Step ישירות מ־Chat Context, Skill, Worker או Template.

## 4. Initialization Flow

```text
Start New Project
        ↓
Project Entry Point
        ↓
Project Existence Check
        ↓
Project Instance Bootstrap Workflow
        ↓
Project OS Reference Bound
        ↓
Project Registry Entry Created
        ↓
Project Structure Initialized
        ↓
Canonical Project State Initialized
        ↓
Handoff to Lifecycle Orchestrator
        ↓
Project Initiation Workflow / Discovery
```

Bootstrap אינו מבצע Discovery. הוא מכין את ה־Project Instance ומעביר שליטה ל־Lifecycle Orchestrator.

## 5. Project Structure

כל Project Instance מקבל את מבנה הידע הבא, כאשר יצירה בפועל מותאמת ל־Minimum Necessary Process:

```text
Project Instance/
├── README.md
├── 00_Project_Context/
│   ├── Project Context.md
│   └── Project Brief.md, כאשר נוצר
├── Project State/
│   └── Canonical Project State
├── Project Knowledge/
├── Project Decisions/
├── Project Evidence/
├── Project Outputs/
├── Project Learning/
└── Phase Workspace/
    └── 01_Discovery/, כאשר מופעל
```

### Structure Rules

- `README.md` מסביר את זהות הפרויקט ואת קישור ה־OS.
- `Project State` מכיל את הרשומה הקנונית בלבד.
- `Project Knowledge` אינו כולל Knowledge של פרויקטים אחרים.
- `Project Decisions` ו־`Project Evidence` נשארים מבודדים.
- `Phase Workspace` נוצר לפי השלב הפעיל ולא בהכרח כולו מראש.
- אין ליצור קובץ או תיקייה ללא שימוש ברור.

## 6. Lifecycle Initialization

### Initial Lifecycle State

כל Project Instance מתחיל ב־:

- **Phase:** `Discovery`.
- **Initial Status:** `proposed` — הערך הקנוני בעת יצירה.
- **Active Status:** `active` — נקבע על ידי ה־Orchestrator כאשר Initiation מתחיל בפועל.
- **Progress:** `0`.

אין להשתמש ב־`In Progress` כערך State חדש; אם נדרש תיאור ידידותי, הוא View בלבד של `active`.

### Required First Outputs

לאחר Handoff ל־Lifecycle Orchestrator, תהליך Initiation/Discovery צפוי ליצור:

- Project Context.
- Problem Statement.
- Confirmed Findings.
- Assumptions.
- Open Questions.
- Initial Risks.
- Initial Scope Boundaries.
- Project Brief.

ה־Discovery Skill אינו יוצר Product Decisions. החלטות יופיעו רק אם אושרו במפורש על ידי Project Owner.

### Discovery Completion

אין מעבר ל־Strategy לפני ש:

- הבעיה מובנת.
- Findings מרכזיים מתועדים.
- Assumptions מזוהים.
- Validation Required ידוע.
- Scope Boundaries קיימים.
- Risks ו־Open Questions מתועדים.

## 7. Capability Loading

Project Instance מקבל גישה מבוקרת ליכולות קיימות:

### Framework References

- Architecture and System Contracts.
- Lifecycle Framework.
- Phase Review and Transition Rules.
- Knowledge System.
- Continuous Improvement Framework.

### Skills

Skills נטענים לפי Project Type, Current Phase, Risk Level, Missing Knowledge ו־Required Output. אין לטעון את כל ה־Skills כברירת מחדל.

### Workers

Workers נטענים לפי Task ו־Capability Need. אין ליצור Worker Instance חדש כחלק מהחבילה ללא צורך והגדרה מאושרת.

### Templates

Templates נטענים לפי Phase, Complexity, Risk ו־Required Output. בתחילת פרויקט נדרש בדרך כלל Project Brief Template, לפי הצורך.

### Reference Rule

החבילה מצביעה על ה־OS המאושר. היא אינה משכפלת System Knowledge, Skills, Workers או Templates לתוך Project Knowledge.

## 8. Registry Integration

בעת יצירת Project Instance נוצר Project Registry Entry קנוני:

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

Project Registry משמש לאיתור, מניעת כפילויות וניתוב. הוא אינו מחליף את Project State המלא ואינו מחזיק את Project Knowledge.

## 9. User Experience

### Initial Request

```text
User:
Start New Project: Habit Tracker
```

### Expected System Behavior

המערכת:

1. מזהה New Project דרך Project Entry Point.
2. מבצעת Project Existence Check.
3. מאתחלת Project Instance.
4. רושמת Project Registry Entry.
5. מקשרת OS Version ויכולות מאושרות.
6. מתחילה ב־Discovery.
7. מעבירה שליטה ל־Lifecycle Orchestrator.

### Expected Initial Response

```text
## Project Bootstrap

Project: Habit Tracker
Project Instance: Initialized
Existing Project Check: No Match
Current Phase: Discovery
Status: active
OS Version: [bound version]

## Required User Action
Describe the problem this project should solve, who experiences it, and the desired outcome.

## Expected Output
- Project Context.
- Discovery Summary.
- Project Brief.

## Completion Criteria
- Problem, users, initial scope and key assumptions are understood.

## Next Recommended Action
Provide the initial project context so Discovery can begin.
```

התגובה הראשונית עוברת דרך Lifecycle Orchestrator כאשר היא כוללת Phase Guidance. המשתמש אינו נדרש להכיר פקודות פנימיות.

## 10. Validation Checklist

### OS Binding

- [ ] OS Name מוגדר.
- [ ] OS Version נקשרה בזמן היצירה.
- [ ] Loaded Capabilities מפנות לגרסאות מאושרות.
- [ ] Governance Rules זמינות.

### Project Isolation

- [ ] Project ID ייחודי.
- [ ] Project State חדש ונפרד.
- [ ] Project Knowledge ריק או מכיל רק מידע שסופק עבור הפרויקט.
- [ ] לא הועתקו Decisions, Evidence או History מפרויקט אחר.

### Registry

- [ ] Project Registry Entry נוצר.
- [ ] Name, Owner, Status, Phase, Version, Location, Created Date ו־Last Activity קיימים.

### Lifecycle

- [ ] Current Phase הוא `Discovery`.
- [ ] Initial Status הוא `proposed` או `active` לפי רגע ההפעלה הקנוני.
- [ ] Handoff ל־Lifecycle Orchestrator נוצר.
- [ ] Discovery אינו נחשב הושלם לפני Completion Criteria.

### Response Authority

- [ ] Project Entry Point קיבל את בקשת המשתמש.
- [ ] Lifecycle Orchestrator יצר Phase Guidance.
- [ ] Skills ו־Workers לא החזירו הנחיית Phase ישירה.
- [ ] המשתמש קיבל Required User Action, Expected Output ו־Completion Criteria.

## 11. Package Boundaries

Bootstrap Package אינו:

- Project Discovery.
- Project Planning.
- Skill או Worker חדש.
- Project State Model חדש.
- Automation.
- Project Knowledge משותף.
- אישור לשינוי OS.

כל שינוי OS עתידי עובר דרך Continuous Improvement, Review ואישור לפי הארכיטקטורה המאושרת.
