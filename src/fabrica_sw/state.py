"""Contratos de estado compartidos por el flujo Graphify/LangGraph."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated, Any, Sequence, TypedDict

from .task_planner import build_tasks

try:
    from langchain_core.messages import BaseMessage
except ImportError:  # Permite validar el contrato sin instalar LangChain.
    BaseMessage = Any  # type: ignore[misc, assignment]

try:
    from langgraph.graph.message import add_messages
except ImportError:  # Fallback para las pruebas unitarias del contrato.
    def add_messages(left: Sequence[Any], right: Sequence[Any]) -> list[Any]:
        """Combina mensajes sin mutar las secuencias de entrada."""

        return [*left, *right]


class ArchitectureBlueprint(TypedDict, total=False):
    """Resultado de arquitectura que acota el trabajo del desarrollador."""

    status: str
    summary: str
    impacted_files: list[str]
    dependencies: list[str]
    rules: list[str]
    graph_context: str
    last_architect_thought: str


class FactoryState(TypedDict, total=False):
    """Estado canónico compartido por arquitectura, desarrollo y auditoría."""

    messages: Annotated[Sequence[BaseMessage], add_messages]
    user_requirement: str
    architecture_blueprint: ArchitectureBlueprint
    source_code_draft: dict[str, str]
    test_results: str
    is_approved: bool
    audit_report: str
    iteration_count: int
    tool_round_count: int
    completion_percentage: float
    tasks: list[dict[str, Any]]
    current_task_index: int
    validation_available: bool
    validation_passed: bool
    validation_exit_code: int | None
    changed_files: list[str]


REQUIRED_FACTORY_STATE_FIELDS = frozenset(
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
    }
)


def create_initial_state(user_requirement: str) -> FactoryState:
    """Crea un estado completo y seguro para iniciar una ejecución."""

    if not isinstance(user_requirement, str) or not user_requirement.strip():
        raise ValueError("user_requirement debe ser un texto no vacío")

    tasks = build_tasks(user_requirement.strip())
    current_task_index = next(
        (index for index, task in enumerate(tasks) if not task.get("completed", False)),
        max(len(tasks) - 1, 0),
    )
    state: FactoryState = {
        "messages": [],
        "user_requirement": user_requirement.strip(),
        "architecture_blueprint": {},
        "source_code_draft": {},
        "test_results": "",
        "is_approved": False,
        "audit_report": "",
        "iteration_count": 0,
        "tool_round_count": 0,
        "completion_percentage": 0.0,
        "tasks": tasks,
        "current_task_index": current_task_index,
        "validation_available": False,
        "validation_passed": False,
        "validation_exit_code": None,
        "changed_files": [],
    }
    validate_factory_state(state)
    return state


def validate_factory_state(state: Mapping[str, Any]) -> None:
    """Valida la forma y los límites del estado completo.

    Los nodos pueden seguir devolviendo actualizaciones parciales; esta
    función se aplica al estado inicial y a los puntos de persistencia.
    """

    missing = REQUIRED_FACTORY_STATE_FIELDS.difference(state)
    if missing:
        raise ValueError(f"FactoryState incompleto; faltan: {sorted(missing)}")

    if not isinstance(state["user_requirement"], str) or not state["user_requirement"].strip():
        raise ValueError("user_requirement debe ser un texto no vacío")
    if not isinstance(state["architecture_blueprint"], Mapping):
        raise ValueError("architecture_blueprint debe ser un mapa")
    impacted_files = state["architecture_blueprint"].get("impacted_files", [])
    if not isinstance(impacted_files, list) or any(
        not isinstance(path, str) or not path.strip() for path in impacted_files
    ):
        raise ValueError("architecture_blueprint.impacted_files debe ser una lista de rutas")
    if not isinstance(state["source_code_draft"], Mapping):
        raise ValueError("source_code_draft debe ser un mapa de rutas a texto")
    if any(not isinstance(path, str) or not isinstance(content, str)
           for path, content in state["source_code_draft"].items()):
        raise ValueError("source_code_draft debe contener pares texto -> texto")
    if not isinstance(state["test_results"], str):
        raise ValueError("test_results debe ser texto")
    if not isinstance(state["is_approved"], bool):
        raise ValueError("is_approved debe ser booleano")
    if not isinstance(state["audit_report"], str):
        raise ValueError("audit_report debe ser texto")
    if not isinstance(state["messages"], Sequence) or isinstance(state["messages"], (str, bytes)):
        raise ValueError("messages debe ser una secuencia")
    if not isinstance(state["iteration_count"], int) or isinstance(state["iteration_count"], bool):
        raise ValueError("iteration_count debe ser un entero")
    if state["iteration_count"] < 0:
        raise ValueError("iteration_count no puede ser negativo")
    if not isinstance(state["tool_round_count"], int) or isinstance(state["tool_round_count"], bool):
        raise ValueError("tool_round_count debe ser un entero")
    if state["tool_round_count"] < 0:
        raise ValueError("tool_round_count no puede ser negativo")
    if not isinstance(state["completion_percentage"], (int, float)) or isinstance(
        state["completion_percentage"], bool
    ):
        raise ValueError("completion_percentage debe ser numérico")
    if not 0 <= state["completion_percentage"] <= 100:
        raise ValueError("completion_percentage debe estar entre 0 y 100")
    if "tasks" in state:
        tasks = state["tasks"]
        if not isinstance(tasks, list) or not tasks or any(
            not isinstance(task, Mapping)
            or not isinstance(task.get("id"), str)
            or not isinstance(task.get("title"), str)
            or not isinstance(task.get("completed"), bool)
            for task in tasks
        ):
            raise ValueError("tasks debe ser una lista de tareas con id, title y completed")
        index = state.get("current_task_index", 0)
        if not isinstance(index, int) or isinstance(index, bool) or not 0 <= index < len(tasks):
            raise ValueError("current_task_index está fuera de rango")
    if "validation_available" in state and not isinstance(state["validation_available"], bool):
        raise ValueError("validation_available debe ser booleano")
    if "validation_passed" in state and not isinstance(state["validation_passed"], bool):
        raise ValueError("validation_passed debe ser booleano")
    if "validation_exit_code" in state and state["validation_exit_code"] is not None and not isinstance(
        state["validation_exit_code"], int
    ):
        raise ValueError("validation_exit_code debe ser entero o None")
    if "changed_files" in state and (
        not isinstance(state["changed_files"], list)
        or any(not isinstance(path, str) for path in state["changed_files"])
    ):
        raise ValueError("changed_files debe ser una lista de rutas")
