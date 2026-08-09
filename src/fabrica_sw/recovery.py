"""Recuperación no destructiva de archivos modificados por la fábrica."""

from __future__ import annotations

import shutil
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


_workspace: Path | None = None
_recovery_directory: Path | None = None
_enabled = False


def configure_recovery(workspace: str | Path, enabled: bool = True) -> str:
    """Crea un punto de recuperación único para la ejecución."""

    global _workspace, _recovery_directory, _enabled

    _workspace = Path(workspace).expanduser().resolve()
    _enabled = enabled

    if not enabled:
        _recovery_directory = None
        return ""

    run_id = (
        datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        + "-"
        + uuid4().hex[:8]
    )
    _recovery_directory = _workspace / ".factory" / "recovery" / run_id
    _recovery_directory.mkdir(parents=True, exist_ok=True)
    return str(_recovery_directory)


def backup_before_write(target_path: str | Path) -> Path | None:
    """Guarda una sola copia del archivo antes de su primera modificación."""

    if not _enabled or _workspace is None or _recovery_directory is None:
        return None

    target = Path(target_path).expanduser().resolve()

    try:
        relative_path = target.relative_to(_workspace)
    except ValueError as exc:
        raise ValueError("No se puede respaldar un archivo externo") from exc

    if relative_path.parts and relative_path.parts[0] == ".factory":
        raise ValueError("El directorio interno .factory está protegido")

    if not target.is_file():
        return None

    backup_path = _recovery_directory / relative_path
    if backup_path.exists():
        return backup_path

    backup_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(target, backup_path)
    return backup_path


def get_recovery_directory() -> str:
    return str(_recovery_directory) if _recovery_directory else ""


__all__ = [
    "configure_recovery",
    "backup_before_write",
    "get_recovery_directory",
]
