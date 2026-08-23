#!/bin/bash
set -u

# One-click launcher for the local AI Project Operating System on macOS.

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
RUNTIME_DIR="$ROOT_DIR/runtime"
STATE_DIR="$ROOT_DIR/.runtime-launcher"
LOG_DIR="$STATE_DIR/logs"
LOCK_DIR="$STATE_DIR/start.lock"
STATE_FILE="$STATE_DIR/pids"
CHAT_URL="http://127.0.0.1:8790"

mkdir -p "$LOG_DIR"

if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  echo "ההפעלה כבר מתבצעת. לא הופעלו תהליכים נוספים."
  exit 0
fi
trap 'rmdir "$LOCK_DIR" 2>/dev/null || true' EXIT

pid_is_alive() {
  kill -0 "$1" 2>/dev/null
}

all_managed_processes_alive() {
  test -s "$STATE_FILE" || return 1
  while IFS='=' read -r name pid; do
    test -n "$pid" || return 1
    pid_is_alive "$pid" || return 1
  done < "$STATE_FILE"
}

if all_managed_processes_alive; then
  echo "המערכת כבר פעילה. לא הופעלו תהליכים כפולים."
  open "$CHAT_URL"
  exit 0
fi

# A stale/partial state is never used to kill processes. It is safe to replace
# only after confirming that none of the recorded PIDs is still alive.
if test -s "$STATE_FILE"; then
  while IFS='=' read -r _name pid; do
    if test -n "$pid" && pid_is_alive "$pid"; then
      echo "נמצאה הפעלה חלקית (PID $pid). עצור אותה עם Stop ואז נסה שוב."
      exit 1
    fi
  done < "$STATE_FILE"
  rm -f "$STATE_FILE"
fi

port_is_busy() {
  lsof -nP -iTCP:"$1" -sTCP:LISTEN >/dev/null 2>&1
}

start_service() {
  local name="$1"
  local port="$2"
  local module="$3"
  local log_file="$LOG_DIR/$name.log"

  if port_is_busy "$port"; then
    echo "הפורט $port כבר בשימוש. לא הופעל $name כדי למנוע כפילות."
    return 1
  fi

  STARTED_PID="$(/usr/bin/python3 "$ROOT_DIR/launcher/spawn_service.py" "$RUNTIME_DIR" "$module" "$log_file")" || return 1
  test -n "$STARTED_PID"
}

wait_for_url() {
  local url="$1"
  local attempts=0
  local status
  while test "$attempts" -lt 30; do
    status="$(curl -sS -o /dev/null -w '%{http_code}' --max-time 1 "$url" 2>/dev/null || true)"
    if test "$status" != "000" && test -n "$status"; then
      return 0
    fi
    attempts=$((attempts + 1))
    sleep 1
  done
  return 1
}

start_service runtime-api 8765 runtime_api || exit 1
runtime_pid="$STARTED_PID"
printf 'runtime_api=%s\n' "$runtime_pid" > "$STATE_FILE"

start_service mcp-server 8787 integration.mcp_server || {
  echo "הפעלת MCP Server נכשלה. בדוק את $LOG_DIR/mcp-server.log"
  exit 1
}
mcp_pid="$STARTED_PID"
printf 'mcp_server=%s\n' "$mcp_pid" >> "$STATE_FILE"

start_service local-chat 8790 integration.local_chat || {
  echo "הפעלת Local Chat נכשלה. בדוק את $LOG_DIR/local-chat.log"
  exit 1
}
chat_pid="$STARTED_PID"
printf 'local_chat=%s\n' "$chat_pid" >> "$STATE_FILE"

if ! wait_for_url "http://127.0.0.1:8765" || \
   ! wait_for_url "http://127.0.0.1:8787/health" || \
   ! wait_for_url "$CHAT_URL"; then
  echo "השירותים לא הפכו לזמינים בזמן. בדוק את הלוגים ב־$LOG_DIR"
  exit 1
fi

echo "AI Project Operating System פעילה. פותח את Local Chat..."
open "$CHAT_URL"
