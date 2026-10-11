#!/usr/bin/env bash
# Hand one self-contained task to Codex, non-interactively, and print its final message.
# Usage (from the repository root): bash auto-loop/tools/codex.sh "detailed task"
# Codex must not stage, commit, or touch protected files; Claude reviews its diff.
set -u

if [ $# -lt 1 ] || [ -z "$1" ]; then
  echo "usage: bash auto-loop/tools/codex.sh \"task\"" >&2
  exit 2
fi

root=$(git rev-parse --show-toplevel) || exit 2
cd "$root" || exit 2
mkdir -p auto-loop/.loop/codex
ts=$(date +%Y%m%d-%H%M%S)
log="auto-loop/.loop/codex/$ts.log"
last="auto-loop/.loop/codex/$ts.last.txt"

rules="Repository rules: read AGENTS.md. Do not run git add, git commit, git reset, git checkout or git push. Do not edit anything under auto-loop/, tests that already exist, AGENTS.md, AGENTS.th.md, .github/ or private/. Use SI units."

codex exec --sandbox workspace-write --output-last-message "$last" "$rules

$1" >"$log" 2>&1
code=$?

echo "[codex exit=$code | full log: $log]"
if [ -s "$last" ]; then
  cat "$last"
else
  tail -n 80 "$log"
fi
exit $code
