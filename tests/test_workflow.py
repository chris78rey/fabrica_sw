import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from fabrica_sw.state import create_initial_state
from fabrica_sw.developer import MAX_TOOL_ROUNDS
from fabrica_sw.workflow import (
    LocalAutonomousFactory,
    _execute_tools_with_limit,
    build_autonomous_factory,
    consolidate_developer_evidence,
    complete_current_task_node,
)
from fabrica_sw.test_profiles import detect_test_command


class FakeResponse:
    def __init__(self, content: str) -> None:
        self.content = content


class ToolCallResponse:
    def __init__(self, tool_calls: list[dict], content: str = "") -> None:
        self.content = content
        self.tool_calls = tool_calls


class FakeModel:
    def __init__(self, responses: list[str]) -> None:
        self.responses = iter(responses)

    def bind_tools(self, tools):
        return self

    def invoke(self, messages):
        return FakeResponse(next(self.responses))


class AuditorToolModel:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.bound = None

    def bind_tools(self, tools):
        self.bound = tools
        return self

    def invoke(self, messages):
        return next(self.responses)


class WorkflowConstructionTests(unittest.TestCase):
    def test_task_is_completed_only_after_quality_gate(self):
        state = create_initial_state("1. Crear escena\n2. Validar movimiento")
        self.assertEqual(state["current_task_index"], 0)
        self.assertFalse(state["tasks"][0]["completed"])
        result = complete_current_task_node(state)
        self.assertTrue(result["tasks"][0]["completed"])
        self.assertEqual(result["current_task_index"], 1)
        self.assertEqual(result["completion_percentage"], 50.0)

    def test_fallback_executes_architect_developer_auditor_and_delivery(self):
        app = LocalAutonomousFactory(
            FakeModel(["Blueprint listo"]),
            FakeModel(["Implementación lista"]),
            FakeModel(['{"is_approved": true, "audit_report": "OK"}']),
        )

        # LangGraph es la implementación preferida cuando está instalado; el
        # fallback local solo se usa en entornos sin esa dependencia.
        self.assertIsInstance(app, LocalAutonomousFactory)
        with patch(
            "fabrica_sw.workflow.execute_test_command",
            return_value="--- STDOUT ---\nOK\n\nComando finalizado con código de salida 0.",
        ):
            result = app.invoke(create_initial_state("Implementar autenticación"))

        self.assertTrue(result["is_approved"])
        self.assertEqual(result["iteration_count"], 1)
        self.assertIn("Comando finalizado", result["test_results"])
        self.assertIn("entrega preparada", result["messages"][-1]["content"])

    def test_consolidates_impacted_files_and_test_results(self):
        with patch("fabrica_sw.workflow.read_file_tool", return_value="contenido actual") as read_file, patch(
            "fabrica_sw.workflow.execute_test_command",
            return_value="--- STDOUT ---\nOK\n\nComando finalizado con código de salida 0.",
        ) as execute_tests:
            result = consolidate_developer_evidence(
                {
                    "architecture_blueprint": {
                        "impacted_files": ["src/auth.py", "src/auth.py"]
                    }
                }
            )

        self.assertEqual(result["source_code_draft"], {"src/auth.py": "contenido actual"})
        self.assertIn("salida 0", result["test_results"])
        read_file.assert_called_once_with("src/auth.py")
        execute_tests.assert_called_once_with(detect_test_command(Path.cwd()))

    def test_tool_round_limit_stops_repeated_calls(self):
        state = create_initial_state("Implementar autenticación")
        state["tool_round_count"] = MAX_TOOL_ROUNDS
        result = _execute_tools_with_limit(state, object())
        self.assertEqual(MAX_TOOL_ROUNDS, result["tool_round_count"])
        self.assertIn("límite de 8 rondas", result["messages"][0]["content"])


    def test_auditor_ejecuta_herramienta_y_recibe_su_resultado(self):
        auditor = AuditorToolModel(
            [
                ToolCallResponse(
                    [{
                        "name": "read_file_tool",
                        "args": {"file_path": "docs/PLAN_IMPLEMENTACION.md"},
                        "id": "audit-1",
                    }]
                ),
                FakeResponse('{"is_approved": true, "audit_report": "Evidencia verificada"}'),
            ]
        )
        app = LocalAutonomousFactory(
            FakeModel(["Blueprint listo"]),
            FakeModel(["ImplementaciÃ³n lista"]),
            auditor,
        )

        with patch(
            "fabrica_sw.workflow.execute_test_command",
            return_value="--- STDOUT ---\nOK\n\nComando finalizado con código de salida 0.",
        ):
            result = app.invoke(create_initial_state("Revisar el flujo"))

        self.assertTrue(result["is_approved"])
        self.assertEqual(result["tool_round_count"], 1)
        self.assertTrue(
            any(
                (message.get("role") if isinstance(message, dict) else getattr(message, "role", None))
                == "tool"
                for message in result["messages"]
            )
        )
        self.assertEqual(
            {tool.__name__ for tool in auditor.bound},
            {
                "read_file_tool",
                "execute_test_command",
                "graphify_query_tool",
                "graphify_shortest_path_tool",
            },
        )


if __name__ == "__main__":
    unittest.main()
