import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from fabrica_sw.auditor import auditor_node
from fabrica_sw.developer import developer_node
from fabrica_sw.state import create_initial_state
from fabrica_sw.workflow_policy import (
    MAX_ITERATIONS,
    ROUTE_DEPLOY,
    ROUTE_DEVELOPER,
    ROUTE_STOP,
    evaluate_workflow_router,
)


class FakeResponse:
    def __init__(self, content: str) -> None:
        self.content = content


class DeveloperModel:
    def bind_tools(self, tools):
        self.tools = tools
        return self

    def invoke(self, messages):
        return FakeResponse("Corrección implementada; listo para auditoría.")


class AuditorModel:
    def __init__(self, decisions: list[bool]) -> None:
        self.decisions = iter(decisions)

    def bind_tools(self, tools):
        self.tools = tools
        return self

    def invoke(self, messages):
        approved = next(self.decisions)
        report = "Aprobado" if approved else "Fallo pendiente; requiere corrección."
        return FakeResponse(
            f'{{"is_approved": {str(approved).lower()}, "audit_report": "{report}"}}'
        )


def run_cycle(auditor_decisions: list[bool]) -> list[str]:
    state = create_initial_state("Implementar autenticación")
    state["architecture_blueprint"] = {"impacted_files": ["src/auth.py"]}
    developer = DeveloperModel()
    auditor = AuditorModel(auditor_decisions)
    routes: list[str] = []

    while True:
        state.update(developer_node(state, developer))
        state.update(auditor_node(state, auditor))
        route = evaluate_workflow_router(state)
        routes.append(route)
        if route != ROUTE_DEVELOPER:
            return routes


class WorkflowCycleTests(unittest.TestCase):
    def test_developer_auditor_correction_then_deploy(self):
        routes = run_cycle([False, True])

        self.assertEqual(routes, [ROUTE_DEVELOPER, ROUTE_DEPLOY])

    def test_developer_auditor_stops_at_iteration_limit(self):
        routes = run_cycle([False] * MAX_ITERATIONS)

        self.assertEqual(routes, [ROUTE_DEVELOPER] * (MAX_ITERATIONS - 1) + [ROUTE_STOP])


if __name__ == "__main__":
    unittest.main()
