"""Detección conservadora de comandos de verificación por tipo de proyecto."""

from __future__ import annotations

import os
import shutil
import re
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


def validate_static_web_project(workspace_dir: Path) -> tuple[str, int] | None:
    """Valida un proyecto HTML/JavaScript sin requerir un runner externo."""

    root = Path(workspace_dir)
    html_path = root / "index.html"
    if not html_path.is_file():
        return None

    try:
        html = html_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return f"VALIDATION_STATIC_ERROR: no se pudo leer index.html: {exc}", 1

    errors: list[str] = []
    lowered = html.lower()
    if not html.strip():
        errors.append("index.html está vacío")
    if "<html" not in lowered or "</html>" not in lowered:
        errors.append("index.html no contiene una estructura HTML completa")

    referenced_scripts = re.findall(r"<script[^>]+src=[\"']([^\"']+)[\"']", html, re.I)
    javascript_paths = {path for path in root.rglob("*.js") if path.is_file()}
    for reference in referenced_scripts:
        if reference.startswith(("http://", "https://", "//")):
            continue
        script_path = (html_path.parent / reference.split("?", 1)[0]).resolve()
        try:
            script_path.relative_to(root.resolve())
        except ValueError:
            errors.append(f"script fuera del workspace: {reference}")
            continue
        if not script_path.is_file():
            errors.append(f"script referenciado inexistente: {reference}")

    for script_path in javascript_paths:
        try:
            source = script_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"no se pudo leer {script_path.relative_to(root)}: {exc}")
            continue
        if not source.strip():
            errors.append(f"{script_path.relative_to(root)} está vacío")
        if any(source.count(opening) != source.count(closing) for opening, closing in (("(", ")"), ("{", "}"), ("[", "]"))):
            errors.append(f"posible desequilibrio de delimitadores en {script_path.relative_to(root)}")

    if errors:
        return "VALIDATION_STATIC_FAILED: " + "; ".join(errors), 1
    return "VALIDATION_STATIC_PASSED: HTML/JavaScript autocontenido válido.", 0


__all__ = ["detect_test_command", "resolve_test_executable", "validate_static_web_project"]
