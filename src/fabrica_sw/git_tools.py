"""Herramientas Git con selección explícita y autorización de auditoría."""

from __future__ import annotations

import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from .git_policy import ensure_commit_approved
from .safe_paths import WORKSPACE_DIR, validate_safe_path

GIT_TIMEOUT_SECONDS = 30
COMMIT_PREFIX = "[fabrica-sw] "


def _selected_relative_files(selected_files: Sequence[str]) -> list[str]:
    """Valida y convierte rutas seleccionadas a rutas relativas al workspace."""
    if isinstance(selected_files, (str, bytes)) or not selected_files:
        raise ValueError("selected_files debe ser una lista no vacía de archivos")

    relative_files: list[str] = []
    for selected_file in selected_files:
        if not isinstance(selected_file, str) or not selected_file.strip():
            raise ValueError("Cada archivo seleccionado debe ser una ruta no vacía")
        safe_file = validate_safe_path(selected_file)
        if not safe_file.is_file():
            raise ValueError(f"El archivo seleccionado no existe: {selected_file}")
        if safe_file in {WORKSPACE_DIR, *relative_files}:
            raise ValueError(f"Archivo seleccionado duplicado o inválido: {selected_file}")
        relative_files.append(safe_file.relative_to(WORKSPACE_DIR).as_posix())

    if len(set(relative_files)) != len(relative_files):
        raise ValueError("No se permiten archivos seleccionados duplicados")
    return relative_files


def git_secure_commit_tool(
    state: Mapping[str, Any],
    selected_files: Sequence[str],
    commit_message: str,
) -> str:
    """Crea un commit usando únicamente los archivos seleccionados explícitamente."""
    ensure_commit_approved(state)

    if not isinstance(commit_message, str) or not commit_message.strip():
        raise ValueError("commit_message debe ser un texto no vacío")

    relative_files = _selected_relative_files(selected_files)
    message = f"{COMMIT_PREFIX}{commit_message.strip()}"
    add_command = ["git", "add", "--", *relative_files]
    commit_command = ["git", "commit", "-m", message]

    try:
        add_result = subprocess.run(
            add_command,
            capture_output=True,
            text=True,
            timeout=GIT_TIMEOUT_SECONDS,
            cwd=str(WORKSPACE_DIR),
            shell=False,
            check=False,
        )
        if add_result.returncode != 0:
            detail = (add_result.stderr or add_result.stdout).strip()
            return f"Error preparando commit: {detail or 'git add falló'}"

        commit_result = subprocess.run(
            commit_command,
            capture_output=True,
            text=True,
            timeout=GIT_TIMEOUT_SECONDS,
            cwd=str(WORKSPACE_DIR),
            shell=False,
            check=False,
        )
        if commit_result.returncode != 0:
            detail = (commit_result.stderr or commit_result.stdout).strip()
            return f"Error creando commit: {detail or 'git commit falló'}"
        return f"Commit creado: {message}"
    except subprocess.TimeoutExpired:
        return "Error creando commit: Git excedió el tiempo máximo permitido"
    except OSError as exc:
        return f"Error ejecutando Git: {exc}"


__all__ = ["git_secure_commit_tool"]
