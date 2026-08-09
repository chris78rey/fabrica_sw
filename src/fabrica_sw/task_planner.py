"""Conversión pequeña y determinista de requisitos en tareas trazables."""

from __future__ import annotations

import re
from functools import lru_cache
from typing import Any


@lru_cache(maxsize=128)
def _build_tasks_cached(requirement: str) -> tuple[tuple[str, str, bool], ...]:
    """Cachea planes deterministas para requisitos repetidos."""

    tasks: list[dict[str, Any]] = []
    for line in requirement.splitlines():
        match = re.match(r"^\s*-\s*\[([ xX])\]\s+(.+?)\s*$", line)
        if match:
            tasks.append({"id": f"TASK-{len(tasks) + 1:03d}", "title": match.group(2), "completed": match.group(1).lower() == "x"})
            continue
        match = re.match(r"^\s*(\d+)[.)]\s+(.+?)\s*$", line)
        if match:
            tasks.append({"id": f"TASK-{len(tasks) + 1:03d}", "title": match.group(2), "completed": False})
    if not tasks:
        title = " ".join(requirement.split()) or "Implementar y validar el requerimiento"
        tasks.append({"id": "TASK-001", "title": title, "completed": False})
    return tuple((task["id"], task["title"], task["completed"]) for task in tasks)


def build_tasks(requirement: str) -> list[dict[str, Any]]:
    """Extrae checklists o pasos numerados; si no existen, crea una tarea."""

    return [{"id": task_id, "title": title, "completed": completed} for task_id, title, completed in _build_tasks_cached(requirement)]
