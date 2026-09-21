"""Deterministic, conservative shared project scaffolding (Python 3.11+)."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
ASSETS = SKILL / "assets"
UPGRADE_HASHES = json.loads((ASSETS / "upgrade-hashes.json").read_text())
MARKER = "<!-- init-project:shared-guidance -->"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe(path: Path) -> None:
    """Reject symlinks in all destination components, including dangling links."""
    for component in (path, *path.parents):
        if component.is_symlink() and not (
            str(component) in {"/tmp", "/var"}
            and str(component.resolve()) == "/private" + str(component)
        ):
            raise ValueError(f"Unsafe symlink destination: {component}")
    if path.exists() and not path.is_file():
        raise ValueError(f"Expected a regular file: {path}")


class Plan:
    def __init__(self, apply: bool):
        self.apply = apply
        self.pending: dict[Path, bytes] = {}
        self.messages: list[str] = []
        self.removals: list[Path] = []

    def read(self, path: Path) -> bytes | None:
        safe(path)
        return self.pending.get(path, path.read_bytes() if path.exists() else None)

    def queue(self, path: Path, data: bytes) -> None:
        safe(path)
        self.pending[path] = data

    def backup(self, path: Path, current: bytes) -> None:
        backup = path.with_name(
            path.name + ".init-project-backup-" + digest(current)[:12]
        )
        existing = self.read(backup)
        if existing is not None and existing != current:
            raise ValueError(f"Backup collision: {backup}")
        self.queue(backup, current)

    def put(self, path: Path, data: str | bytes, *, replace: bool = False) -> bool:
        data = data.encode() if isinstance(data, str) else data
        current = self.read(path)
        if current == data:
            self.messages.append(f"KEEP {path}")
            return True
        if current is None or replace:
            if current is not None:
                self.backup(path, current)
            self.queue(path, data)
            self.messages.append(f"{'CREATE' if current is None else 'UPDATE'} {path}")
            return True
        proposed = path.with_name(path.name + ".init-project-proposed")
        previous = self.read(proposed)
        if previous is not None and previous != data:
            proposed = proposed.with_name(proposed.name + "-" + digest(data)[:12])
            previous = self.read(proposed)
            if previous is not None and previous != data:
                raise ValueError(f"Proposal collision: {proposed}")
        if previous != data:
            self.queue(proposed, data)
        self.messages.append(f"CONFLICT preserve {path}; proposal {proposed}")
        return False

    def finish(self) -> None:
        # Validate the complete plan before creating anything.
        for path in [*self.pending, *self.removals]:
            safe(path)
        for message in self.messages:
            print(("" if self.apply else "DRY-RUN ") + message)
        if self.apply:
            for path, data in self.pending.items():
                path.parent.mkdir(parents=True, exist_ok=True)
                safe(path)
                path.write_bytes(data)
            for path in self.removals:
                path.unlink()


def parse_agent(data: str, fallback: str) -> tuple[str, str, str]:
    metadata = {}
    body = data
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", data, re.DOTALL)
    if match:
        for line in match.group(1).splitlines():
            key, sep, value = line.partition(":")
            if sep:
                metadata[key.strip()] = value.strip().strip("\"'")
        body = data[match.end() :]
    return (
        metadata.get("name", fallback),
        metadata.get("description", f"{fallback} project role"),
        body,
    )


def agent_outputs(data: str, fallback: str) -> tuple[str, str]:
    name, description, body = parse_agent(data, fallback)
    claude = (
        f"---\nname: {json.dumps(name)}\ndescription: {json.dumps(description)}\n---\n\n"
        + body.lstrip("\n")
    )
    codex = (
        "\n".join(
            f"{key} = {json.dumps(value, ensure_ascii=False)}"
            for key, value in (
                ("name", name),
                ("description", description),
                ("developer_instructions", body),
            )
        )
        + "\n"
    )
    return claude, codex


def roles() -> list[Path]:
    result = sorted((ASSETS / "agents").glob("*.md"))
    if not result:
        raise ValueError(f"Missing agent templates: {ASSETS / 'agents'}")
    return result


def project(plan: Plan, root: Path) -> None:
    if not root.is_dir():
        raise ValueError(f"Project must be an existing directory: {root}")
    legacy = [
        p
        for p in [
            root / "CLAUDE.md",
            root / ".claude/CLAUDE.md",
            root / ".Codex/AGENTS.md",
            *sorted((root / ".claude/rules").rglob("*.md")),
        ]
        if p.exists()
    ]
    agents_path = root / "AGENTS.md"
    current = plan.read(agents_path)
    reference = f"{MARKER}\nRead `.agents/project-workflow.md` for the shared project workflow.\n"
    # Conditional prose is intentional: Claude already loads its own guidance.
    if legacy:
        paths = ", ".join("`" + str(p.relative_to(root)) + "`" for p in legacy)
        reference += f"Codex only: also read the existing legacy guidance in {paths}. Claude already loads its own guidance and must not follow this additional read instruction. Honor any rule frontmatter path scopes: apply scoped rules only to matching files. Do not recursively follow references back to this file.\n"
    reference += "<!-- /init-project:shared-guidance -->\n"
    if current is None:
        plan.put(agents_path, "# Project instructions\n\n" + reference)
    elif MARKER.encode() not in current:
        plan.put(
            agents_path,
            current
            + (b"\n" if current.endswith(b"\n") else b"\n\n")
            + reference.encode(),
            replace=True,
        )
    claude_path = root / "CLAUDE.md"
    claude_current = plan.read(claude_path)
    if claude_current is None:
        plan.put(claude_path, "@AGENTS.md\n")
    elif not re.search(rb"(?m)^\s*@(?:\./)?AGENTS\.md\s*$", claude_current):
        shared_import = (
            f"{MARKER}\n@AGENTS.md\n<!-- /init-project:shared-guidance -->\n".encode()
        )
        plan.put(
            claude_path,
            claude_current
            + (b"\n" if claude_current.endswith(b"\n") else b"\n\n")
            + shared_import,
            replace=True,
        )
    plan.put(
        root / ".agents/project-workflow.md", (ASSETS / "workflow.md").read_bytes()
    )
    config = root / ".codex/config.toml"
    settings = root / ".claude/settings.json"
    if plan.read(config) is None:
        plan.put(
            config,
            '# Project defaults. Review permissions for your environment.\napproval_policy = "on-request"\nsandbox_mode = "workspace-write"\n',
        )
    else:
        plan.messages.append(
            f"WARN preserve {config}; manually review permission parity between tools"
        )
    if plan.read(settings) is None:
        plan.put(
            settings,
            json.dumps(
                {
                    "permissions": {
                        "deny": [
                            "Read(./.env)",
                            "Read(./.env.*)",
                            "Read(./secrets/**)",
                            "Read(./**/secrets/**)",
                            "Read(./**/.env)",
                            "Read(./**/.env.*)",
                        ]
                    }
                },
                indent=2,
            )
            + "\n",
        )
    else:
        plan.messages.append(
            f"WARN preserve {settings}; manually review permission parity between tools"
        )
    for source in roles():
        claude, codex = agent_outputs(source.read_text(), source.stem)
        local_path = root / ".claude/agents" / source.name
        selected = plan.read(local_path)
        selected_path = local_path
        defaults = {
            digest(source.read_bytes()),
            digest(claude.encode()),
            UPGRADE_HASHES.get("agents/" + source.name),
        }
        if selected is None:
            global_path = Path.home() / ".claude/agents" / source.name
            global_body = plan.read(global_path)
            if global_body is not None and digest(global_body) not in defaults:
                selected = global_body
                selected_path = global_path
        if selected is not None:
            # Keep Claude metadata intact while translating only its role body.
            claude = selected
            _, codex = agent_outputs(selected.decode(), source.stem)
            if digest(selected) not in defaults:
                plan.messages.append(
                    f"WARN converted preserved custom body from {selected_path}; Claude metadata is preserved, but review tool/model references and permission parity manually for Codex"
                )
        plan.put(local_path, claude)
        plan.put(root / ".codex/agents" / (source.stem + ".toml"), codex)
    plan.put(
        root / ".agents/skills/fix-issue/SKILL.md",
        (ASSETS / "fix-issue.md").read_bytes(),
    )
    plan.put(
        root / ".claude/skills/fix-issue/SKILL.md",
        "---\nname: fix-issue\ndescription: Diagnose and fix a reported project issue.\n---\n\nRead and follow the canonical skill at `.agents/skills/fix-issue/SKILL.md` relative to the project root.\n",
    )
    for name, content in [
        (
            "todo.md",
            "# Tasks\n\n## Plan\n\n- [ ] Define the next task.\n\n## Review\n\n",
        ),
        ("lessons.md", "# Lessons\n\nRecord corrections and prevention rules here.\n"),
    ]:
        if plan.read(root / "tasks" / name) is None:
            plan.put(root / "tasks" / name, content)
    ignore = root / ".gitignore"
    previous = plan.read(ignore) or b""
    lines = previous.decode(errors="replace").splitlines()
    missing = [
        line
        for line in [
            ".env",
            ".env.*",
            "**/.env",
            "**/.env.*",
            "secrets/",
            "**/secrets/",
        ]
        if line not in lines
    ]
    if missing:
        plan.put(
            ignore,
            previous
            + (b"\n" if previous and not previous.endswith(b"\n") else b"")
            + ("\n".join(missing) + "\n").encode(),
            replace=True,
        )


def install_skill(plan: Plan, destination: Path) -> None:
    manifest_path = destination / ".init-project-manifest.json"
    manifest_data = plan.read(manifest_path)
    manifest = json.loads(manifest_data) if manifest_data else {}
    if not isinstance(manifest, dict):
        raise TypeError(f"Invalid installation manifest: {manifest_path}")
    updated = dict(manifest)
    obsolete = {
        "assets/legacy/" + name: fingerprint
        for name, fingerprint in UPGRADE_HASHES.items()
    }
    obsolete["assets/legacy/skill-baseline.txt"] = UPGRADE_HASHES["SKILL.md"]
    obsolete.update({
        name: fingerprint for name, fingerprint in UPGRADE_HASHES.items()
        if name.startswith("agents/")
    })
    for relative, fingerprint in obsolete.items():
        target = destination / relative
        old = plan.read(target)
        if old is None:
            updated.pop(relative, None)
        elif digest(old) in {fingerprint, manifest.get(relative)}:
            plan.backup(target, old)
            plan.removals.append(target)
            plan.messages.append(f"REMOVE obsolete snapshot {target} (backed up)")
            updated.pop(relative, None)
        else:
            plan.messages.append(f"WARN preserve customized obsolete snapshot {target}")
    for source in sorted(SKILL.rglob("*")):
        if (
            not source.is_file()
            or "__pycache__" in source.parts
            or source.name.endswith(".pyc")
            or ".init-project-" in source.name
        ):
            continue
        relative = source.relative_to(SKILL)
        target = destination / relative
        current = plan.read(target)
        known = manifest.get(relative.as_posix())
        replace = current is not None and known == digest(current)
        if current is not None and digest(current) == UPGRADE_HASHES.get(relative.as_posix()):
            replace = True
        if plan.put(target, source.read_bytes(), replace=replace):
            updated[relative.as_posix()] = digest(source.read_bytes())
    plan.put(
        manifest_path,
        json.dumps(updated, indent=2, sort_keys=True) + "\n",
        replace=True,
    )


def install_user(plan: Plan, home: Path) -> None:
    for directory in [".agents/skills/init-project", ".claude/skills/init-project"]:
        install_skill(plan, home / directory)
    for source in roles():
        target = home / ".claude/agents" / source.name
        current = plan.read(target)
        canonical = source.read_text()
        claude, codex = agent_outputs(canonical, source.stem)
        old_default = current is not None and digest(current) == UPGRADE_HASHES.get(
            "agents/" + source.name
        )
        if current is not None and current != claude.encode() and not old_default:
            plan.put(target, claude)
            _, codex = agent_outputs(current.decode(), source.stem)
            plan.messages.append(
                f"WARN converted preserved custom body from {target}; review tool/model references and permission parity manually"
            )
        else:
            plan.put(
                target, claude, replace=old_default
            )
        plan.put(home / ".codex/agents" / (source.stem + ".toml"), codex)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--project", type=Path)
    mode.add_argument("--install-user", action="store_true")
    parser.add_argument(
        "--home", type=Path, help="User installation root (defaults to home directory)"
    )
    parser.add_argument(
        "--apply", action="store_true", help="Write planned changes; default is dry-run"
    )
    args = parser.parse_args()
    if args.home is not None and not args.install_user:
        parser.error("--home requires --install-user")
    try:
        plan = Plan(args.apply)
        if args.install_user:
            install_user(plan, (args.home or Path.home()).expanduser().absolute())
        else:
            project(plan, args.project.expanduser().absolute())
        plan.finish()
        return 0
    except (OSError, ValueError, TypeError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
