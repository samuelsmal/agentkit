#!/usr/bin/env bash
# tech-research setup: run by `agentkit add` in the target project directory.
# Installs a pre-commit hook that rewraps Markdown to 100 chars and checks the result.
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG=.pre-commit-config.yaml

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git init -q
  echo "setup: git init (the pre-commit hook needs a repository)"
fi

if [ ! -e "$CONFIG" ]; then
  cp "$SKILL_DIR/assets/pre-commit-config.yaml" "$CONFIG"
  echo "setup: created $CONFIG"
elif grep -q 'md-line-width' "$CONFIG"; then
  echo "setup: $CONFIG already has the Markdown hooks"
else
  echo "setup: $CONFIG exists; merge these hooks by hand:"
  sed 's/^/    /' "$SKILL_DIR/assets/pre-commit-config.yaml"
fi

if command -v pre-commit >/dev/null 2>&1; then
  pre-commit install
  echo "setup: to rewrap existing Markdown now, run: pre-commit run --all-files"
else
  echo "setup: pre-commit not found. Install it (uv tool install pre-commit), then run: pre-commit install"
fi
