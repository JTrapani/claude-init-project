---
name: init-project
description: Initialize or upgrade shared Claude Code and Codex project guidance, native agent configuration, and task files while preserving existing customizations.
---

# Initialize shared agent configuration

Use the bundled deterministic scaffold script for fresh projects and upgrades of earlier Claude-only or partially converted installations. Keep project conventions, stack choices, deployment restrictions, existing tasks and lessons authoritative.

## Prepare

Read root AGENTS.md, root CLAUDE.md, .claude/CLAUDE.md, any legacy .Codex/AGENTS.md, README and the package manifest when present. Inspect current tasks and lessons without replacing them. Treat a repository with source or a manifest as existing: do not repeat a stack interview or infer a different hosting/database choice.

For a truly empty project, establish its purpose and language first. Ask only unresolved stack choices that affect its setup, using the client's available question mechanism. Offer a recommendation when the operator is unsure. Confirm the resolved choices before writing project-specific instructions. Do not assume a Claude-only tool name exists in Codex.

## Preview and apply

From this skill directory, run:

```sh
python3 scripts/scaffold.py --project /absolute/path/to/project
```

Review all proposed changes and conflicts. The command defaults to preview. When initialization is requested, apply non-conflicting changes:

```sh
python3 scripts/scaffold.py --project /absolute/path/to/project --apply
```

Use the actual installed skill path for scripts when the shell is in the project directory. Every relative path in this skill refers to this skill's directory.

Existing custom content is preserved. Review any `.init-project-proposed` file against its destination before accepting it; the script never authorizes accepting conflicts. Follow the operator's existing authorization and preserve backups. Do not replace existing files wholesale to obtain a cleaner layout.

Fill in genuinely missing project-specific guidance in root AGENTS.md from detected or confirmed facts: actual stack, test/lint/synthesis commands, approval rules and pointers to substantial project plans. Keep this outside managed sections. Existing task/lesson content stays intact. On re-runs, only correct facts the operator authorized changing.

## Compatibility checks

- Root AGENTS.md is the shared entry point. Fresh root CLAUDE.md imports it. Legacy Claude guidance remains readable through explicit migration references; avoid circular imports and duplicating legacy content.
- Shared workflow and skills live under .agents/. Claude and Codex receive native agent/configuration files; matching role names do not make their settings interchangeable.
- Preserve existing .claude/settings.json and .codex/config.toml. Report permission differences; Claude Read-deny entries are not Codex enforcement. Never claim equivalent secret protection or auto-memory behavior from generated Markdown.
- Existing customized global agents are preserved. If their bodies retain provider-specific tools or models, report that manual adaptation is still needed.
- Context7 is optional. Use available official documentation when it is absent. Inspect actual exposed tools instead of inventing a deferred-tool list or CLI command.
- Bootstrap, deploy, git initialization, repository creation, commits and pushes are separate operations requiring their normal authorization. This skill performs none of them.

## Verify and report

Run the preview again. Confirm no unexplained changes remain, native TOML/JSON parses, task files retain their original content, and all instruction references exist. Report created/updated/preserved/conflicting files and any unresolved migration/permission gap. Installed skills may require a fresh client session before their updated metadata is discovered.

For global installation or upgrade, run the source repository's install.sh, or preview the installed script with `python3 scripts/scaffold.py --install-user`. The installer supports an isolated home with `--home` for testing. Preserve existing settings, agent customizations and extra skill files; never delete an installed skill tree wholesale.
