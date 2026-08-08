from types import SimpleNamespace
from unittest.mock import patch

import unittest

from fabrica_sw.git_tools import git_secure_commit_tool


class GitSecureCommitToolTests(unittest.TestCase):
    APPROVED = {"is_approved": True}

    @patch("fabrica_sw.git_tools.subprocess.run")
    def test_commits_only_explicitly_selected_files(self, run):
        run.side_effect = [
            SimpleNamespace(returncode=0, stdout="", stderr=""),
            SimpleNamespace(returncode=0, stdout="[main] ok", stderr=""),
        ]

        result = git_secure_commit_tool(
            self.APPROVED,
            ["docs/PLAN_IMPLEMENTACION.md", "src/fabrica_sw/git_tools.py"],
            "Implementar commit seguro",
        )

        self.assertIn("Commit creado", result)
        add_command = run.call_args_list[0].args[0]
        commit_command = run.call_args_list[1].args[0]
        self.assertEqual(add_command[:3], ["git", "add", "--"])
        self.assertNotIn(".", add_command)
        self.assertEqual(commit_command[:3], ["git", "commit", "-m"])
        self.assertEqual(commit_command[3], "[fabrica-sw] Implementar commit seguro")
        self.assertTrue(all(call.kwargs["shell"] is False for call in run.call_args_list))

    @patch("fabrica_sw.git_tools.subprocess.run")
    def test_rejected_state_does_not_execute_git(self, run):
        with self.assertRaises(PermissionError):
            git_secure_commit_tool(
                {"is_approved": False},
                ["docs/PLAN_IMPLEMENTACION.md"],
                "No debe ejecutarse",
            )
        run.assert_not_called()

    @patch("fabrica_sw.git_tools.subprocess.run")
    def test_rejects_path_outside_workspace(self, run):
        with self.assertRaises(ValueError):
            git_secure_commit_tool(
                self.APPROVED,
                ["../fuera-del-workspace.txt"],
                "Ruta inválida",
            )
        run.assert_not_called()

    @patch("fabrica_sw.git_tools.subprocess.run")
    def test_add_failure_does_not_run_commit(self, run):
        run.return_value = SimpleNamespace(returncode=1, stdout="", stderr="no es repo")

        result = git_secure_commit_tool(
            self.APPROVED,
            ["docs/PLAN_IMPLEMENTACION.md"],
            "Debe fallar de forma controlada",
        )

        self.assertIn("Error preparando commit", result)
        self.assertEqual(run.call_count, 1)


if __name__ == "__main__":
    unittest.main()
