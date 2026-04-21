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

Use the `AskUserQuestion` tool to walk through the questions below one at a time. Every question MUST include a **"Not sure — recommend one"** option — the tool call always appends this option in addition to the listed choices, even when the list below does not spell it out. When the user picks that option, give ONE opinionated recommendation consistent with prior answers plus a one-sentence rationale, then confirm before moving on.

**Default bias.** The defaults below apply ONLY when the user picks "Not sure — recommend one" AND they are consistent with prior explicit answers. Never steer a user away from an explicit choice — e.g., if Q2 is TypeScript, do not recommend Python tooling in later questions.

Operator preferences that seed the defaults:
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
   - Go / Rust → skip the framework question (these ecosystems lean on stdlib + lightweight libraries; capture that as "stdlib" in the dictionary)
4. **UI styling** (only if there's a UI) — Tailwind + shadcn/ui (default), Tailwind only, CSS Modules, none.
5. **Database** — Postgres (default), DynamoDB, SQLite, MySQL, MongoDB, none yet, not sure.
6. **Auth** — only offer options consistent with Q2 + Q3. Python backends → PyJWT / custom JWT (default), Cognito, Auth0, none yet. Next.js → Auth.js / NextAuth (default), Clerk, Auth0, none yet. Do not suggest PyJWT for a TS-only project or Auth.js for a Python-only backend.
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

Populate with real values. **Source of truth**: if the stack dictionary from Step 2b exists (brand-new repo path), use it verbatim — language, framework, DB, auth, testing, linter, package manager, and hosting all come from there. Otherwise fall back to values detected from the manifest files read in Step 2.

The `## Common Commands` section MUST include the package manager chosen in Step 2b (e.g. `uv sync`, `uv run pytest`, `pnpm install`, `pnpm dev`).

Use this structure:

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

**Source of truth**: if the stack dictionary from Step 2b picked a linter/formatter, emit a config block for it:
- ruff → a `[tool.ruff]` block with `target-version` matching the chosen Python version, `line-length = 120`, and `[tool.ruff.lint] select = ["E", "F", "I", "W"]`
- Biome → a `biome.json` stanza with `"formatter": { "enabled": true }` and recommended lint rules
- ESLint + Prettier → an `.eslintrc.json` / `.prettierrc` pair with TypeScript + import-order defaults
- `gofmt` + `golangci-lint` → a minimal `.golangci.yml` with the `errcheck`, `govet`, `staticcheck`, `ineffassign` linters enabled
- `clippy` + `rustfmt` → a `rustfmt.toml` with `edition = "2021"` and a one-line `clippy` invocation

If no Step 2b dictionary exists (pre-existing repo), infer from detected linter config (`.eslintrc`, `.prettierrc`, `pyproject.toml [tool.ruff]`, etc.) or write sensible defaults for the detected stack.

## Step 7 — Write .claude/rules/testing.md

**Source of truth**: if the stack dictionary from Step 2b picked a test framework, use that — e.g., for Python + AWS, document `pytest` + `pytest-mock` + `moto` with an example fixture pattern; for TypeScript, document `vitest` (unit) + `playwright` (e2e). Otherwise detect the test framework from the repo and write conventions to match.

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

Add stack-specific entries based on the Step 2b dictionary if present; otherwise the detected stack. Examples: Python → `.pytest_cache/`, `.ruff_cache/`, `.venv/`, `coverage/`; TypeScript → `.next/`, `.turbo/`, `.pnpm-store/`; AWS CDK → `cdk.out/`, `cdk.context.json`; Go → `bin/`, `*.test`; Rust → `target/`.

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
