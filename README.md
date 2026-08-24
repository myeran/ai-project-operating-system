# AI Project Operating System

מערכת מקומית לניהול מחזור חיים של פרויקטים באמצעות Runtime, Orchestrator,
State Adapter ו־Skills בעלי חוזים ובדיקות.

## מדריך למשתמש

למטרת המערכת, הוראות הורדה לכל תיקייה מקומית, פתיחה ב־Codex, יצירת פרויקט
והודעת הצ׳אט הראשונה להפעלת
`project_navigator_skill`, ראו [מדריך המשתמש בעברית](USER_GUIDE_HE.md).

## הפעלה

ב־macOS:

```bash
./Start\ AI\ Project\ OS.command
```

לעצירה:

```bash
./Stop\ AI\ Project\ OS.command
```

## בדיקות

```bash
python3 -m unittest discover -s runtime/tests -p 'test_*.py'
```

## Skills

המערכת כוללת Skills עבור Discovery, Strategy, Planning, Design, Execution,
Validation, Launch ו־Learning. כל Skill כולל Definition, חוזה מכונה, מתאם
Runtime ובדיקות.

ה־Runtime פועל במצב מקומי. נתוני הפרויקטים נשמרים במסד SQLite מקומי ואינם
נכללים ב־Repository הציבורי.

## גבולות בטיחות

ה־Skills מפיקים המלצות ותוצרים לבדיקה. הם אינם משנים Scope, אינם מאשרים
החלטות ואינם מבצעים שחרור או התחייבות למשאבים ללא אישור מפורש.
