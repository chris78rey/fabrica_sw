import os
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from fabrica_sw.architect import architect_node
from fabrica_sw.auditor import auditor_node
from fabrica_sw.developer import developer_node
from fabrica_sw.github_safe_pusher import github_secure_push_tool
from fabrica_sw.git_tools import git_secure_commit_tool
from fabrica_sw.state import create_initial_state
from fabrica_sw.workflow_policy import ROUTE_DEPLOY, evaluate_workflow_router


class ApprovalModel:
    def invoke(self, messages):
        return SimpleNamespace(
            content='{"is_approved": true, "audit_report": "Pruebas y archivos verificados."}'
        )


class EndToEndWorkflowTests(unittest.TestCase):
    @patch.dict(os.environ, {"GITHUB_TOKEN": "test-token"}, clear=False)
    def test_architecture_to_synchronization(self):
        with (
            patch(
                "fabrica_sw.architect.graphify_query_tool",
                return_value="Graphify simulado",
            ),
            patch("fabrica_sw.git_tools.subprocess") as git_subprocess,
            patch("fabrica_sw.github_safe_pusher.subprocess") as push_subprocess,
        ):
            git_subprocess.run.side_effect = [
                SimpleNamespace(returncode=0, stdout="", stderr=""),
                SimpleNamespace(returncode=0, stdout="commit ok", stderr=""),
            ]
            push_subprocess.run.side_effect = [
                SimpleNamespace(returncode=0, stdout="abc123", stderr=""),
                SimpleNamespace(returncode=0, stdout="push ok", stderr=""),
            ]

            state = create_initial_state("Implementar autenticación segura")
            state.update(architect_node(state))
            self.assertEqual(state["architecture_blueprint"]["status"], "planned")

            state.update(developer_node(state))
            self.assertEqual(state["iteration_count"], 1)
            state["source_code_draft"] = {
                "src/fabrica_sw/auth_security.py": "implementación"
            }
            state["test_results"] = "74 pruebas OK"

            state.update(auditor_node(state, ApprovalModel()))
            self.assertTrue(state["is_approved"])
            self.assertEqual(evaluate_workflow_router(state), ROUTE_DEPLOY)

            commit_result = git_secure_commit_tool(
                state,
                ["src/fabrica_sw/auth_security.py"],
                "Implementar autenticación segura",
            )
            push_result = github_secure_push_tool(state, "main")

            self.assertIn("Commit creado", commit_result)
            self.assertIn("Push exitoso", push_result)
            self.assertEqual(git_subprocess.run.call_count, 2)
            self.assertEqual(push_subprocess.run.call_count, 2)


if __name__ == "__main__":
    unittest.main()
