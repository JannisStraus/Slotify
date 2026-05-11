#!/usr/bin/env bash
set -euo pipefail

PATTERN="bin/slotify"

pids=$(pgrep -f "$PATTERN" || true)

if [ -z "$pids" ]; then
    echo "No slotify process running."
    exit 0
fi

echo "Stopping slotify (PIDs: $pids)..."
kill $pids

for _ in {1..10}; do
    sleep 0.5
    if ! pgrep -f "$PATTERN" > /dev/null; then
        echo "Stopped."
        exit 0
    fi
done

echo "Process did not exit, sending SIGKILL..."
kill -9 $(pgrep -f "$PATTERN") 2>/dev/null || true
echo "Stopped."
