---
name: git-workflow
description: Manage branches, verification, commits, pull requests and approved merges.
---

Inspect the current branch, working tree, upstream and PR before taking action. Preserve other contributors' changes. Use the project's tracker and naming conventions; branch names start with the change type rather than a username. Keep issue references in branch names, commit messages and PR descriptions, not source comments or documentation.

For implementation, run the project's actual checks rather than assuming a language or package manager. Stage explicit reviewed paths. Commit and publish only within the operator's requested scope. Do not add AI attribution trailers or generated-by footers.

Require independent code-review results before opening a PR. Ask the parent to arrange review when delegation is unavailable. Fix supported findings, explain disagreements and resolve review threads only after the corresponding action. Use available tools, not hardcoded provider-specific tool names.

Update the tracker to In Progress after work begins, In Review after the PR exists, and Done only after a verified merge. If tracker access is unavailable, report the outstanding status update; do not claim it succeeded.

Before merging, verify checks and review-thread disposition and obtain explicit operator approval. Deployment is a separate action requiring its own authorization and the project's deployment mechanism. Initializing agent configuration does not authorize commits, pushes, remote creation or deployment.
