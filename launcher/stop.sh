#!/bin/bash
set -u

# Stop only processes recorded by launcher/start.sh.

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
STATE_DIR="$ROOT_DIR/.runtime-launcher"
STATE_FILE="$STATE_DIR/pids"

if test ! -s "$STATE_FILE"; then
  echo "אין תהליכים שהופעלו על ידי ה־Launcher. לא נסגרו תהליכים אחרים."
  exit 0
fi

is_expected_process() {
  local pid="$1"
  local name="$2"
  local command
  command="$(ps -p "$pid" -o command= 2>/dev/null || true)"
  case "$name" in
    runtime_api) echo "$command" | grep -F -- '-m runtime_api' >/dev/null 2>&1 ;;
    mcp_server) echo "$command" | grep -F -- '-m integration.mcp_server' >/dev/null 2>&1 ;;
    local_chat) echo "$command" | grep -F -- '-m integration.local_chat' >/dev/null 2>&1 ;;
    *) return 1 ;;
  esac
}

stop_pid() {
  local name="$1"
  local pid="$2"
  if ! kill -0 "$pid" 2>/dev/null; then
    return 0
  fi
  if ! is_expected_process "$pid" "$name"; then
    echo "דילוג על PID $pid: הוא אינו מזוהה כתהליך של המערכת."
    return 0
  fi
  kill -TERM "$pid" 2>/dev/null || true
}

while IFS='=' read -r name pid; do
  test -n "$pid" && stop_pid "$name" "$pid"
done < "$STATE_FILE"

for _attempt in 1 2 3 4 5; do
  still_running=0
  while IFS='=' read -r _name pid; do
    if test -n "$pid" && kill -0 "$pid" 2>/dev/null; then
      still_running=1
    fi
  done < "$STATE_FILE"
  test "$still_running" -eq 0 && break
  sleep 1
done

while IFS='=' read -r name pid; do
  if test -n "$pid" && kill -0 "$pid" 2>/dev/null && is_expected_process "$pid" "$name"; then
    kill -KILL "$pid" 2>/dev/null || true
  fi
done < "$STATE_FILE"

rm -f "$STATE_FILE"
echo "AI Project Operating System נעצרה. תהליכים שאינם שייכים ל־Launcher לא שונו."
