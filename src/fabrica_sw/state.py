"""Contratos de estado compartidos por el flujo Graphify/LangGraph."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated, Any, Sequence, TypedDict

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
