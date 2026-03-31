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
5. **Optionally initialise a private GitHub repo** — creates the repo, stages, commits, and pushes the initial structure

---

## Installation

Save `init-project.md` to your global Claude commands directory:

```bash
cp init-project.md ~/.claude/commands/init-project.md
```

> **Note:** This is a user-level command. It must live in `~/.claude/commands/`, not inside a project repo — because it runs before any `.claude/` structure exists.

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

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (Claude Pro/Max subscription or API key)
- [Context7 MCP](https://context7.com) (strongly recommended — install with `claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp`)
- Node.js 18+ and npm/npx

---

## License

MIT — take it, use it, build something real.
