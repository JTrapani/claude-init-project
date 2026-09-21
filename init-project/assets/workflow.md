# Shared project workflow

## Planning and verification

- Read project instructions and tasks/lessons.md before implementation. Preserve explicit stack, deployment and approval decisions.
- For non-trivial work, write a checkable plan in tasks/todo.md. Use the client's plan mode when available; otherwise keep the plan in that file and communicate the next step.
- Delegate independent, bounded tasks when helpful and supported. Assign file ownership, respect concurrent edits, and consolidate results.
- Verify behavior with appropriate tests and inspection before marking work complete. Record results and limitations in tasks/todo.md.
- After a user correction, record the reusable lesson in tasks/lessons.md.
- Diagnose from evidence; after repeated unsuccessful attempts, reassess the cause and report remaining uncertainty.
- Verify current APIs against official documentation. Use Context7 when available and useful; an unavailable connector is not a reason to invent tool calls or documentation.

## Git and review

- Use the git-workflow role for branching, commits, PRs and merges when the client exposes that role. If unavailable, report it and follow the shared role instructions using available tools.
- Associate work with the project's issue tracker. Keep change-history references in branch names, commits and PR descriptions.
- Stage only reviewed files. Run relevant checks and independent code review before opening a PR. Track issue status from actual workflow events.
- Merging and deployment require explicit operator approval. Project-specific deployment restrictions remain authoritative; initialization never deploys, creates remotes or pushes.

## Code and data hygiene

- Make focused changes with clear interfaces and project-native conventions. Preserve existing behavior unless a change is agreed.
- Comments and documentation explain behavior and constraints. Keep ticket identifiers, commit hashes and PR history out of source comments, docstrings and project documentation; durable vendor/specification references are appropriate.
- Keep secrets, credentials, personal data and customer financial records out of logs, exception messages, generated examples and ordinary reports. Use explicit safe fields instead of whole-object dumps.
- Read secret material only when explicitly needed and authorized. Instruction text is not an operating-system permission boundary; respect client sandbox and access policies.

## Shared context

Both clients use the same tasks/todo.md and tasks/lessons.md. Follow root AGENTS.md and any applicable nested instructions. Tool-specific configuration affects only its own client; do not infer equivalent permissions or memory behavior from matching directory names.
