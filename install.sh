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

# Read the integer `version:` from a Markdown file's frontmatter.
# Prints 0 when there is no frontmatter or no version key (treated as oldest).
read_version() {
  local v
  v="$(awk '
    NR==1 && $0 !~ /^---[[:space:]]*$/ { exit }   # no frontmatter block
    NR==1 { next }                                 # opening ---
    /^---[[:space:]]*$/ { exit }                   # closing --- before any version
    /^version:[[:space:]]*[0-9]+/ { n=$0; sub(/^version:[[:space:]]*/,"",n); sub(/[^0-9].*$/,"",n); print n; exit }
  ' "$1" 2>/dev/null)"
  echo "${v:-0}"
}

# Emit a file's contents with the frontmatter `version:` line removed, so two files can be
# compared for content equality while ignoring only the version stamp.
strip_version() {
  sed -E '/^version:[[:space:]]*[0-9]+[[:space:]]*$/d' "$1"
}

shopt -s nullglob
agent_files=("$REPO_DIR"/agents/*.md)
shopt -u nullglob
if (( ${#agent_files[@]} == 0 )); then
  echo "No agents to install from $REPO_DIR/agents" >&2
  exit 1
fi

# Version-aware install of the global subagents. Absent -> install. Behind ->
# show a diff and ask before replacing (never a silent overwrite of a customized
# agent). Up-to-date -> skip.
installed=0 updated=0 migrated=0 skipped=0
for src in "${agent_files[@]}"; do
  name="$(basename "$src")"
  dest="$AGENTS_DEST/$name"
  sv="$(read_version "$src")"

  if [[ ! -e "$dest" ]]; then
    cp "$src" "$dest"
    echo "  installed $name (v$sv)"
    installed=$((installed + 1))
    continue
  fi

  iv="$(read_version "$dest")"
  if (( sv > iv )); then
    # Migration guard for pre-versioning installs: an untagged file (v0) whose content matches the
    # shipped version except for the missing `version:` line is an unmodified current agent — just
    # add the tag, no diff/prompt. Only genuinely-customized files fall through to the prompt.
    if (( iv == 0 )) && diff -q <(strip_version "$dest") <(strip_version "$src") >/dev/null 2>&1; then
      cp "$src" "$dest"
      echo "  migrated $name -> v$sv (added version tag; content unchanged)"
      migrated=$((migrated + 1))
      continue
    fi
    echo "  $name is behind: installed v$iv < shipped v$sv"
    if [[ -t 0 ]]; then
      diff -u "$dest" "$src" || true
      read -r -p "  Replace $name with v$sv? [y/N] " ans || ans="n"
    else
      ans="n"
      echo "  (non-interactive shell: not replacing — re-run in a terminal to update)"
    fi
    if [[ "$ans" == [yY] ]]; then
      cp "$src" "$dest"
      echo "  updated $name v$iv -> v$sv"
      updated=$((updated + 1))
    else
      echo "  kept existing $name (v$iv)"
      skipped=$((skipped + 1))
    fi
  else
    echo "  $name up-to-date (v$iv)"
    skipped=$((skipped + 1))
  fi
done

# Replace the skill wholesale (any hand-edits inside the installed skill dir are lost),
# then bundle the shipped agent copies inside it so the skill can version-compare
# installed agents against these references at runtime.
rm -rf "$SKILLS_DEST/init-project"
cp -R "$REPO_DIR/init-project" "$SKILLS_DEST/init-project"
mkdir -p "$SKILLS_DEST/init-project/agents"
cp "${agent_files[@]}" "$SKILLS_DEST/init-project/agents/"

echo "Installed init-project skill to $SKILLS_DEST/init-project"
echo "Agents: $installed installed, $updated updated, $migrated migrated, $skipped left as-is (in $AGENTS_DEST)"
echo "Re-run ./install.sh after pulling updates."
