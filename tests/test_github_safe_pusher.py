import os
from types import SimpleNamespace
from unittest.mock import patch

import unittest

from fabrica_sw.github_safe_pusher import github_secure_push_tool


class GithubSecurePushToolTests(unittest.TestCase):
    APPROVED = {"is_approved": True}

    @patch.dict(os.environ, {"GITHUB_TOKEN": "token-super-secreto"}, clear=False)
    @patch("fabrica_sw.github_safe_pusher.subprocess.run")
    def test_verifies_head_before_pushing_without_exposing_token(self, run):
        run.side_effect = [
            SimpleNamespace(returncode=0, stdout="abc123", stderr=""),
            SimpleNamespace(
                returncode=0,
                stdout="push token-super-secreto completado",
                stderr="",
            ),
        ]

        result = github_secure_push_tool(self.APPROVED, "main")

        self.assertIn("Push exitoso a origin/main", result)
        self.assertNotIn("token-super-secreto", result)
        self.assertEqual(run.call_args_list[0].args[0], ["git", "rev-parse", "--verify", "HEAD"])
        self.assertEqual(run.call_args_list[1].args[0], ["git", "push", "origin", "main"])
        self.assertNotIn("token-super-secreto", run.call_args_list[1].args[0])
        self.assertTrue(all(call.kwargs["shell"] is False for call in run.call_args_list))
        push_env = run.call_args_list[1].kwargs["env"]
        self.assertEqual(push_env["GITHUB_TOKEN"], "token-super-secreto")
        self.assertEqual(push_env["GIT_TERMINAL_PROMPT"], "0")
        self.assertTrue(push_env["GIT_ASKPASS"])

    @patch("fabrica_sw.github_safe_pusher.subprocess.run")
    def test_requires_token_before_executing_git(self, run):
        with patch.dict(os.environ, {}, clear=True):
            result = github_secure_push_tool(self.APPROVED, "main")

        self.assertIn("falta GITHUB_TOKEN", result)
        run.assert_not_called()

    @patch.dict(os.environ, {"GITHUB_TOKEN": "token"}, clear=False)
    @patch("fabrica_sw.github_safe_pusher.subprocess.run")
    def test_rejected_state_does_not_push(self, run):
        with self.assertRaises(PermissionError):
            github_secure_push_tool({"is_approved": False}, "main")
        run.assert_not_called()

    @patch.dict(os.environ, {"GITHUB_TOKEN": "token"}, clear=False)
    @patch("fabrica_sw.github_safe_pusher.subprocess.run")
    def test_invalid_branch_does_not_push(self, run):
        with self.assertRaises(ValueError):
            github_secure_push_tool(self.APPROVED, "main; rm -rf")
        run.assert_not_called()

    @patch.dict(os.environ, {"GITHUB_TOKEN": "token"}, clear=False)
    @patch("fabrica_sw.github_safe_pusher.subprocess.run")
    def test_missing_head_does_not_push(self, run):
        run.return_value = SimpleNamespace(returncode=1, stdout="", stderr="sin HEAD")

        result = github_secure_push_tool(self.APPROVED, "main")

        self.assertIn("Error verificando commit local", result)
        self.assertEqual(run.call_count, 1)


if __name__ == "__main__":
    unittest.main()
