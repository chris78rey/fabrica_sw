"""Punto de entrada para ejecutar la fábrica sobre un repositorio local."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fabrica-sw",
        description="Ejecuta el flujo seguro Arquitecto -> Desarrollador -> Auditor.",
    )
    parser.add_argument("--repository", required=True, type=Path, help="Directorio del repositorio.")
    parser.add_argument("--requirement", help="Requerimiento de la fábrica.")
    parser.add_argument("--requirements-file", type=Path, help="Archivo UTF-8 con el requerimiento.")
    parser.add_argument("--max-iterations", type=int, default=4, help="Máximo de ciclos de corrección.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repository = args.repository.expanduser().resolve()
    if not repository.is_dir():
        raise SystemExit(f"El repositorio no existe o no es un directorio: {repository}")
    if args.max_iterations <= 0:
        raise SystemExit("--max-iterations debe ser mayor que cero.")
    if bool(args.requirement) == bool(args.requirements_file):
        raise SystemExit("Debe indicar exactamente uno de --requirement o --requirements-file.")

    if args.requirements_file is not None:
        requirements_file = args.requirements_file.expanduser().resolve()
        try:
            requirement = requirements_file.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            raise SystemExit(f"No se pudo leer --requirements-file: {exc}") from exc
    else:
        requirement = args.requirement

    from .model_factory import ModelFactoryError
    from .runner import FactoryRunRequest, run_factory

    try:
        result = run_factory(
            FactoryRunRequest(repository=repository, requirement=requirement, max_iterations=args.max_iterations)
        )
    except (ModelFactoryError, ValueError, OSError) as exc:
        raise SystemExit(f"Ejecución no iniciada: {exc}") from exc

    print(json.dumps(result.report, ensure_ascii=False, indent=2))
    return 0 if result.report["approved"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
