# init-project

A global Claude Code command that scaffolds the full `.claude/` and `tasks/` structure for any new project — in one shot.

Built and maintained by [Joe Trapani](https://www.linkedin.com/in/joetrapani/), CTO at Capital Investment Advisors. Part of the [Build Different](https://www.linkedin.com/in/tech-ninja/) blog series. 

---

## What it does

Type `/init-project` in any new Claude Code project and Claude will:

1. **Check Context7 MCP** — verifies the Context7 MCP server is connected and warns if it's missing
2. **Detect your stack** — reads `package.json`, `pyproject.toml`, `Cargo.toml`, and `README.md` to understand your project
3. **Create the full `.claude/` structure:**
   - `.claude/CLAUDE.md` — project context, conventions, and workflow rules tailored to your stack
   - `.claude/rules/code-style.md` — coding standards inferred from your linter config
   - `.claude/rules/testing.md` — test conventions for your detected framework
   - `.claude/commands/fix-issue.md` — end-to-end GitHub issue resolution command
   - `.claude/settings.json` — auto-memory enabled, `.env` and secrets protected
4. **Create task management files:**
   - `tasks/todo.md` — Claude writes plans here before any non-trivial work
   - `tasks/lessons.md` — Claude logs corrections here; reviewed at every session start
5. **Verify global subagents** — checks `~/.claude/agents/` and installs any missing agents (see [Subagents](#subagents) below)
6. **Optionally initialise a private GitHub repo** — creates the repo, stages, commits, and pushes the initial structure

---

## Installation

Save `init-project.md` and the subagents to your global Claude directories:

```bash
cp init-project.md ~/.claude/commands/init-project.md
mkdir -p ~/.claude/agents
cp agents/*.md ~/.claude/agents/
```

> **Note:** The command and agents are user-level. They must live in `~/.claude/commands/` and `~/.claude/agents/`, not inside a project repo — because they run before any `.claude/` structure exists.

---

## Usage

```bash
cd your-new-project
claude
/init-project
```

Claude will detect your stack, scaffold everything, and summarise what was created.

---

## Why this exists

Claude Code is powerful out of the box. But default state — no memory, no rules, no context — is just the starting point. The difference between default and properly set up is night and day: fewer hallucinations, more consistency, and a system that gets smarter the more you use it.

This command is the compiled result of everything that actually works. Take it, use it, adapt it to your stack.

Read more: [Build Different — Build the Builder](#) *(link coming)*

---

## Subagents

This project includes four global subagents that extend Claude Code with specialized capabilities. They live in `~/.claude/agents/` and are available across all projects.

| Agent | Purpose |
|---|---|
| `code-reviewer` | Multi-pass code review with parallel bug, security, and CLAUDE.md compliance checks. Validates findings to filter false positives. |
| `git-workflow` | Contextual git lifecycle agent. Detects current state (branch, commits, PR, comments) and executes the correct next step — branching, committing, internal review, PR creation, comment resolution, and merge (with operator approval). |
| `doc-generator` | Generate documentation — docstrings, README files, API docs. |
| `test-writer` | Write comprehensive tests — unit tests, integration tests, edge case coverage. |

### How subagents work

Subagents are specialized agents that run in their own context. They are invoked via the `Agent` tool with `subagent_type` matching the agent name. For example:

```
Agent(subagent_type="code-reviewer", prompt="Review PR #21")
Agent(subagent_type="git-workflow", prompt="Ship the current changes")
```

The `git-workflow` agent is the primary workflow enforcer. CLAUDE.md directs all git operations through it, ensuring:
- Every change has a Linear ticket
- Code review runs before PRs are opened
- PR comments are addressed before merge
- Merge requires explicit operator approval

### Installation

The `/init-project` command automatically verifies these agents are installed. To install manually:

```bash
cp agents/*.md ~/.claude/agents/
```

Reference copies are stored in the `agents/` directory of this repo.

### Customization notes

- **`git-workflow`** is opinionated toward [Linear](https://linear.app) for ticket tracking. If you use a different tracker (Jira, GitHub Issues, etc.), edit `~/.claude/agents/git-workflow.md` — the Linear-specific lines are commented for easy replacement.
- **`code-reviewer`** supports inline PR comments via the `--comment` flag, which requires the `github_inline_comment` MCP server. Without it, the reviewer works normally but outputs findings to the terminal only. The MCP server is optional.

---

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (Claude Pro/Max subscription or API key)
- [Context7 MCP](https://context7.com) (strongly recommended — install with `claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp`)
- Node.js 18+ and npm/npx

---

## License

MIT — take it, use it, build something real.
