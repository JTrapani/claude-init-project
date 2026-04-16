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
- `package.json` or `pyproject.toml` or `Cargo.toml` (detect stack)
- `README.md` (understand project purpose)
- Any existing `CLAUDE.md` (avoid overwriting existing work)

If `.claude/CLAUDE.md` already has substantial content, ask whether to overwrite or skip.

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

  ## Workflow Orchestration

  ### 1. Plan Node Default
  - Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
  - Always use context7 for research and documentation when implementing any apis or reviewing documentation.
  - If something goes sideways, STOP and re-plan immediately — don't keep pushing
  - Use plan mode for verification steps, not just building
  - Write detailed specs upfront to reduce ambiguity

  ### 2. Subagent Strategy
  - Use subagents liberally to keep main context window clean
  - Offload research, exploration, and parallel analysis to subagents
  - For complex problems, throw more compute at it via subagents
  - One task per subagent for focused execution

  ### 3. Self-Improvement Loop
  - After ANY correction from the user: update tasks/lessons.md with the pattern
  - Write rules for yourself that prevent the same mistake
  - Ruthlessly iterate on these lessons until mistake rate drops
  - Review tasks/lessons.md at session start

  ### 4. Verification Before Done
  - Never mark a task complete without proving it works
  - Diff behaviour between main and your changes when relevant
  - Ask yourself: "Would a staff engineer approve this?"
  - Run tests, check logs, demonstrate correctness

  ### 5. Demand Elegance (Balanced)
  - For non-trivial changes: pause and ask "is there a more elegant way?"
  - If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
  - Skip this for simple, obvious fixes — don't over-engineer

  ### 6. Autonomous Bug Fixing
  - When given a bug report: just fix it. Don't ask for hand-holding
  - Point at logs, errors, failing tests — then resolve them
  - Go fix failing CI tests without being told how

  ### 7. Debugging
  - When debugging, if you do not have clear logs, do research on web and context7 before guessing. 
  - If you have attempted a fix more than twice without advancing the issue, stop and re-evaluate your approach
  - After solving an issue, always give a clear RCA.

  ## Task Management
  - Plan First: Write plan to tasks/todo.md with checkable items
  - Verify Plan: Check in before starting implementation
  - Track Progress: Mark items complete as you go
  - Explain Changes: High-level summary at each step
  - Document Results: Add review section to tasks/todo.md
  - Capture Lessons: Update tasks/lessons.md after corrections

  ## Git Workflow
  - **Always use the `git-workflow` agent** for all git operations — branching, committing, PRs, reviews, and merges
  - Never commit, push, open PRs, or merge directly — route through the agent
  - The agent enforces: Linear ticket linking, pre-PR code review, operator approval before merge
  - Invoke via subagent with `subagent_type: "git-workflow"`
  - Exception: initial project scaffolding by /init-project (git-workflow is not yet available)

  ## Core Principles
  - Simplicity First: Make every change as simple as possible. Impact minimal code.
  - No Laziness: Find root causes. No temporary fixes. Senior developer standards.
  - Minimal Impact: Changes should only touch what's necessary. Avoid introducing bugs.
  - Always use Context7 for SDK/library API documentation. For cloud provider workflows, IAM, and security practices, cross-check with a web search against official docs — Context7 may have stale information.


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
