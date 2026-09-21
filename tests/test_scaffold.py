"""Exercise scaffolding through its public CLI using isolated project and home trees."""

import hashlib
import json
import shutil
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "init-project" / "scripts" / "scaffold.py"
AGENTS = ("code-reviewer", "git-workflow", "doc-generator", "test-writer")


class ScaffoldTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / "project"
        self.home = self.root / "home"
        self.script = SCRIPT
        self.project.mkdir()
        self.home.mkdir()

    def run_cli(self, *args, successful=True):
        environment = dict(os.environ, HOME=str(self.home), PYTHONDONTWRITEBYTECODE="1")
        result = subprocess.run(
            [sys.executable, str(self.script), *map(str, args)],
            cwd=self.root,
            env=environment,
            text=True,
            capture_output=True,
            timeout=30,
            check=False,
        )
        if successful:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def scaffold(self, apply=True):
        return self.run_cli("--project", self.project, *(["--apply"] if apply else []))

    def install(self, apply=True):
        return self.run_cli(
            "--install-user", "--home", self.home, *(["--apply"] if apply else [])
        )

    def write(self, relative, content, root=None):
        target = (root or self.project) / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
        return target

    def snapshot(self, root):
        return {
            str(path.relative_to(root)): path.read_bytes()
            for path in root.rglob("*")
            if path.is_file()
        }

    def test_custom_local_and_global_roles_are_carried_to_codex(self):
        for scope in (self.home, self.project):
            role = scope / ".claude/agents/code-reviewer.md"
            role.parent.mkdir(parents=True, exist_ok=True)
            role.write_text(
                "---\nname: code-reviewer\ndescription: Custom reviewer\n---\nCUSTOM_CHECKLIST_REQUIRED\n"
            )
            self.scaffold()
            codex = tomllib.loads(
                (self.project / ".codex/agents/code-reviewer.toml").read_text()
            )
            self.assertIn("CUSTOM_CHECKLIST_REQUIRED", codex["developer_instructions"])
            self.assertIn("CUSTOM_CHECKLIST_REQUIRED", role.read_text())

    def test_nested_rules_are_referenced(self):
        rule = self.project / ".claude/rules/security/critical.md"
        rule.parent.mkdir(parents=True)
        rule.write_text("Keep this nested security rule.\n")
        self.scaffold()
        self.assertIn(
            ".claude/rules/security/critical.md",
            (self.project / "AGENTS.md").read_text(),
        )

    def use_old_defaults_fixture(self):
        skill = self.root / "source/init-project"
        shutil.copytree(ROOT / "init-project", skill)
        self.script = skill / "scripts/scaffold.py"
        hashes_path = skill / "assets/upgrade-hashes.json"
        hashes = json.loads(hashes_path.read_text())
        fixtures = {
            name: f"# Previous default: {name}\n".encode() for name in hashes
        }
        hashes_path.write_text(json.dumps({
            name: hashlib.sha256(body).hexdigest() for name, body in fixtures.items()
        }))
        return fixtures

    def test_old_defaults_upgrade_without_bundled_snapshots(self):
        fixtures = self.use_old_defaults_fixture()
        destination = self.home / ".agents/skills/init-project"
        for name in ("SKILL.md", "CLAUDE.md"):
            self.write(str(destination / name), fixtures[name].decode())
        for name, body in fixtures.items():
            if name.startswith("agents/"):
                self.write(".claude/" + name, body.decode(), root=self.home)
        before = self.snapshot(self.home)
        self.install(apply=False)
        self.assertEqual(self.snapshot(self.home), before)
        self.install()
        self.assertNotEqual((destination / "SKILL.md").read_bytes(), fixtures["SKILL.md"])
        for name in AGENTS:
            actual = (self.home / f".claude/agents/{name}.md").read_bytes()
            self.assertNotEqual(actual, fixtures[f"agents/{name}.md"])
        self.assertFalse((destination / "assets/legacy").exists())
        self.script = destination / "scripts/scaffold.py"
        before = self.snapshot(self.home)
        self.install()
        self.assertEqual(self.snapshot(self.home), before)
        self.scaffold()
        self.assertTrue((self.project / ".codex/agents/code-reviewer.toml").exists())

    def test_obsolete_snapshots_cleaned_and_customizations_preserved(self):
        fixtures = self.use_old_defaults_fixture()
        destination = self.home / ".agents/skills/init-project"
        old_paths = {
            "assets/legacy/SKILL.md": fixtures["SKILL.md"],
            "assets/legacy/skill-baseline.txt": fixtures["SKILL.md"],
            "assets/legacy/CLAUDE.md": fixtures["CLAUDE.md"],
            "assets/legacy/agents/code-reviewer.md": b"Managed previous version\n",
            "agents/code-reviewer.md": fixtures["agents/code-reviewer.md"],
        }
        for name, body in old_paths.items():
            self.write(str(destination / name), body.decode())
        manifest = {name: hashlib.sha256(body).hexdigest() for name, body in old_paths.items()}
        self.write(str(destination / ".init-project-manifest.json"), json.dumps(manifest))
        custom = destination / "assets/legacy/CLAUDE.md"
        custom.write_text("Customized instructions\n")
        before = self.snapshot(self.home)
        self.install(apply=False)
        self.assertEqual(self.snapshot(self.home), before)
        self.install()
        for name, body in old_paths.items():
            path = destination / name
            if path == custom:
                self.assertEqual(path.read_text(), "Customized instructions\n")
            else:
                self.assertFalse(path.exists())
                self.assertEqual(next(path.parent.glob(path.name + ".init-project-backup-*")).read_bytes(), body)
        self.assertEqual(len(list(destination.rglob("SKILL.md"))), 1)
        updated = json.loads((destination / ".init-project-manifest.json").read_text())
        self.assertNotIn("assets/legacy/SKILL.md", updated)
        self.assertIn("assets/legacy/CLAUDE.md", updated)
        before = self.snapshot(self.home)
        self.install()
        self.assertEqual(self.snapshot(self.home), before)

    def test_project_dry_run_does_not_write(self):
        self.scaffold(apply=False)
        self.assertEqual(list(self.project.iterdir()), [])
        self.assertEqual(list(self.home.iterdir()), [])

    def test_fresh_project_has_both_native_layouts_and_valid_config(self):
        self.scaffold()
        for relative in (
            "AGENTS.md",
            "CLAUDE.md",
            ".agents/project-workflow.md",
            ".claude/settings.json",
            ".codex/config.toml",
            "tasks/todo.md",
            "tasks/lessons.md",
        ):
            self.assertTrue((self.project / relative).is_file(), relative)
        json.loads((self.project / ".claude/settings.json").read_text())
        tomllib.loads((self.project / ".codex/config.toml").read_text())
        for name in AGENTS:
            self.assertTrue((self.project / f".claude/agents/{name}.md").is_file())
            role = self.project / f".codex/agents/{name}.toml"
            document = tomllib.loads(role.read_text())
            self.assertTrue(document.get("developer_instructions"), role)
        self.assertEqual(list(self.home.iterdir()), [])

    def test_project_rerun_is_idempotent(self):
        self.scaffold()
        before = self.snapshot(self.project)
        self.scaffold()
        self.assertEqual(self.snapshot(self.project), before)

    def test_legacy_instructions_and_tasks_survive_migration(self):
        originals = {
            "AGENTS.md": "# Local instructions\nUse our existing project conventions.\n",
            "CLAUDE.md": "# Existing Claude instructions\nFollow the billing conventions.\n",
            ".claude/CLAUDE.md": "# Existing workflow\nKeep operational checks.\n",
            ".Codex/AGENTS.md": "# Existing Codex workflow\nPreserve the deployment conventions.\n",
            ".claude/rules/custom.md": "# Custom rule\nUse deterministic identifiers.\n",
            ".claude/rules/frontend.md": '---\npaths:\n  - "frontend/**/*.tsx"\n---\nUse the existing component library.\n',
            "tasks/todo.md": "# Active work\n- [ ] Finish the migration\n",
            "tasks/lessons.md": "# Lessons\nPreserve user choices.\n",
        }
        for relative, content in originals.items():
            self.write(relative, content)
        self.scaffold()
        for relative, content in originals.items():
            actual = (self.project / relative).read_text()
            if relative in ("AGENTS.md", "CLAUDE.md"):
                self.assertIn(content, actual, relative)
            else:
                self.assertEqual(actual, content, relative)
        agents = (self.project / "AGENTS.md").read_text()
        for legacy in (
            "CLAUDE.md",
            ".claude/CLAUDE.md",
            ".Codex/AGENTS.md",
            ".claude/rules/custom.md",
            ".claude/rules/frontend.md",
        ):
            self.assertIn(legacy, agents)
        self.assertRegex(agents.lower(), r"scope[sd]?")
        self.assertIn("matching files", agents.lower())
        before = self.snapshot(self.project)
        self.scaffold()
        self.assertEqual(self.snapshot(self.project), before)

    def test_existing_claude_gets_shared_import_and_exact_original_backup(self):
        original = b"# Custom instructions\r\nPreserve non-ASCII text: caf\xc3\xa9."
        claude = self.project / "CLAUDE.md"
        claude.write_bytes(original)
        self.scaffold()
        self.assertTrue(claude.read_bytes().startswith(original))
        self.assertIn("@AGENTS.md", claude.read_text().splitlines())
        backups = list(self.project.glob("CLAUDE.md.init-project-backup-*"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_bytes(), original)
        before = self.snapshot(self.project)
        self.scaffold()
        self.assertEqual(self.snapshot(self.project), before)

    def test_existing_shared_import_is_not_duplicated(self):
        for reference in ("@AGENTS.md", "@./AGENTS.md"):
            with self.subTest(reference=reference):
                original = (
                    f"# Custom instructions\n{reference}\nKeep local conventions.\n"
                )
                self.write("CLAUDE.md", original)
                self.scaffold()
                self.assertEqual((self.project / "CLAUDE.md").read_text(), original)
                self.assertEqual(
                    list(self.project.glob("CLAUDE.md.init-project-backup-*")), []
                )

    def test_custom_settings_and_config_are_preserved(self):
        originals = {
            ".claude/settings.json": '{"permissions": {"allow": ["Bash(make test)"]}}\n',
            ".codex/config.toml": 'model = "custom-model"\n[projects.custom]\ntrust_level = "trusted"\n',
        }
        for relative, content in originals.items():
            self.write(relative, content)
        self.scaffold()
        for relative, content in originals.items():
            self.assertEqual((self.project / relative).read_text(), content)

    def test_gitignore_preserves_existing_entries_and_adds_sensitive_paths(self):
        original = "# Local build products\nartifacts/\n"
        self.write(".gitignore", original)
        self.scaffold()
        ignore = (self.project / ".gitignore").read_text()
        self.assertIn(original, ignore)
        entries = set(ignore.splitlines())
        self.assertIn(".env", entries)
        self.assertIn(".env.*", entries)
        self.assertTrue({"secrets/", "secrets/**"} & entries)

    def test_user_install_dry_run_does_not_write(self):
        self.install(apply=False)
        self.assertEqual(list(self.home.iterdir()), [])

    def test_user_install_supports_both_tools_and_is_idempotent(self):
        self.install()
        for tool in (".claude", ".agents"):
            skill = self.home / tool / "skills/init-project"
            self.assertTrue((skill / "SKILL.md").is_file(), skill)
            self.assertTrue((skill / "scripts/scaffold.py").is_file(), skill)
        for name in AGENTS:
            self.assertTrue((self.home / f".claude/agents/{name}.md").is_file())
            role = self.home / f".codex/agents/{name}.toml"
            self.assertTrue(
                tomllib.loads(role.read_text()).get("developer_instructions")
            )
        before = self.snapshot(self.home)
        self.install()
        self.assertEqual(self.snapshot(self.home), before)

    def test_install_preserves_custom_agents_and_extra_skill_files(self):
        custom = "---\nname: code-reviewer\ndescription: Custom reviewer\n---\n\nUse our custom review checklist.\n"
        self.write(".claude/agents/code-reviewer.md", custom, root=self.home)
        self.install()
        self.assertEqual(
            (self.home / ".claude/agents/code-reviewer.md").read_text(), custom
        )
        role = self.home / ".codex/agents/code-reviewer.toml"
        self.assertIn(
            "Use our custom review checklist.",
            tomllib.loads(role.read_text())["developer_instructions"],
        )
        extras = {}
        for tool in (".claude", ".agents"):
            relative = f"{tool}/skills/init-project/my-notes.md"
            extras[relative] = "Personal installation notes.\n"
            self.write(relative, extras[relative], root=self.home)
        self.install()
        for relative, content in extras.items():
            self.assertEqual((self.home / relative).read_text(), content)
        self.assertEqual(
            (self.home / ".claude/agents/code-reviewer.md").read_text(), custom
        )

    def test_install_preserves_customized_managed_skill_files(self):
        self.install()
        custom = (
            "# My customized initialization instructions\nPreserve this workflow.\n"
        )
        for tool in (".claude", ".agents"):
            self.write(f"{tool}/skills/init-project/SKILL.md", custom, root=self.home)
        self.install()
        for tool in (".claude", ".agents"):
            skill = self.home / tool / "skills/init-project/SKILL.md"
            self.assertEqual(skill.read_text(), custom)
            self.assertTrue(list(skill.parent.glob("SKILL.md.init-project-proposed*")))
        before = self.snapshot(self.home)
        self.install()
        self.assertEqual(self.snapshot(self.home), before)

    def test_project_symlink_escape_is_rejected_without_external_writes(self):
        outside = self.root / "outside"
        outside.mkdir()
        (self.project / ".claude").symlink_to(outside, target_is_directory=True)
        self.run_cli("--project", self.project, "--apply", successful=False)
        self.assertEqual(list(outside.iterdir()), [])

    def test_user_install_symlink_escape_is_rejected_without_external_writes(self):
        outside = self.root / "outside"
        outside.mkdir()
        (self.home / ".agents").symlink_to(outside, target_is_directory=True)
        self.run_cli("--install-user", "--home", self.home, "--apply", successful=False)
        self.assertEqual(list(outside.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
