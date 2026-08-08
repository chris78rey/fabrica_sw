from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class GraphifyHookTests(unittest.TestCase):
    def test_versionable_post_commit_hook_rebuilds_code_graph(self):
        hook = (PROJECT_ROOT / ".githooks" / "post-commit").read_text(encoding="utf-8")

        self.assertIn("post-commit", hook)
        self.assertIn("graphify.exe", hook)
        self.assertIn("update", hook)
        self.assertIn("--code-only", hook)
        self.assertIn("--no-cluster", hook)
        self.assertIn("exit 0", hook)
        self.assertNotIn("git add .", hook)

    def test_install_script_uses_versionable_hooks_path(self):
        installer = (
            PROJECT_ROOT / "scripts" / "install-git-hooks.ps1"
        ).read_text(encoding="utf-8")

        self.assertIn("core.hooksPath .githooks", installer)
        self.assertIn(".git", installer)
        self.assertIn("No existe un repositorio Git", installer)


if __name__ == "__main__":
    unittest.main()
