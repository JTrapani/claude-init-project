#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DEST="$HOME/.claude/skills"
AGENTS_DEST="$HOME/.claude/agents"

mkdir -p "$SKILLS_DEST" "$AGENTS_DEST"

rm -rf "$SKILLS_DEST/init-project"
cp -R "$REPO_DIR/init-project" "$SKILLS_DEST/init-project"

cp "$REPO_DIR"/agents/*.md "$AGENTS_DEST/"

agent_count=$(ls -1 "$REPO_DIR"/agents/*.md | wc -l | tr -d ' ')
echo "Installed init-project skill to $SKILLS_DEST/init-project"
echo "Installed $agent_count agent(s) to $AGENTS_DEST"
echo "Re-run ./install.sh after pulling updates."
