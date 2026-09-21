# init-project

Initialize Claude Code and Codex projects from shared workflow and role definitions. The existing repository name and `./install.sh` entry point remain supported.

## Install or upgrade

Requires Python 3.11+ and Bash. No third-party Python dependencies.

```sh
./install.sh
```

The installer updates the user skill locations for both clients and installs native agent definitions. It preserves customizations and extra files instead of deleting the installed skill directory. Differing files it cannot safely upgrade produce a `.init-project-proposed` sibling for review. Existing settings are never silently replaced.

Preview without writes:

```sh
python3 init-project/scripts/scaffold.py --install-user
```

Test with an isolated home:

```sh
./install.sh --home /tmp/init-project-demo-home
```

User paths:

- `~/.agents/skills/init-project/`: shared/Codex skill.
- `~/.claude/skills/init-project/`: Claude skill.
- `~/.codex/agents/*.toml`: Codex roles.
- `~/.claude/agents/*.md`: Claude roles.

After installation, start a fresh client session if skill discovery has not refreshed. Invoke `/init-project` in Claude or select the `init-project` skill in Codex. Both use the same scaffold engine.

## Initialize or upgrade a repository

The initializer detects existing files, preserving project-specific guidance, settings, tasks and lessons. It previews before applying:

```sh
python3 init-project/scripts/scaffold.py --project /path/to/repo
python3 init-project/scripts/scaffold.py --project /path/to/repo --apply
```

For a new repository, the agent fills project context from the actual manifest/README or a short stack interview. The script does not generate application code, install dependencies, create GitHub repositories, commit, push or deploy.

Fresh layout:

```text
AGENTS.md                         Shared project entry point
CLAUDE.md                         Imports AGENTS.md
.agents/
  project-workflow.md              Shared workflow
  skills/fix-issue/SKILL.md        Shared reusable workflow
.claude/
  settings.json                   Native Claude settings
  agents/*.md                     Native Claude roles
  skills/fix-issue/SKILL.md        Claude access to shared workflow
.codex/
  config.toml                     Native Codex configuration
  agents/*.toml                   Native Codex roles
tasks/
  todo.md                         Shared working plan
  lessons.md                      Shared lessons
```

## Upgrading existing Claude-only repositories

Run the updated installer once, then run the skill in each repository you want to upgrade. Installing globally alone does not modify existing repositories.

- Existing root `CLAUDE.md`, `.claude/CLAUDE.md`, `.claude/rules/` and custom `AGENTS.md` content are preserved. Shared entry-point references make legacy guidance available without bulk rewriting it.
- Existing `tasks/todo.md` and `tasks/lessons.md` are left intact.
- Existing native settings are retained. New managed references are added only once; repeat runs should be stable.
- A missing `.gitignore` is created; an existing one gains missing secret/local-artifact exclusions without losing its rules.
- Managed updates use previous-content hashes and backups. Conflicts are written as proposals, never silently accepted. Keep or manually reconcile each proposal, then preview again.
- Customized installed agents stay intact. Their Codex counterparts can carry the same instructions, but provider-specific tool references need review; metadata translation is not a guarantee of identical behavior.
- The partially converted `.Codex/` layout is treated as legacy guidance, not native Codex configuration. The supported configuration path is lowercase `.codex/config.toml`.

The first migration favors preserving content over forcing old repositories into the exact fresh-project layout. Later consolidation is optional and should be reviewed separately.

## Canonical sources

Edit `init-project/assets/workflow.md` for shared doctrine and `init-project/assets/agents/*.md` for the four roles: `code-reviewer`, `git-workflow`, `doc-generator`, and `test-writer`. Both native formats derive from those definitions. Defaults inherit the client's model rather than hardcoding Claude or OpenAI model names.

Compact content hashes recognize older defaults without shipping historical instruction copies. Install manifests track managed files; customized agents are never replaced just because their version stamp is old.

## Permissions and compatibility

Claude and Codex have different configuration and permission systems. Claude settings can deny Read access to environment/secret files. Codex's generated TOML does not pretend to translate those deny rules. Project instructions to avoid secrets are guidance, not an enforced filesystem boundary; configure client/organization access controls separately when required.

The installer preserves existing permission settings and reports the gap. It never enables full-access mode, adds blanket tool approval or installs an auto-deployment hook. Existing project-specific approval and deployment restrictions remain authoritative.

Primary documentation:

- [Codex instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Codex configuration](https://learn.chatgpt.com/docs/config-file/config-basic)
- [Codex skills](https://learn.chatgpt.com/docs/build-skills)
- [Codex custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Claude memory/imports](https://code.claude.com/docs/en/memory)
- [Claude skills](https://code.claude.com/docs/en/skills)

## Tests

```sh
python3 -m unittest discover -s tests -v
```

Tests use temporary homes and repositories, not live client installations. They cover fresh setup, legacy migration, customized files, repeat runs, native configuration parsing, dry-run behavior and symlink safety. They validate generated artifacts; actual discovery depends on the installed client supporting the documented configuration formats.
