import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from fabrica_sw.developer import (
    LocalToolNode,
    ROUTE_EXECUTE_TOOLS,
    ROUTE_POST_PROCESS,
    developer_node,
    should_continue_router,
)


class FakeResponse:
    content = "Implementación propuesta"


class FakeModel:
    def bind_tools(self, tools):
        self.tools = tools
        return self

    def invoke(self, messages):
        self.messages = messages
        return FakeResponse()


class DeveloperNodeTests(unittest.TestCase):
    def test_binds_safe_tools_and_increments_iteration(self):
        model = FakeModel()
        result = developer_node(
            {
                "user_requirement": "crear endpoint",
                "architecture_blueprint": {"impacted_files": ["src/api.py"]},
                "iteration_count": 2,
            },
            model,
        )
        self.assertEqual(3, result["iteration_count"])
        self.assertIn("src/api.py", model.messages[1]["content"])
        self.assertTrue(model.tools)

    def test_without_model_does_not_write_files(self):
        result = developer_node({"user_requirement": "crear endpoint"})
        self.assertEqual(1, result["iteration_count"])
        self.assertIn("llamadas de herramientas", result["messages"][0]["content"])

    def test_local_tool_node_dispatches_only_registered_tools(self):
        def allowed(value: str) -> str:
            return value.upper()

        node = LocalToolNode([allowed])
        result = node.invoke({"messages": [{"tool_calls": [{"name": "allowed", "args": {"value": "ok"}, "id": "1"}]}]})
        self.assertEqual("OK", result["messages"][0]["content"])

        denied = node.invoke({"messages": [{"tool_calls": [{"name": "os.system", "args": {}}]}]})
        self.assertIn("no permitida", denied["messages"][0]["content"])

    def test_rejects_blank_requirement(self):
        with self.assertRaisesRegex(ValueError, "user_requirement"):
            developer_node({"user_requirement": " "})

    def test_router_sends_tool_calls_to_executor(self):
        state = {"messages": [{"tool_calls": [{"name": "allowed", "args": {}}]}]}
        self.assertEqual(ROUTE_EXECUTE_TOOLS, should_continue_router(state))

    def test_router_finishes_when_model_has_no_tool_calls(self):
        self.assertEqual(ROUTE_POST_PROCESS, should_continue_router({"messages": [{"content": "listo"}]}))

    def test_developer_preserves_previous_messages_after_tool_execution(self):
        model = FakeModel()
        developer_node(
            {
                "user_requirement": "crear endpoint",
                "architecture_blueprint": {},
                "messages": [
                    {"role": "assistant", "content": "Solicito leer src/api.py", "tool_calls": [{"name": "read_file_tool", "args": {}}]},
                    {"role": "tool", "content": "contenido de api.py", "tool_call_id": "1"},
                ],
                "iteration_count": 1,
            },
            model,
        )
        self.assertEqual(3, len(model.messages))
        self.assertEqual("tool", model.messages[-1]["role"])
        self.assertEqual("contenido de api.py", model.messages[-1]["content"])


if __name__ == "__main__":
    unittest.main()
