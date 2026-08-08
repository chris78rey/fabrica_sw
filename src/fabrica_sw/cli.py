"""Punto de entrada para ejecutar la fábrica sobre un repositorio local."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Sequence


def _configure_loaded_workspace(repository: Path) -> None:
    """Sincroniza las constantes importadas antes de procesar ``--repository``."""

    from . import auditor, git_tools, github_safe_pusher, safe_factory_tools, safe_paths, workflow

    safe_paths.WORKSPACE_DIR = repository
    safe_factory_tools.WORKSPACE_COMMAND_DIR = repository
    safe_factory_tools.GRAPH_PATH = repository / "graphify-out" / "graph.json"
    git_tools.WORKSPACE_DIR = repository
    github_safe_pusher.WORKSPACE_DIR = repository
    auditor.WORKSPACE_DIR = repository
    workflow.WORKSPACE_COMMAND_DIR = repository


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fabrica-sw",
        description="Ejecuta el flujo seguro Arquitecto -> Desarrollador -> Auditor.",
    )
    parser.add_argument(
        "--repository",
        required=True,
        type=Path,
        help="Directorio del repositorio que funcionará como workspace seguro.",
    )
    parser.add_argument(
        "--requirement",
        required=True,
        help="Requerimiento que debe analizar e implementar la fábrica.",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=4,
        help="Máximo de ciclos Desarrollador-Auditor (por defecto: 4).",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repository = args.repository.expanduser().resolve()
    if not repository.is_dir():
        raise SystemExit(f"El repositorio no existe o no es un directorio: {repository}")
    if args.max_iterations <= 0:
        raise SystemExit("--max-iterations debe ser mayor que cero.")

    # Debe establecerse antes de importar las herramientas que calculan
    # WORKSPACE_DIR al importar el módulo.
    os.environ["FABRICA_WORKSPACE_DIR"] = str(repository)
    _configure_loaded_workspace(repository)

    from .model_factory import ModelFactoryError, create_models
    from .state import create_initial_state
    from .developer import MAX_TOOL_ROUNDS
    from .workflow import build_autonomous_factory

    try:
        models = create_models()
        factory = build_autonomous_factory(
            models["architect"],
            models["developer"],
            models["auditor"],
            max_iterations=args.max_iterations,
        )
        # Un flujo con herramientas puede superar 25 nodos aunque estÃ© acotado.
        recursion_limit = max(100, 5 + args.max_iterations * (2 * MAX_TOOL_ROUNDS + 8))
        final_state = factory.invoke(
            create_initial_state(args.requirement),
            config={"recursion_limit": recursion_limit},
        )
    except (ModelFactoryError, ValueError) as exc:
        raise SystemExit(f"Ejecución no iniciada: {exc}") from exc

    print(
        json.dumps(
            {
                "repository": str(repository),
                "approved": final_state.get("is_approved", False),
                "completion_percentage": final_state.get("completion_percentage", 0.0),
                "iteration_count": final_state.get("iteration_count", 0),
                "audit_report": final_state.get("audit_report", ""),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if final_state.get("is_approved", False) else 1


if __name__ == "__main__":
    raise SystemExit(main())
