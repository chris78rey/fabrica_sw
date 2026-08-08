"""Políticas deterministas para el ciclo Desarrollador--Auditor."""

from __future__ import annotations

from typing import Any, Mapping

MAX_ITERATIONS = 4
ROUTE_DEVELOPER = "developer"
ROUTE_DEPLOY = "deploy_and_sync"
ROUTE_STOP = "stop_execution"


def evaluate_workflow_router(
    state: Mapping[str, Any], max_iterations: int = MAX_ITERATIONS
) -> str:
    """Decide corrección, despliegue o detención con un límite seguro."""
    if isinstance(max_iterations, bool) or not isinstance(max_iterations, int) or max_iterations <= 0:
        raise ValueError("max_iterations debe ser un entero positivo")

    iteration_count = state.get("iteration_count", 0)
    if isinstance(iteration_count, bool) or not isinstance(iteration_count, int):
        raise ValueError("iteration_count debe ser un entero")
    if iteration_count < 0:
        raise ValueError("iteration_count no puede ser negativo")

    if iteration_count >= max_iterations:
        return ROUTE_STOP
    if state.get("is_approved", False):
        return ROUTE_DEPLOY
    return ROUTE_DEVELOPER


def evaluate_workflow_route(
    state: Mapping[str, Any], max_iterations: int = MAX_ITERATIONS
) -> str:
    """Alias de compatibilidad para el nombre usado en la primera versión."""

    return evaluate_workflow_router(state, max_iterations)


__all__ = [
    "MAX_ITERATIONS",
    "ROUTE_DEVELOPER",
    "ROUTE_DEPLOY",
    "ROUTE_STOP",
    "evaluate_workflow_router",
    "evaluate_workflow_route",
]
