#!/usr/bin/env python3
"""Spawn one launcher service in its own macOS process session."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 4:
        print("usage: spawn_service.py RUNTIME_DIR MODULE LOG_FILE", file=sys.stderr)
        return 2

    runtime_dir = Path(sys.argv[1]).resolve()
    module = sys.argv[2]
    log_path = Path(sys.argv[3]).resolve()
    log_path.parent.mkdir(parents=True, exist_ok=True)

    with log_path.open("ab") as log:
        process = subprocess.Popen(
            [sys.executable, "-m", module],
            cwd=runtime_dir,
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
            close_fds=True,
            env={**os.environ, "PYTHONUNBUFFERED": "1"},
        )
    print(process.pid)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
