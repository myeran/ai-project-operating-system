#!/bin/bash
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec "$ROOT_DIR/launcher/start.sh" "$@"
