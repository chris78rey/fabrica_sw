"""Políticas de autorización para operaciones Git de la fábrica."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


def ensure_commit_approved(state: Mapping[str, Any]) -> None:
    """Permite continuar solo con una aprobación booleana explícita.

    La operación Git concreta se implementará después; esta compuerta debe ser
    llamada por cualquier herramienta de commit antes de seleccionar cambios.
    """

    if not isinstance(state, Mapping):
        raise TypeError("state debe ser un mapa")
    if state.get("is_approved") is not True:
        raise PermissionError("Commit bloqueado: la auditoría no ha aprobado el estado")


__all__ = ["ensure_commit_approved"]
