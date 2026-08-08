import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import get_type_hints

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from fabrica_sw.state import (
    ArchitectureBlueprint,
    FactoryState,
    create_initial_state,
    validate_factory_state,
)
from fabrica_sw.persistence import (
    build_persistence_config,
    build_thread_config,
    resolve_database_path,
)
from fabrica_sw.workflow_policy import (
    MAX_ITERATIONS,
    ROUTE_DEVELOPER,
    ROUTE_DEPLOY,
    ROUTE_STOP,
    evaluate_workflow_router,
    evaluate_workflow_route,
)


class FactoryStateContractTests(unittest.TestCase):
    def test_canonical_state_contains_shared_fields(self) -> None:
        fields = set(get_type_hints(FactoryState, include_extras=True))
        self.assertEqual(
            fields,
            {
                "messages",
                "user_requirement",
                "architecture_blueprint",
                "source_code_draft",
                "test_results",
                "is_approved",
                "audit_report",
                "iteration_count",
                "tool_round_count",
                "completion_percentage",
            },
        )

    def test_blueprint_can_carry_impact_information(self) -> None:
        blueprint: ArchitectureBlueprint = {
            "status": "planned",
            "impacted_files": ["src/auth.py"],
            "dependencies": ["database"],
        }
        self.assertEqual(blueprint["impacted_files"], ["src/auth.py"])

    def test_initial_state_has_safe_defaults(self) -> None:
        state = create_initial_state("Implementar autenticación")
        self.assertEqual(state["user_requirement"], "Implementar autenticación")
        self.assertEqual(state["architecture_blueprint"], {})
        self.assertEqual(state["source_code_draft"], {})
        self.assertEqual(state["test_results"], "")
        self.assertFalse(state["is_approved"])
        self.assertEqual(state["iteration_count"], 0)
        self.assertEqual(state["tool_round_count"], 0)
        self.assertEqual(state["completion_percentage"], 0.0)

    def test_invalid_progress_is_rejected(self) -> None:
        state = create_initial_state("Implementar autenticación")
        state["completion_percentage"] = 101
        with self.assertRaisesRegex(ValueError, "entre 0 y 100"):
            validate_factory_state(state)

    def test_invalid_impacted_files_are_rejected(self) -> None:
        state = create_initial_state("Implementar autenticación")
        state["architecture_blueprint"] = {"impacted_files": [""]}
        with self.assertRaisesRegex(ValueError, "impacted_files"):
            validate_factory_state(state)

    def test_empty_requirement_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "no vacío"):
            create_initial_state("   ")


    def test_thread_config_is_explicit_and_normalized(self) -> None:
        self.assertEqual(
            build_thread_config("  proyecto-auth  "),
            {"configurable": {"thread_id": "proyecto-auth"}},
        )

    def test_blank_thread_id_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            build_thread_config(" ")

    def test_persistence_uses_factory_database_path(self) -> None:
        with TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "state" / "factory_state.db"
            config = build_persistence_config("run-001", db_path)

            self.assertEqual(config["db_path"], str(db_path))
            self.assertEqual(config["config"]["configurable"]["thread_id"], "run-001")
            self.assertTrue(db_path.parent.is_dir())

    def test_database_path_is_created_without_touching_database(self) -> None:
        with TemporaryDirectory() as temp_dir:
            db_path = resolve_database_path(Path(temp_dir) / "nested" / "factory_state.db")
            self.assertEqual(db_path.name, "factory_state.db")
            self.assertFalse(db_path.exists())

    def test_unapproved_state_routes_to_developer_before_limit(self) -> None:
        self.assertEqual(
            evaluate_workflow_route({"iteration_count": MAX_ITERATIONS - 1}),
            ROUTE_DEVELOPER,
        )

    def test_approved_state_routes_to_deploy_before_limit(self) -> None:
        self.assertEqual(
            evaluate_workflow_route({"iteration_count": 0, "is_approved": True}),
            ROUTE_DEPLOY,
        )

    def test_canonical_router_routes_unapproved_state_to_developer(self) -> None:
        self.assertEqual(
            evaluate_workflow_router({"iteration_count": 0, "is_approved": False}),
            ROUTE_DEVELOPER,
        )

    def test_canonical_router_routes_approved_state_to_deploy(self) -> None:
        self.assertEqual(
            evaluate_workflow_router({"iteration_count": 0, "is_approved": True}),
            ROUTE_DEPLOY,
        )

    def test_canonical_router_stops_at_iteration_limit(self) -> None:
        self.assertEqual(
            evaluate_workflow_router({"iteration_count": MAX_ITERATIONS}),
            ROUTE_STOP,
        )

    def test_iteration_limit_routes_to_stop(self) -> None:
        self.assertEqual(
            evaluate_workflow_route(
                {"iteration_count": MAX_ITERATIONS, "is_approved": False}
            ),
            ROUTE_STOP,
        )

    def test_invalid_iteration_policy_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            evaluate_workflow_route({"iteration_count": -1})
        with self.assertRaises(ValueError):
            evaluate_workflow_route({"iteration_count": 0}, max_iterations=0)


if __name__ == "__main__":
    unittest.main()
