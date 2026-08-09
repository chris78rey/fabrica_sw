"""Detección conservadora de comandos de verificación por tipo de proyecto."""

from __future__ import annotations

import os
import shutil
from pathlib import Path


def detect_test_command(workspace_dir: Path) -> list[str] | None:
    """Devuelve un comando seguro y portable para el proyecto detectado.

    La detección solo inspecciona archivos de marcadores; no ejecuta nada.
    """
    root = Path(workspace_dir)
    if (root / "package.json").is_file():
        return ["npm", "test"]
    if (root / "go.mod").is_file():
        return ["go", "test", "./..."]
    if (root / "Cargo.toml").is_file():
        return ["cargo", "test"]
    if (root / "pom.xml").is_file():
        return ["mvn", "test", "-q"]
    if (root / "build.gradle").is_file() or (root / "build.gradle.kts").is_file():
        return ["gradle", "test"]
    if (root / "project.godot").is_file():
        return ["godot", "--headless", "--path", ".", "--editor", "--quit"]
    if (root / "pytest.ini").is_file() or (root / "tox.ini").is_file():
        return ["python", "-m", "pytest", "-q"]
    pyproject = root / "pyproject.toml"
    if pyproject.is_file() and "[tool.pytest" in pyproject.read_text(encoding="utf-8"):
        return ["python", "-m", "pytest", "-q"]
    if (root / "tests").is_dir():
        return ["python", "-m", "unittest", "discover", "-s", "tests", "-q"]
    return None


def resolve_test_executable(command: list[str], workspace_dir: Path) -> str | None:
    """Resuelve ejecutables, permitiendo configurar Godot fuera del PATH."""

    if not command:
        return None
    if command[0].lower() == "godot":
        configured = os.environ.get("GODOT_BIN", "").strip().strip('"')
        if configured and Path(configured).is_file():
            return configured
    return shutil.which(command[0], path=os.environ.get("PATH"))


__all__ = ["detect_test_command", "resolve_test_executable"]
