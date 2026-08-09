"""Orquestación segura del flujo Arquitecto -> Desarrollo -> Auditoría.

El módulo mantiene un fallback local para que el proyecto siga siendo ejecutable
cuando LangGraph no está instalado. La etapa de entrega es deliberadamente
inocua: deja el estado listo para que el caller invoque Git de forma explícita.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
import shutil
from typing import Any

from .auditor import (
    AUDITOR_TOOLS,
    ROUTE_AUDIT_EXECUTE_TOOLS,
    auditor_node,
    auditor_should_continue_router,
)
from .architect import architect_node
from .developer import (
    MAX_TOOL_ROUNDS,
    LocalToolNode,
    ROUTE_EXECUTE_TOOLS,
    ROUTE_POST_PROCESS,
    build_tool_executor_node,
    developer_node,
    should_continue_router,
)
from .state import FactoryState
from .safe_factory_tools import (
    SAFE_DEVELOPMENT_TOOLS,
    WORKSPACE_COMMAND_DIR,
    execute_test_command,
    read_file_tool,
)
from .test_profiles import detect_test_command
from .workflow_policy import (
    MAX_ITERATIONS,
    ROUTE_DEPLOY,
    ROUTE_DEVELOPER,
    ROUTE_STOP,
    evaluate_workflow_router,
)


def deploy_and_sync_node(state: FactoryState) -> dict[str, Any]:
    """Marca la entrega como preparada sin producir efectos externos."""

    return {
        "messages": [
            {
                "role": "assistant",
                "content": (
                    "Auditoría aprobada; entrega preparada. "
                    "Commit, push y sincronización Graphify requieren invocación explícita."
                ),
            }
        ]
    }


def consolidate_developer_evidence(state: FactoryState) -> dict[str, Any]:
    """Consolida archivos impactados y pruebas antes de invocar al Auditor."""

    blueprint = state.get("architecture_blueprint", {})
    impacted_files = blueprint.get("impacted_files", []) if isinstance(blueprint, Mapping) else []
    if not isinstance(impacted_files, list) or any(
        not isinstance(path, str) or not path.strip() for path in impacted_files
    ):
        raise ValueError("architecture_blueprint.impacted_files debe ser una lista de rutas")

    source_code_draft = {
        path: read_file_tool(path)
        for path in dict.fromkeys(impacted_files)
    }
    test_command = detect_test_command(WORKSPACE_COMMAND_DIR)
    if test_command and shutil.which(test_command[0]) is None:
        test_command = None
    test_results = (
        execute_test_command(test_command)
        if test_command
        else "No se detectó un comando de pruebas seguro para este proyecto."
    )
    return {
        "source_code_draft": source_code_draft,
        "test_results": test_results,
        "tool_round_count": 0,
        "messages": [
            {
                "role": "assistant",
                "content": (
                    "Evidencia consolidada: "
                    f"{len(source_code_draft)} archivo(s) inspeccionado(s). "
                    "Resultados de pruebas disponibles para Auditoría."
                ),
            }
        ],
    }


def _merge_state(state: FactoryState, update: Mapping[str, Any]) -> FactoryState:
    """Aplica una actualización de nodo conservando la secuencia de mensajes."""

    merged = dict(state)
    for key, value in update.items():
        if key == "messages" and value:
            merged[key] = list(merged.get(key, [])) + list(value)
        else:
            merged[key] = value
    return merged  # type: ignore[return-value]


def _execute_tools_with_limit(state: FactoryState, tool_node: Any) -> dict[str, Any]:
    """Ejecuta herramientas y corta ciclos repetitivos de forma determinista."""

    rounds = state.get("tool_round_count", 0)
    if not isinstance(rounds, int) or isinstance(rounds, bool) or rounds < 0:
        raise ValueError("tool_round_count debe ser un entero no negativo")
    if rounds >= MAX_TOOL_ROUNDS:
        return {
            "messages": [
                {
                    "role": "assistant",
                    "content": (
                        "Se detuvo el ciclo de herramientas por alcanzar el límite de "
                        f"{MAX_TOOL_ROUNDS} rondas. La auditoría debe revisar el resultado."
                    ),
                }
            ],
            "tool_round_count": rounds,
        }
    update = tool_node.invoke(state)
    return {**update, "tool_round_count": rounds + 1}


class LocalAutonomousFactory:
    """Ejecutor determinista del flujo cuando LangGraph no está disponible."""

    def __init__(
        self,
        architect_model: Any,
        developer_model: Any,
        auditor_model: Any,
        *,
        max_iterations: int = MAX_ITERATIONS,
        deploy_node: Callable[[FactoryState], Mapping[str, Any]] = deploy_and_sync_node,
    ) -> None:
        self.architect_model = architect_model
        self.developer_model = developer_model
        self.auditor_model = auditor_model
        self.max_iterations = max_iterations
        self.deploy_node = deploy_node
        # El fallback debe aceptar respuestas simples de modelos locales y no
        # depender del contrato estricto AIMessage de LangGraph ToolNode.
        self.tool_node = LocalToolNode(SAFE_DEVELOPMENT_TOOLS)
        self.audit_tool_node = LocalToolNode(AUDITOR_TOOLS)

    def invoke(
        self,
        state: FactoryState,
        config: Mapping[str, Any] | None = None,
    ) -> FactoryState:
        del config
        current = _merge_state(state, architect_node(state, self.architect_model))
        current = self._run_developer_cycle(current)
        current = _merge_state(current, consolidate_developer_evidence(current))

        while True:
            current = _merge_state(current, auditor_node(current, self.auditor_model))
            if auditor_should_continue_router(current) == ROUTE_AUDIT_EXECUTE_TOOLS:
                current = _merge_state(
                    current,
                    _execute_tools_with_limit(current, self.audit_tool_node),
                )
                continue
            route = evaluate_workflow_router(current, max_iterations=self.max_iterations)
            if route == ROUTE_DEPLOY:
                return _merge_state(current, self.deploy_node(current))
            if route == ROUTE_STOP:
                return current
            current = self._run_developer_cycle(current)
            current = _merge_state(current, consolidate_developer_evidence(current))

    def _run_developer_cycle(self, state: FactoryState) -> FactoryState:
        current = state
        while True:
            current = _merge_state(current, developer_node(current, self.developer_model))
            if should_continue_router(current) != ROUTE_EXECUTE_TOOLS:
                return current
            current = _merge_state(current, _execute_tools_with_limit(current, self.tool_node))


def build_autonomous_factory(
    architect_model: Any,
    developer_model: Any,
    auditor_model: Any,
    *,
    max_iterations: int = MAX_ITERATIONS,
    deploy_node: Callable[[FactoryState], Mapping[str, Any]] = deploy_and_sync_node,
    checkpointer: Any | None = None,
) -> Any:
    """Construye el flujo completo y selecciona LangGraph o el fallback local."""

    try:
        from langgraph.graph import END, StateGraph
    except ImportError:
        return LocalAutonomousFactory(
            architect_model,
            developer_model,
            auditor_model,
            max_iterations=max_iterations,
            deploy_node=deploy_node,
        )

    builder = StateGraph(FactoryState)
    builder.add_node("architect", lambda state: architect_node(state, architect_model))
    builder.add_node("developer", lambda state: developer_node(state, developer_model))
    builder.add_node("auditor", lambda state: auditor_node(state, auditor_model))
    builder.add_node("consolidate_evidence", consolidate_developer_evidence)
    tool_node = build_tool_executor_node()
    audit_tool_node = build_tool_executor_node(AUDITOR_TOOLS)
    builder.add_node("execute_tools", lambda state: _execute_tools_with_limit(state, tool_node))
    builder.add_node(
        "audit_execute_tools",
        lambda state: _execute_tools_with_limit(state, audit_tool_node),
    )
    builder.add_node("deploy_and_sync", deploy_node)
    builder.set_entry_point("architect")
    builder.add_edge("architect", "developer")
    builder.add_conditional_edges(
        "developer",
        should_continue_router,
        {ROUTE_EXECUTE_TOOLS: "execute_tools", ROUTE_POST_PROCESS: "consolidate_evidence"},
    )
    builder.add_edge("execute_tools", "developer")
    builder.add_edge("consolidate_evidence", "auditor")

    def route_after_auditor(state: FactoryState) -> str:
        if auditor_should_continue_router(state) == ROUTE_AUDIT_EXECUTE_TOOLS:
            return ROUTE_AUDIT_EXECUTE_TOOLS
        return evaluate_workflow_router(state, max_iterations=max_iterations)

    builder.add_conditional_edges(
        "auditor",
        route_after_auditor,
        {
            ROUTE_AUDIT_EXECUTE_TOOLS: "audit_execute_tools",
            ROUTE_DEVELOPER: "developer",
            ROUTE_DEPLOY: "deploy_and_sync",
            ROUTE_STOP: END,
        },
    )
    builder.add_edge("audit_execute_tools", "auditor")
    builder.add_edge("deploy_and_sync", END)
    if checkpointer is None:
        return builder.compile()
    return builder.compile(checkpointer=checkpointer)
