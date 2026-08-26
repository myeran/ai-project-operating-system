"""Generate project lifecycle Mermaid and HTML views from canonical State."""

from __future__ import annotations

from pathlib import Path
from typing import Any


PHASES = [
    ("Discovery", "Discovery Skill", "D"),
    ("Strategy", "Product Strategy Skill", "S"),
    ("Planning", "Project Planning Skill", "P"),
    ("Design", "UX/UI Skill", "U"),
    ("Execution", "Engineering Skill", "E"),
    ("Validation", "Review Skill", "V"),
    ("Launch", "Launch Skill", "L"),
    ("Learning", "Documentation Skill", "K"),
]


class LifecycleArtifactService:
    """Create reproducible project-local lifecycle artifacts."""

    def __init__(self, root: str | Path | None = None) -> None:
        self.root = Path(root) if root is not None else Path.cwd()

    def generate(self, workspace_location: str, state: dict[str, Any]) -> dict[str, str]:
        workspace = self._workspace(workspace_location)
        output_dir = workspace / "project_visuals"
        output_dir.mkdir(parents=True, exist_ok=True)
        mmd_path = output_dir / "project-lifecycle.mmd"
        html_path = output_dir / "project-lifecycle.html"
        mermaid = self._render_mermaid(state)
        mmd_path.write_text(mermaid, encoding="utf-8")
        html_path.write_text(self._render_html(mermaid), encoding="utf-8")
        return {"mermaid": str(mmd_path), "html": str(html_path)}

    def existing_paths(self, workspace_location: str) -> dict[str, str] | None:
        """Return generated visual paths without creating or changing files."""

        output_dir = self._workspace(workspace_location) / "project_visuals"
        paths = {
            "mermaid": output_dir / "project-lifecycle.mmd",
            "html": output_dir / "project-lifecycle.html",
        }
        if not all(path.is_file() for path in paths.values()):
            return None
        return {kind: str(path) for kind, path in paths.items()}

    def _workspace(self, workspace_location: str) -> Path:
        workspace = Path(workspace_location)
        return workspace if workspace.is_absolute() else self.root / workspace

    @staticmethod
    def _render_mermaid(state: dict[str, Any]) -> str:
        current = state.get("phase") or "Discovery"
        phases = [phase for phase, _, _ in PHASES]
        current_index = phases.index(current) if current in phases else 0
        lines = [
            "%% Generated from canonical Project State; do not edit status manually.",
            f"%% project_id={state.get('project_id', '')}",
            f"%% current_phase={current}",
            "",
            "flowchart TB",
        ]
        for index, (phase, skill, node_id) in enumerate(PHASES):
            lines.append(f"    {node_id}[{phase}\\n{skill}]")
            if index < len(PHASES) - 1:
                lines.append(f"    {node_id} --> {PHASES[index + 1][2]}")
        lines.extend([
            "",
            "    classDef current fill:#e4f5ed,stroke:#16845b,color:#126744,stroke-width:3px;",
            "    classDef completed fill:#e6f0fb,stroke:#2563a6,color:#1e568f,stroke-width:2px;",
            "    classDef future fill:#eef2f5,stroke:#9aa9b6,color:#6d8194,stroke-width:1px;",
            f"    class {PHASES[current_index][2]} current;",
        ])
        completed = [node_id for index, (_, _, node_id) in enumerate(PHASES) if index < current_index]
        future = [node_id for index, (_, _, node_id) in enumerate(PHASES) if index > current_index]
        if completed:
            lines.append(f"    class {','.join(completed)} completed;")
        if future:
            lines.append(f"    class {','.join(future)} future;")
        return "\n".join(lines) + "\n"

    @staticmethod
    def _render_html(mermaid: str) -> str:
        return f'''<!doctype html>
<html lang="he" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Project Lifecycle</title>
  <style>
    :root {{ color-scheme: light; --ink:#17324d; --muted:#6d8194; --surface:#f7fafc; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; padding:24px; background:linear-gradient(180deg,#fff 0%,var(--surface) 100%); color:var(--ink); font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }}
    main {{ max-width:980px; margin:auto; background:#fff; border:1px solid #e5edf3; border-radius:20px; padding:24px; box-shadow:0 12px 40px rgba(23,50,77,.08); }}
    .eyebrow {{ color:#16845b; font-size:12px; font-weight:800; letter-spacing:.08em; text-transform:uppercase; }}
    h1 {{ margin:7px 0 8px; font-size:clamp(24px,3vw,34px); }}
    .subtitle {{ margin:0 0 20px; color:var(--muted); }}
    .legend {{ display:flex; flex-wrap:wrap; gap:14px; margin-bottom:20px; color:var(--muted); font-size:13px; }}
    .legend span {{ display:inline-flex; align-items:center; gap:7px; }}
    .swatch {{ width:10px; height:10px; border-radius:50%; display:inline-block; }}
    .current {{ background:#16845b; }} .completed {{ background:#2563a6; }} .future {{ background:#9aa9b6; }}
    .diagram {{ overflow-x:auto; padding:10px 0 18px; }}
    .mermaid {{ width:100%; }}
    .note {{ border-top:1px solid #d7e1e9; padding-top:16px; color:var(--muted); font-size:14px; line-height:1.6; }}
  </style>
  <script type="module">
    import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11.12.2/+esm";
    mermaid.initialize({{ startOnLoad:true, securityLevel:"strict", theme:"base", flowchart:{{ htmlLabels:true, curve:"basis" }} }});
  </script>
</head>
<body>
  <main>
    <div class="eyebrow">Project Navigator</div>
    <h1>מסלול בניית הפרויקט</h1>
    <p class="subtitle">נוצר אוטומטית מתוך ה־Runtime וה־Project State.</p>
    <div class="legend" aria-label="מקרא">
      <span><i class="swatch current"></i>שלב נוכחי</span>
      <span><i class="swatch completed"></i>שלב שהסתיים</span>
      <span><i class="swatch future"></i>שלב עתידי</span>
    </div>
    <section class="diagram" aria-label="תרשים זרימה של שלבי הפרויקט">
      <pre class="mermaid">{mermaid}</pre>
    </section>
    <p class="note">עדכון של ה־Project State יוצר מחדש את התרשים ואת קובץ ה־HTML.</p>
  </main>
</body>
</html>
'''
