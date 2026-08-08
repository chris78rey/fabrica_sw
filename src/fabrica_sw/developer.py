"""Nodo de desarrollo y despacho seguro de llamadas a herramientas."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from typing import Any

from .safe_factory_tools import SAFE_DEVELOPMENT_TOOLS
from .state import FactoryState

DEVELOPER_SYSTEM_PROMPT = (
    "Eres el Desarrollador de la fábrica autónoma. Implementa el requerimiento "
    "usando únicamente las herramientas seguras disponibles. Lee antes de escribir, "
    "ejecuta las pruebas y documenta decisiones con comentarios # WHY:. No hagas commits."
)
ROUTE_EXECUTE_TOOLS = "execute_tools"
ROUTE_POST_PROCESS = "post_process"
MAX_TOOL_ROUNDS = 8


def _message_content(message: Any) -> str:
    content = getattr(message, "content", message)
    return content if isinstance(content, str) else str(content)


def developer_node(state: FactoryState, model: Any | None = None) -> dict[str, Any]:
    """Solicita al modelo la implementación y avanza una iteración.

    El nodo no modifica archivos por sí mismo: las escrituras solo ocurren cuando
    el modelo emite una llamada a ``write_file_tool`` que pasa por el despachador.
    """

    requirement = state.get("user_requirement", "")
    if not isinstance(requirement, str) or not requirement.strip():
        raise ValueError("user_requirement debe ser un texto no vacío")

    blueprint = state.get("architecture_blueprint", {})
    history = list(state.get("messages", []))
    if history:
        messages = [{"role": "system", "content": DEVELOPER_SYSTEM_PROMPT}, *history]
        has_tool_result = any(
            (item.get("role") if isinstance(item, Mapping) else getattr(item, "type", None)) == "tool"
            for item in history
        )
        if not has_tool_result:
            messages.append(
                {
                    "role": "user",
                    "content": f"Requerimiento: {requirement}\n\nArquitectura aprobada:\n{blueprint}",
                }
            )
    else:
        messages = [
            {"role": "system", "content": DEVELOPER_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Requerimiento: {requirement}\n\nArquitectura aprobada:\n{blueprint}",
            },
        ]

    if model is None:
        response: Any = {
            "role": "assistant",
            "content": "Desarrollo preparado. Se requieren llamadas de herramientas para modificar archivos.",
        }
    else:
        invoker = model.bind_tools(SAFE_DEVELOPMENT_TOOLS) if hasattr(model, "bind_tools") else model
        response = invoker.invoke(messages)

    current_iteration = state.get("iteration_count", 0)
    if not isinstance(current_iteration, int) or isinstance(current_iteration, bool) or current_iteration < 0:
        raise ValueError("iteration_count debe ser un entero no negativo")
    return {"messages": [response], "iteration_count": current_iteration + 1}


def _call_data(call: Any) -> tuple[str, Mapping[str, Any], str | None]:
    if isinstance(call, Mapping):
        name = call.get("name")
        args = call.get("args", {})
        call_id = call.get("id")
    else:
        name = getattr(call, "name", None)
        args = getattr(call, "args", {})
        call_id = getattr(call, "id", None)
    if not isinstance(name, str) or not isinstance(args, Mapping):
        raise ValueError("tool_call debe incluir name y args como mapa")
    return name, args, call_id if isinstance(call_id, str) else None


class LocalToolNode:
    """Fallback compatible con ``langgraph.prebuilt.ToolNode`` para este venv."""

    def __init__(self, tools: Sequence[Callable[..., Any]]) -> None:
        self.tools = {tool.__name__: tool for tool in tools}

    def invoke(self, state: FactoryState) -> dict[str, Any]:
        messages = state.get("messages", [])
        if not messages:
            return {"messages": []}
        latest = messages[-1]
        calls = latest.get("tool_calls", []) if isinstance(latest, Mapping) else getattr(latest, "tool_calls", [])
        results: list[dict[str, Any]] = []
        for call in calls:
            name = "unknown"
            call_id: str | None = None
            try:
                name, args, call_id = _call_data(call)
                tool = self.tools.get(name)
                if tool is None:
                    raise ValueError(f"Herramienta no permitida: {name}")
                content = str(tool(**dict(args)))
            except (TypeError, ValueError) as exc:
                content = f"ERROR: {exc}"
            result = {"role": "tool", "content": content, "name": name}
            if call_id:
                result["tool_call_id"] = call_id
            results.append(result)
        return {"messages": results}

    __call__ = invoke


def build_tool_executor_node(tools: Sequence[Callable[..., Any]] = SAFE_DEVELOPMENT_TOOLS) -> Any:
    """Usa ToolNode real si existe; de lo contrario, el fallback local seguro."""

    try:
        from langgraph.prebuilt import ToolNode
    except ImportError:
        return LocalToolNode(tools)
    return ToolNode(tools)


tool_executor_node = build_tool_executor_node()


def should_continue_router(state: FactoryState) -> str:
    """Envía llamadas de herramientas al ejecutor o termina la fase de desarrollo."""

    messages = state.get("messages", [])
    if not messages:
        return ROUTE_POST_PROCESS
    latest = messages[-1]
    calls = latest.get("tool_calls", []) if isinstance(latest, Mapping) else getattr(latest, "tool_calls", [])
    return ROUTE_EXECUTE_TOOLS if calls else ROUTE_POST_PROCESS

__all__ = [
    "DEVELOPER_SYSTEM_PROMPT",
    "ROUTE_EXECUTE_TOOLS",
    "ROUTE_POST_PROCESS",
    "MAX_TOOL_ROUNDS",
    "LocalToolNode",
    "build_tool_executor_node",
    "developer_node",
    "should_continue_router",
    "tool_executor_node",
]
