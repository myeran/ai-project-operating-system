"""Locate and start the shared AI Project Operating System Runtime."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen


CONFIG_PATH = Path.home() / ".codex" / "project-navigator" / "runtime.json"
RUNTIME_URL = "http://127.0.0.1:8765"


def is_runtime_root(path: Path) -> bool:
    return (path / "launcher" / "start.sh").is_file() and (path / "runtime" / "runtime_api.py").is_file()


def candidates(workspace: Path) -> list[Path]:
    result: list[Path] = []
    configured = os.environ.get("AI_PROJECT_OS_ROOT")
    if configured:
        result.append(Path(configured).expanduser())
    if CONFIG_PATH.is_file():
        try:
            result.append(Path(json.loads(CONFIG_PATH.read_text(encoding="utf-8"))["runtime_root"]))
        except (OSError, KeyError, TypeError, json.JSONDecodeError):
            pass
    result.extend([workspace, *workspace.parents])
    home = Path.home()
    for parent in (home / "Documents", home / "Desktop", home / "Projects", home / "Project", home / "Downloads"):
        result.append(parent / "ai-project-operating-system")
        result.append(parent / "AI Project Operating System")
    return result


def locate(workspace: str | None) -> Path:
    start = Path(workspace or os.getcwd()).expanduser().resolve()
    seen: set[Path] = set()
    for candidate in candidates(start):
        candidate = candidate.expanduser().resolve()
        if candidate in seen:
            continue
        seen.add(candidate)
        if is_runtime_root(candidate):
            return candidate
    raise RuntimeError("AI Project Operating System Runtime was not found")


def register(root: Path) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps({"runtime_root": str(root)}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def runtime_is_available() -> bool:
    try:
        with urlopen(RUNTIME_URL, timeout=1):
            return True
    except (URLError, TimeoutError, OSError):
        return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("ensure", "start", "status"))
    parser.add_argument("--workspace", default=None)
    args = parser.parse_args()
    try:
        root = locate(args.workspace)
        register(root)
        if args.command == "ensure":
            print(root)
            return 0
        if args.command == "status":
            print("ready" if runtime_is_available() else "stopped")
            return 0 if runtime_is_available() else 1
        if not runtime_is_available():
            subprocess.run([str(root / "launcher" / "start.sh"), "--no-browser"], cwd=root, check=True, timeout=60)
        print(root)
        return 0
    except (RuntimeError, OSError, subprocess.SubprocessError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
