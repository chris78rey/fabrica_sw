"""Nodo de auditoría segura para validar el trabajo del desarrollador."""

from __future__ import annotations

import json
import re
from typing import Any, Mapping

from .safe_factory_tools import (
    execute_test_command,
    graphify_query_tool,
    graphify_shortest_path_tool,
    read_file_tool,
)
from .safe_paths import WORKSPACE_DIR
from .state import FactoryState

AUDITOR_SYSTEM_PROMPT = (
    "Eres el Auditor de Software de la fábrica autónoma. Inspecciona los archivos "
    "impactados usando herramientas seguras, revisa los resultados de pruebas y "
    "comprueba las decisiones arquitectónicas con Graphify. No escribas archivos, "
    "no ejecutes commits y responde únicamente con JSON: "
    '{"is_approved": true|false, "audit_report": "..."}. '
    "Aprueba solo si la evidencia es suficiente y no hay fallos críticos."
)
AUDITOR_TOOLS = [
    read_file_tool,
    execute_test_command,
    graphify_query_tool,
    graphify_shortest_path_tool,
]
ROUTE_AUDIT_EXECUTE_TOOLS = "audit_execute_tools"
ROUTE_AUDIT_DECISION = "audit_decision"


def _response_content(response: Any) -> str:
    content = getattr(response, "content", response)
    return content if isinstance(content, str) else str(content)


def _extract_audit_decision(content: str) -> tuple[bool, str]:
    """Extrae una decisión sin aprobar por accidente una respuesta ambigua."""

    candidates = re.findall(r"\{.*?\}", content, flags=re.DOTALL)
    for candidate in candidates:
        try:
            data = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(data, Mapping) and isinstance(data.get("is_approved"), bool):
            report = data.get("audit_report", content)
            return data["is_approved"], report if isinstance(report, str) else str(report)

    match = re.search(r"['\"]?is_approved['\"]?\s*:\s*(true|false)", content, re.I)
    approved = bool(match and match.group(1).lower() == "true")
    return approved, content


def _calculate_completion_percentage(content: str) -> float:
    checklist = re.findall(r"^\s*-\s*\[([ xX])\]", content, flags=re.MULTILINE)
    if not checklist:
        return 0.0
    completed = sum(marker.lower() == "x" for marker in checklist)
    return round(completed * 100 / len(checklist), 2)


def _read_checklist() -> str:
    """Lee el checklist conocido sin salir del workspace seguro."""

    for relative_path in ("requirements_checklist.txt", "docs/PLAN_IMPLEMENTACION.md"):
        path = (WORKSPACE_DIR / relative_path).resolve()
        try:
            path.relative_to(WORKSPACE_DIR)
        except ValueError:
            continue
        if path.is_file():
            return path.read_text(encoding="utf-8")
    return ""


def auditor_node(state: FactoryState, model: Any | None = None) -> dict[str, Any]:
    """Audita el estado actual y devuelve aprobación, informe y avance."""

    requirement = state.get("user_requirement", "")
    if not isinstance(requirement, str) or not requirement.strip():
        raise ValueError("user_requirement debe ser un texto no vacío")

    blueprint = state.get("architecture_blueprint", {})
    test_results = state.get("test_results", "")
    source_code_draft = state.get("source_code_draft", {})
    messages: list[Any] = [
        {"role": "system", "content": AUDITOR_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"Requerimiento: {requirement}\n\n"
                f"Blueprint: {json.dumps(blueprint, ensure_ascii=False)}\n\n"
                f"Archivos en borrador: {json.dumps(list(source_code_draft), ensure_ascii=False)}\n\n"
                f"Resultados de pruebas:\n{test_results}\n\n"
                "Realiza una auditoría de solo lectura y devuelve el JSON solicitado."
            ),
        },
    ]

    history = list(state.get("messages", []))
    if history:
        audit_request = messages[-1]
        messages = [messages[0], *history]
        if not any(
            isinstance(item, Mapping)
            and item.get("role") == "user"
            and "devuelve el JSON solicitado." in str(item.get("content", ""))
            for item in history
        ):
            messages.append(audit_request)

    if model is None:
        approved = False
        report = "Auditoría pendiente: no se proporcionó un modelo auditor."
        response: Any = {"role": "assistant", "content": report}
    else:
        invoker = model.bind_tools(AUDITOR_TOOLS) if hasattr(model, "bind_tools") else model
        response = invoker.invoke(messages)
        approved, report = _extract_audit_decision(_response_content(response))

    return {
        "messages": [response],
        "is_approved": approved,
        "audit_report": report,
        "completion_percentage": _calculate_completion_percentage(_read_checklist()),
    }


def auditor_should_continue_router(state: FactoryState) -> str:
    """Envía las llamadas del Auditor al ejecutor antes de aplicar la política."""

    messages = state.get("messages", [])
    if not messages:
        return ROUTE_AUDIT_DECISION
    latest = messages[-1]
    calls = latest.get("tool_calls", []) if isinstance(latest, Mapping) else getattr(latest, "tool_calls", [])
    return ROUTE_AUDIT_EXECUTE_TOOLS if calls else ROUTE_AUDIT_DECISION


__all__ = [
    "AUDITOR_SYSTEM_PROMPT",
    "auditor_node",
    "_calculate_completion_percentage",
    "_extract_audit_decision",
    "AUDITOR_TOOLS",
    "ROUTE_AUDIT_EXECUTE_TOOLS",
    "ROUTE_AUDIT_DECISION",
    "auditor_should_continue_router",
]
