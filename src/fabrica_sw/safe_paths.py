"""Validación de rutas para herramientas que operan en el workspace."""

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
    """Garantiza que la ruta permanezca dentro del repositorio seleccionado."""

    if isinstance(target_path, str) and not target_path.strip():
        raise ValueError("target_path debe contener texto")

    workspace = (
        Path(workspace_dir).expanduser().resolve()
        if workspace_dir is not None
        else WORKSPACE_DIR.resolve()
    )

    candidate = Path(target_path).expanduser()

    # Las rutas relativas parten del repositorio seleccionado, no de la fábrica.
    if not candidate.is_absolute():
        candidate = workspace / candidate

    resolved_path = candidate.resolve()

    try:
        resolved_path.relative_to(workspace)
    except ValueError as exc:
        raise ValueError(
            f"La ruta '{target_path}' está fuera del directorio del workspace seguro "
            f"'{workspace}'."
        ) from exc

    return resolved_path
