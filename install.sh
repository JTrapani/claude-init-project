#!/usr/bin/env bash
set -euo pipefail
: "${HOME:?HOME must be set and non-empty}"

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DEST="$HOME/.claude/skills"
AGENTS_DEST="$HOME/.claude/agents"

[[ -d "$REPO_DIR/init-project" && -d "$REPO_DIR/agents" ]] || {
  echo "install.sh must be run from inside the claude-init-project repo" >&2
  exit 1
}

mkdir -p "$SKILLS_DEST" "$AGENTS_DEST"

shopt -s nullglob
agent_files=("$REPO_DIR"/agents/*.md)
shopt -u nullglob
if (( ${#agent_files[@]} == 0 )); then
  echo "No agents to install from $REPO_DIR/agents" >&2
  exit 1
fi
cp "${agent_files[@]}" "$AGENTS_DEST/"
agent_count=${#agent_files[@]}

rm -rf "$SKILLS_DEST/init-project"
cp -R "$REPO_DIR/init-project" "$SKILLS_DEST/init-project"

echo "Installed init-project skill to $SKILLS_DEST/init-project"
echo "Installed $agent_count agent(s) to $AGENTS_DEST"
echo "Re-run ./install.sh after pulling updates."
