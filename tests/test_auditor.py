import unittest
from unittest.mock import patch

from fabrica_sw.auditor import (
    _calculate_completion_percentage,
    _extract_audit_decision,
    auditor_should_continue_router,
    auditor_node,
)
from fabrica_sw.state import create_initial_state


class FakeResponse:
    content = '{"is_approved": true, "audit_report": "Sin hallazgos críticos."}'


class FakeModel:
    def __init__(self):
        self.bound = None

    def bind_tools(self, tools):
        self.bound = tools
        return self

    def invoke(self, messages):
        self.messages = messages
        return FakeResponse()


class AuditorTests(unittest.TestCase):
    def test_auditor_usa_herramientas_y_extrae_aprobacion(self):
        model = FakeModel()
        state = create_initial_state("revisar autenticación")
        with patch("fabrica_sw.auditor._read_checklist", return_value="- [x] Uno\n- [ ] Dos\n"):
            update = auditor_node(state, model)

        self.assertTrue(update["is_approved"])
        self.assertEqual(update["audit_report"], "Sin hallazgos críticos.")
        self.assertEqual(update["completion_percentage"], 50.0)
        self.assertIsNotNone(model.bound)

    def test_sin_model_no_aprueba(self):
        state = create_initial_state("revisar autenticación")
        update = auditor_node(state)
        self.assertFalse(update["is_approved"])
        self.assertIn("pendiente", update["audit_report"])

    def test_respuesta_ambigua_no_aprueba(self):
        approved, report = _extract_audit_decision("La revisión continúa; no hay decisión.")
        self.assertFalse(approved)
        self.assertIn("no hay decisión", report)

    def test_calcula_checklist_markdown(self):
        self.assertEqual(_calculate_completion_percentage("- [x] A\n- [X] B\n- [ ] C\n"), 66.67)
        self.assertEqual(_calculate_completion_percentage("sin tareas"), 0.0)

    def test_router_detecta_llamada_de_herramienta(self):
        state = create_initial_state("revisar autenticaciÃ³n")
        state["messages"] = [{
            "role": "assistant",
            "content": "",
            "tool_calls": [{"name": "read_file_tool", "args": {}}],
        }]
        self.assertEqual(auditor_should_continue_router(state), "audit_execute_tools")


if __name__ == "__main__":
    unittest.main()
