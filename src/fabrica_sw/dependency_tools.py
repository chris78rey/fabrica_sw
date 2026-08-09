"""Instalación de dependencias estrictamente limitada al proyecto."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from .autonomy import AutonomyConfig
from .safe_paths import validate_safe_path

_workspace: Path | None = None
_config = AutonomyConfig.safe()
_install_count = 0
_last_result = ""
_successful_install_cache: dict[tuple[str, str, int, int], str] = {}


def configure_dependency_installer(workspace: str | Path, config: AutonomyConfig) -> None:
    global _workspace, _config, _install_count, _last_result, _successful_install_cache
    _workspace = validate_safe_path(workspace)
    _config = config
    _install_count = 0
    _last_result = ""
    _successful_install_cache = {}


def get_last_dependency_result() -> str:
    return _last_result


def _workspace_path() -> Path:
    return _workspace or validate_safe_path(".")


def _has_node_dependencies(path: Path) -> bool:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return True
    return bool(data.get("dependencies") or data.get("devDependencies") or data.get("optionalDependencies"))


def _detect_project_type(root: Path, requested: str) -> tuple[str, Path] | None:
    if requested:
        candidates = {
            "python": root / "requirements.txt",
            "node": root / "package.json",
            "go": root / "go.mod",
            "rust": root / "Cargo.toml",
        }
        manifest = candidates.get(requested.lower())
        return (requested.lower(), manifest) if manifest and manifest.is_file() else None
    for kind, filename in (
        ("node", "package.json"),
        ("python", "requirements.txt"),
        ("go", "go.mod"),
        ("rust", "Cargo.toml"),
    ):
        manifest = root / filename
        if manifest.is_file():
            if kind != "node" or _has_node_dependencies(manifest):
                return kind, manifest
    return None


def _run(command: list[str], root: Path) -> str:
    executable = shutil.which(command[0])
    if executable is None:
        return f"DEPENDENCY_INSTALL_BLOCKED: no se encontró '{command[0]}'."
    command[0] = executable
    try:
        completed = subprocess.run(
            command,
            cwd=root,
            shell=False,
            capture_output=True,
            text=True,
            timeout=_config.global_timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return "DEPENDENCY_INSTALL_FAILED: instalación agotó el tiempo máximo."
    output = (completed.stdout + "\n" + completed.stderr).strip()
    if completed.returncode != 0:
        return f"DEPENDENCY_INSTALL_FAILED: código {completed.returncode}.\n{output[-2000:]}"
    return f"DEPENDENCY_INSTALL_PASSED: {output[-2000:]}" if output else "DEPENDENCY_INSTALL_PASSED"


def install_project_dependencies_tool(project_type: str = "", reason: str = "") -> str:
    """Instala dependencias declaradas usando únicamente herramientas locales.

    No acepta comandos arbitrarios ni instala globalmente. El modelo solo
    selecciona el tipo de proyecto; la lista de comandos la controla este módulo.
    """
    global _install_count, _last_result
    root = _workspace_path()
    detected = _detect_project_type(root, project_type)
    if detected is None:
        _last_result = "DEPENDENCY_INSTALL_SKIPPED: no hay un manifiesto compatible con dependencias."
        return _last_result
    kind, manifest = detected
    manifest_stat = manifest.stat()
    cache_key = (kind, str(manifest.resolve()), manifest_stat.st_mtime_ns, manifest_stat.st_size)
    cached_result = _successful_install_cache.get(cache_key)
    if cached_result:
        _last_result = f"{cached_result}\nDEPENDENCY_INSTALL_CACHED: manifiesto sin cambios."
        return _last_result
    if not _config.allow_dependency_install or _config.install_scope != "project":
        _last_result = (
            "DEPENDENCY_INSTALL_BLOCKED: el modo actual no permite instalaciones; "
            "requiere FACTORY_AUTONOMY_MODE=balanced/full y "
            "FACTORY_ALLOW_DEPENDENCY_INSTALL=true."
        )
        return _last_result
    if _install_count >= _config.max_installs:
        _last_result = "DEPENDENCY_INSTALL_BLOCKED: se alcanzó FACTORY_MAX_INSTALLS."
        return _last_result

    _install_count += 1
    if kind == "node":
        command = ["npm", "ci" if (root / "package-lock.json").is_file() else "install", "--ignore-scripts", "--no-audit", "--no-fund"]
    elif kind == "go":
        command = ["go", "mod", "download"]
    elif kind == "rust":
        command = ["cargo", "fetch"]
    else:
        venv = root / ".venv"
        python = venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        if not python.is_file():
            created = _run([sys.executable, "-m", "venv", str(venv)], root)
            if not created.startswith("DEPENDENCY_INSTALL_PASSED"):
                _last_result = created
                return created
        command = [str(python), "-m", "pip", "install", "-r", str(manifest), "--disable-pip-version-check"]
    _last_result = _run(command, root)
    if _last_result.startswith("DEPENDENCY_INSTALL_PASSED:"):
        _successful_install_cache[cache_key] = _last_result
    return _last_result
