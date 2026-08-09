"""Ejecución reutilizable de la fábrica para CLI e interfaces locales."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .autonomy import AutonomyConfig
from .dependency_tools import configure_dependency_installer, get_last_dependency_result
from .developer import MAX_TOOL_ROUNDS
from .git_tools import git_secure_commit_tool
from .model_factory import ModelFactoryError, create_models
from .recovery import configure_recovery, get_recovery_directory
from .state import create_initial_state
from .task_planner import build_tasks
from .workflow import build_autonomous_factory


@dataclass(frozen=True)
class FactoryRunRequest:
    repository: Path
    requirement: str
    max_iterations: int = 4


@dataclass
class FactoryRunResult:
    report: dict[str, Any]
    state: dict[str, Any]


def configure_loaded_workspace(repository: Path) -> None:
    """Actualiza módulos que conservan el workspace durante la importación."""

    from . import auditor, git_tools, github_safe_pusher, safe_factory_tools, safe_paths, workflow

    safe_paths.WORKSPACE_DIR = repository
    safe_factory_tools.WORKSPACE_COMMAND_DIR = repository
    safe_factory_tools.GRAPH_PATH = repository / "graphify-out" / "graph.json"
    git_tools.WORKSPACE_DIR = repository
    github_safe_pusher.WORKSPACE_DIR = repository
    auditor.WORKSPACE_DIR = repository
    workflow.WORKSPACE_COMMAND_DIR = repository


def _build_report(repository: Path, requirement: str, state: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "PASSED" if state.get("is_approved", False) else "BLOCKED",
        "repository": str(repository),
        "approved": state.get("is_approved", False),
        "validation_available": state.get("validation_available", False),
        "validation_passed": state.get("validation_passed", False),
        "validation_exit_code": state.get("validation_exit_code"),
        "changed_files": state.get("changed_files", []),
        "completion_percentage": state.get("completion_percentage", 0.0),
        "iteration_count": state.get("iteration_count", 0),
        "audit_report": state.get("audit_report", ""),
        "autonomy_mode": state.get("autonomy_mode", "safe"),
        "dependency_install_result": state.get("dependency_install_result", ""),
        "recovery_directory": state.get("recovery_directory", ""),
        "auto_commit_result": state.get("auto_commit_result", ""),
        "tasks": build_tasks(requirement),
    }


def run_factory(request: FactoryRunRequest) -> FactoryRunResult:
    """Ejecuta la fábrica y guarda RUN_REPORT.json en el repositorio."""

    repository = request.repository.expanduser().resolve()
    if not repository.is_dir():
        raise ValueError(f"El repositorio no existe o no es un directorio: {repository}")
    if request.max_iterations <= 0:
        raise ValueError("max_iterations debe ser mayor que cero.")
    if not request.requirement or not request.requirement.strip():
        raise ValueError("El requerimiento no puede estar vacío.")

    os.environ["FABRICA_WORKSPACE_DIR"] = str(repository)
    configure_loaded_workspace(repository)
    autonomy = AutonomyConfig.from_env()
    configure_dependency_installer(repository, autonomy)
    configure_recovery(
        repository,
        enabled=autonomy.create_recovery and autonomy.mode in {"balanced", "full"},
    )

    try:
        models = create_models()
        factory = build_autonomous_factory(
            models["architect"],
            models["developer"],
            models["auditor"],
            max_iterations=request.max_iterations,
        )
        recursion_limit = max(100, 5 + request.max_iterations * (2 * MAX_TOOL_ROUNDS + 8))
        final_state = factory.invoke(
            create_initial_state(request.requirement),
            config={"recursion_limit": recursion_limit},
        )
        final_state["autonomy_mode"] = autonomy.mode
        final_state["dependency_install_result"] = get_last_dependency_result()
        final_state["recovery_directory"] = get_recovery_directory()
        final_state["auto_commit_result"] = ""

        if autonomy.auto_commit and final_state.get("is_approved", False):
            selected_files = []
            for relative_path in final_state.get("changed_files", []):
                if relative_path.startswith(".factory/"):
                    continue
                candidate = repository / relative_path
                if candidate.is_file():
                    selected_files.append(relative_path)
            if selected_files:
                final_state["auto_commit_result"] = git_secure_commit_tool(
                    final_state,
                    selected_files,
                    "Entrega autónoma validada",
                )
    except (ModelFactoryError, ValueError):
        raise

    report = _build_report(repository, request.requirement, final_state)
    try:
        (repository / "RUN_REPORT.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    except OSError as exc:
        raise OSError(f"No se pudo guardar RUN_REPORT.json: {exc}") from exc
    return FactoryRunResult(report=report, state=final_state)
