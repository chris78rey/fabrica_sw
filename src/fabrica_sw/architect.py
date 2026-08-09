"""Nodo de arquitectura con consulta previa al grafo de Graphify."""

from __future__ import annotations

import json
import re
from typing import Any, Mapping

from .safe_factory_tools import graphify_query_tool, graphify_shortest_path_tool, read_file_tool
from .state import FactoryState

ARCHITECT_TOOLS = [read_file_tool, graphify_query_tool, graphify_shortest_path_tool]
ARCHITECT_SYSTEM_PROMPT = (
    "Eres el Arquitecto de Software de la fábrica autónoma. Analiza el requerimiento "
    "y el contexto de Graphify. Responde únicamente con un JSON con summary, "
    "impacted_files, dependencies y rules. Si Graphify no está disponible, continúa "
    "en modo bootstrap inspeccionando directamente los archivos. No escribas archivos "
    "ni hagas commits."
)


def _response_content(response: Any) -> str:
    content = getattr(response, "content", response)
    if isinstance(content, str):
        return content
    return str(content)


def _extract_json_object(content: str) -> dict[str, Any] | None:
    """Extrae un objeto JSON aunque el modelo lo envuelva en markdown."""
    candidates = [content.strip()]
    if "```" in content:
        candidates.append(content.replace("```json", "").replace("```", "").strip())
    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed
    return None


def _as_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item.strip() for item in value if isinstance(item, str) and item.strip()]


def _infer_impacted_files(content: str, requirement: str) -> list[str]:
    """Recupera rutas explícitas si el modelo omite el campo estructurado."""

    parsed = _extract_json_object(content) or {}
    declared = _as_string_list(parsed.get("impacted_files"))
    if declared:
        return declared
    candidates = re.findall(r"(?<![\w.-])(?:[\w.-]+/)*[\w.-]+\.(?:py|md|txt|json|toml|js|ts|go|rs|java)", requirement)
    return list(dict.fromkeys(candidates))


def _build_blueprint(content: str, graph_context: str, requirement: str = "") -> dict[str, Any]:
    parsed = _extract_json_object(content) or {}
    return {
        "status": "planned",
        "summary": str(parsed.get("summary", content)).strip(),
        "impacted_files": _infer_impacted_files(content, requirement),
        "dependencies": _as_string_list(parsed.get("dependencies")),
        "rules": _as_string_list(parsed.get("rules")),
        "graph_context": graph_context,
        "last_architect_thought": content,
    }


def architect_node(state: FactoryState, model: Any | None = None) -> dict[str, Any]:
    """Consulta Graphify y produce un blueprint arquitectónico estructurado."""
    requirement = state.get("user_requirement", "")
    if not isinstance(requirement, str) or not requirement.strip():
        raise ValueError("user_requirement debe ser un texto no vacío")

    existing_blueprint = state.get("architecture_blueprint")
    if (
        isinstance(existing_blueprint, Mapping)
        and existing_blueprint.get("status") == "planned"
        and existing_blueprint.get("summary")
    ):
        return {"architecture_blueprint": dict(existing_blueprint), "messages": []}

    graph_context = graphify_query_tool(
        f"Analiza archivos y dependencias impactados por este requerimiento: {requirement}"
    )
    messages: list[Any] = [
        {"role": "system", "content": ARCHITECT_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"Requerimiento: {requirement}\n\nContexto Graphify:\n{graph_context}",
        },
    ]

    response: Any | None = None
    if model is not None:
        invoker = model.bind_tools(ARCHITECT_TOOLS) if hasattr(model, "bind_tools") else model
        response = invoker.invoke(messages)
        architect_thought = _response_content(response)
    else:
        architect_thought = (
            "Arquitectura preliminar generada con consulta Graphify. "
            f"Contexto obtenido:\n{graph_context}"
        )

    blueprint = _build_blueprint(architect_thought, graph_context, requirement)
    blueprint["rules"] = [
        *blueprint["rules"],
        "Consultar Graphify antes de modificar archivos.",
        "No escribir archivos ni confirmar cambios desde el Arquitecto.",
    ]
    return {
        "architecture_blueprint": blueprint,
        "messages": [response] if response is not None else messages,
    }


__all__ = ["ARCHITECT_TOOLS", "ARCHITECT_SYSTEM_PROMPT", "architect_node"]
