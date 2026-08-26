"""Render the maintained Mermaid lifecycle source as a standalone HTML view."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "project-lifecycle.mmd"
OUTPUT = ROOT / "project-lifecycle.html"


def main() -> None:
    diagram = SOURCE.read_text(encoding="utf-8").strip()
    title = "FaceDoor Access — Project Lifecycle"
    html = f'''<!doctype html>
<html lang="he" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    :root {{ color-scheme: light; --ink:#17324d; --muted:#6d8194; --line:#d7e1e9; --surface:#f7fafc; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; padding:24px; background:linear-gradient(180deg,#fff 0%,var(--surface) 100%); color:var(--ink); font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }}
    main {{ max-width:1180px; margin:auto; background:#fff; border:1px solid #e5edf3; border-radius:20px; padding:24px; box-shadow:0 12px 40px rgba(23,50,77,.08); }}
    .eyebrow {{ color:#16845b; font-size:12px; font-weight:800; letter-spacing:.08em; text-transform:uppercase; }}
    h1 {{ margin:7px 0 8px; font-size:clamp(24px,3vw,34px); }}
    .subtitle {{ margin:0 0 20px; color:var(--muted); }}
    .legend {{ display:flex; flex-wrap:wrap; gap:14px; margin-bottom:20px; color:var(--muted); font-size:13px; }}
    .legend span {{ display:inline-flex; align-items:center; gap:7px; }}
    .swatch {{ width:10px; height:10px; border-radius:50%; display:inline-block; }}
    .current {{ background:#16845b; }} .completed {{ background:#2563a6; }} .future {{ background:#9aa9b6; }}
    .diagram {{ overflow-x:auto; padding:10px 0 18px; }}
    .mermaid {{ width:100%; }}
    .note {{ border-top:1px solid var(--line); padding-top:16px; color:var(--muted); font-size:14px; line-height:1.6; }}
  </style>
  <script type="module">
    import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11.12.2/+esm";
    mermaid.initialize({{ startOnLoad:true, securityLevel:"strict", theme:"base", flowchart:{{ htmlLabels:true, curve:"basis" }} }});
  </script>
</head>
<body>
  <main>
    <div class="eyebrow">FaceDoor Access · Project Navigator</div>
    <h1>מסלול בניית הפרויקט</h1>
    <p class="subtitle">התרשים נוצר מתוך <code>project-lifecycle.mmd</code>.</p>
    <div class="legend" aria-label="מקרא">
      <span><i class="swatch current"></i>שלב נוכחי</span>
      <span><i class="swatch completed"></i>שלב שהסתיים</span>
      <span><i class="swatch future"></i>שלב עתידי</span>
    </div>
    <section class="diagram" aria-label="תרשים זרימה של שלבי הפרויקט">
      <pre class="mermaid">{diagram}</pre>
    </section>
    <p class="note">השלב הנוכחי הוא Discovery. לאחר אישור מעבר מפורש, הסטטוס בתרשים יעודכן ל־Strategy.</p>
  </main>
</body>
</html>
'''
    OUTPUT.write_text(html, encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()
