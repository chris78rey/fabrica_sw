"""Validación de rutas para herramientas que operan en el espacio de trabajo."""

from __future__ import annotations

import os
from pathlib import Path

WORKSPACE_DIR = Path(
    os.environ.get("FABRICA_WORKSPACE_DIR", Path.cwd())
).resolve()


def validate_safe_path(
    target_path: str | os.PathLike[str],
    workspace_dir: str | os.PathLike[str] | None = None,
) -> Path:
    """Resuelve una ruta y garantiza que quede dentro de ``WORKSPACE_DIR``.

    ``Path.resolve`` también sigue enlaces simbólicos existentes, evitando que
    un enlace dentro del proyecto permita acceder a un destino externo.
    """
    if isinstance(target_path, str) and not target_path.strip():
        raise ValueError("target_path debe contener texto")

    workspace = Path(workspace_dir).resolve() if workspace_dir is not None else WORKSPACE_DIR
    candidate = Path(target_path)
    resolved_path = candidate.resolve()
    try:
        resolved_path.relative_to(workspace)
    except ValueError as exc:
        raise ValueError(
            f"La ruta '{target_path}' está fuera del directorio de trabajo seguro "
            f"'{workspace}'."
        ) from exc
    return resolved_path
