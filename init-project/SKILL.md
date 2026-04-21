---
name: init-project
description: Scaffold the full .claude/ and tasks/ structure for a new project. Creates CLAUDE.md, rules, commands, settings.json, tasks/todo.md and tasks/lessons.md with starter content tailored to this project.
---

You are setting up the standard Claude Code project structure for this repository.
Follow these steps exactly.

## Step 1 — Check Context7 MCP

Check if any `mcp__context7__` tools appear in the `<available-deferred-tools>` list at the start of the conversation. This list is always present and reflects the actual MCP connections for the current session.

**Do NOT run `claude mcp list` via Bash** — it spawns a separate process that cannot see the current session's MCP connections and will return empty/inaccurate results.

- If `mcp__context7__` tools appear in the deferred tools list — continue normally
- If they do **not** appear — make a note to warn at the end. Do not stop.

## Step 2 — Gather context

Before creating any files, read the following if they exist:
- `package.json` or `pyproject.toml` or `Cargo.toml` or `go.mod` or `Gemfile` (detect stack)
- `README.md` (understand project purpose)
- Any existing `CLAUDE.md` (avoid overwriting existing work)

If `.claude/CLAUDE.md` already has substantial content, ask whether to overwrite or skip.

### 2a — Classify the repo

Treat the repo as **brand new** if ALL of these are true:
- No manifest file (package.json, pyproject.toml, Cargo.toml, go.mod, Gemfile, etc.)
- No source files beyond meta files (README.md, LICENSE, .gitignore, .git/)
- No substantial `.claude/CLAUDE.md`

If the repo is **not brand new**: record the detected stack and skip to Step 3.
If the repo **is brand new**: proceed to 2b.

### 2b — Tech-stack interview (brand-new repos only)

Use the `AskUserQuestion` tool to walk through the questions below one at a time. Every question MUST include a **"Not sure — recommend one"** option. When the user picks that option, give ONE opinionated recommendation that is consistent with prior answers plus a one-sentence rationale, then confirm before moving on.

**Default bias** for recommendations (match what the operator already uses elsewhere):
- Backend / services: Python 3.13 + uv + ruff + pytest, AWS Lambda via CDK, Postgres or DynamoDB, PyJWT
- Agents / ML: Strands Agents + Bedrock AgentCore on Lambda, moto for AWS test doubles
- Frontend / web UI: Next.js (App Router) + Tailwind + shadcn/ui, deployed on Vercel

Ask in this order, skipping any question made irrelevant by earlier answers:

1. **Project purpose** — web app, backend API / service, CLI tool, library / SDK, data pipeline, agent / ML project, mobile, other.
2. **Primary language** — Python (default), TypeScript, Go, Rust, other, not sure.
3. **Framework** — tailored options:
   - Python web / API → FastAPI (default), Django, Flask, none
   - Python agent / ML → Strands Agents + Bedrock AgentCore (default), LangChain, raw boto3
   - Python CLI → Typer (default), Click, argparse
   - TypeScript web → Next.js App Router (default), Remix, SvelteKit, Astro
   - TypeScript server (Node runtime for APIs / workers) → Hono (default), Express, Fastify, NestJS
4. **UI styling** (only if there's a UI) — Tailwind + shadcn/ui (default), Tailwind only, CSS Modules, none.
5. **Database** — Postgres (default), DynamoDB, SQLite, MySQL, MongoDB, none yet, not sure.
6. **Auth** — PyJWT / custom JWT (default for Python backends), Auth.js / NextAuth (default for Next.js), Clerk, Cognito, Auth0, none yet, not sure.
7. **Testing** — tailored to language: Python → pytest + pytest-mock + moto (default; moto if AWS is in play). TS → Vitest + Playwright. Go → stdlib `testing`. Rust → `cargo test`.
8. **Linter / formatter** — Python → ruff (default, handles lint + format; target the chosen Python version, line-length 120, rules `E,F,I,W`). TS → Biome (default) or ESLint + Prettier. Go → `gofmt` + `golangci-lint`. Rust → `clippy` + `rustfmt`.
9. **Package manager** — Python → uv (default). TS → pnpm (default), npm, yarn, bun.
10. **Hosting / deployment** — AWS Lambda via CDK (default for Python services / agents), Vercel (default for Next.js), Fly.io, Render, Railway, ECS / Fargate, self-hosted, not sure.

Record every answer in a stack dictionary keyed by category. These answers drive Step 4 (`## Stack`), Step 6 (code-style — e.g. emit a `[tool.ruff]` block for Python), Step 7 (testing), and Step 12c (`.gitignore`).

### 2c — Confirm the stack

Summarise the resolved stack in a short block and ask the user to confirm before any files are created. If they pick "edit", loop back to the specific question(s) they want to change. Only move to Step 3 after explicit confirmation.

## Step 3 — Create directory structure

Run: mkdir -p .claude/rules .claude/commands .claude/agents .claude/skills tasks

## Step 4 — Write .claude/CLAUDE.md

Populate with real detected values. Use this structure:

  # Project: [name]

  ## Stack
  [actual detected stack: language, framework, database, auth, etc.]

  ## Key Conventions
  [inferred from linter config, README, or existing code]

  ## Common Commands
  [actual detected dev/build/test/migrate commands]

  Read the workflow rules from [CLAUDE.md](CLAUDE.md) (located in this skill's directory) and include the full contents of that file in the generated `.claude/CLAUDE.md`, after the project-specific sections (Stack, Key Conventions, Common Commands) written above.



## Step 5 — Verify global subagents

Check if the following agents exist in `~/.claude/agents/`:
- `code-reviewer.md`
- `git-workflow.md`
- `doc-generator.md`
- `test-writer.md`

For each agent:
- If present: report as "already installed" — do not overwrite (user may have customized)
- If missing: warn the user and instruct them to install from the init-project repo:
  `cp agents/*.md ~/.claude/agents/`

Report which agents are present and which are missing.

## Step 6 — Write .claude/rules/code-style.md

Infer conventions from detected linter config (.eslintrc, .prettierrc, ruff, etc.).
Write sensible defaults for the detected stack if none found.

## Step 7 — Write .claude/rules/testing.md

Detect the test framework and write conventions to match.

## Step 8 — Write .claude/commands/fix-issue.md

  ---
  name: fix-issue
  description: Fix a GitHub issue end-to-end. Pass the issue number as an argument.
  disable-model-invocation: true
  ---

  Fix GitHub issue $ARGUMENTS:
  1. Run `gh issue view $ARGUMENTS` to read the full issue
  2. Understand root cause before touching any code
  3. Find all relevant files — search, don't assume
  4. Implement the fix with minimal impact on surrounding code
  5. Write or update tests to cover the fix
  6. Run the test suite and confirm it passes
  7. Run the linter
  8. Commit with a clear message referencing the issue number
  9. Push and open a PR with a summary of what changed and why
  10. Update tasks/todo.md

## Step 9 — Write .claude/settings.json

  {
    "autoMemoryEnabled": true,
    "permissions": {
      "deny": [
        "Read(./.env)",
        "Read(./.env.*)",
        "Read(./secrets/**)"
      ]
    }
  }

## Step 10 — Write tasks/todo.md

  # Tasks

  _Claude writes plans here before starting any non-trivial work._
  _Each task gets checkable items and a review section when complete._

  ---

  ## [Task name goes here]

  ### Plan
  - [ ] Step 1
  - [ ] Step 2
  - [ ] Step 3

  ### Review
  _Added after completion: what was done, what was learned._

## Step 11 — Write tasks/lessons.md

  # Lessons Learned

  _Updated after every correction. Claude reviews this at the start of each session._
  _This file should be committed to git — it is project intelligence._

  ---

  ## Format

  ### YYYY-MM-DD
  - [What went wrong or what was discovered]
  - [The rule that prevents it happening again]

## Step 12 — Prompt: GitHub repo setup

After creating all files, ask the user:

  "Would you like to initialise this project as a GitHub repository and push
  the initial structure? (yes/no)"

If yes, proceed through the following. If no, skip to Step 13.

### 12a — Check prerequisites

Run: git --version && gh --version && gh auth status

- If `git` is not installed: tell the user to install from https://git-scm.com and stop
- If `gh` is not installed: tell the user to install from https://cli.github.com and stop
- If `gh` is not authenticated: run `gh auth login` and wait for completion

### 12b — Check for existing git repo

Run: git rev-parse --git-dir 2>/dev/null

- If already a git repo: skip `git init`
- If not: run `git init`

### 12c — Create .gitignore

Check if `.gitignore` exists. If not, create one. Always include:

  # Claude local overrides
  .claude/settings.local.json

  # Environment files
  .env
  .env.*
  .env.local

  # Dependencies
  node_modules/
  __pycache__/
  *.pyc

  # Build output
  dist/
  build/
  .next/
  out/

  # OS
  .DS_Store
  Thumbs.db

Add stack-specific entries for the detected stack (coverage/, .pytest_cache/, etc.).

### 12d — Create GitHub repository

All repositories are created PRIVATE by default. This is a firm standard — do not
ask the user for visibility preference.

Run: gh repo create <project-name> --private --source=. --remote=origin --description "<inferred description>"

If the directory name is not a valid repo name, suggest a slugified version and
confirm before proceeding.

### 12e — Stage and commit

Run:
  git add .
  git commit -m "chore: initial project structure with Claude Code setup

  - Add .claude/ directory with CLAUDE.md, rules, commands, settings
  - Add tasks/todo.md and tasks/lessons.md
  - Add .gitignore"

### 12f — Push

Run: git push -u origin main

If the default branch is `master`, use `master` instead.
After a successful push, print the repo URL from: gh repo view --json url -q .url

## Step 13 — Confirm and summarise

Output a clean summary:

  ✅ .claude/ structure created:
    - .claude/CLAUDE.md        (project context + workflow rules)
    - .claude/rules/code-style.md
    - .claude/rules/testing.md
    - .claude/commands/fix-issue.md
    - .claude/settings.json
    - tasks/todo.md
    - tasks/lessons.md

  🤖 Global subagents verified:
    - ~/.claude/agents/code-reviewer.md   [installed/already present]
    - ~/.claude/agents/git-workflow.md    [installed/already present]
    - ~/.claude/agents/doc-generator.md   [installed/already present]
    - ~/.claude/agents/test-writer.md     [installed/already present]

  Stack detected: [what you found]
  Next: review .claude/CLAUDE.md and fill in any [bracketed placeholders]

If a GitHub repo was created and pushed, append:

  🐙 GitHub repo initialised:
    [repo URL]
    Initial commit pushed to origin/main (private)

If any values could not be auto-detected, list them explicitly.

If Context7 was NOT detected in Step 1, append this warning:

  ⚠️  Context7 MCP not detected

  Context7 is required for accurate, up-to-date library documentation.
  Without it, Claude may suggest deprecated APIs or outdated patterns.

  Install it with:
    claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp

  Then verify: claude mcp list
