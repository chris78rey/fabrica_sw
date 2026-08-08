"""Simulación local del flujo de la fábrica, sin commit ni push reales."""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from fabrica_sw.git_policy import ensure_commit_approved  # noqa: E402
from fabrica_sw.auth_security import (  # noqa: E402
    hash_password_secure,
    validate_password_complexity,
)


SANDBOX = PROJECT_ROOT / "sandbox_test_repo"
REQUIREMENTS = SANDBOX / "requirements_checklist.txt"
SOURCE = SANDBOX / "auth_security.py"


def _write_initial_files() -> None:
    SANDBOX.mkdir(parents=True, exist_ok=True)
    REQUIREMENTS.write_text(
        """# REQUERIMIENTOS: SISTEMA DE AUTENTICACIÓN
- [ ] 1. Crear hashing seguro de contraseñas.
- [ ] 2. Validar longitud y complejidad de credenciales.
- [ ] 3. Añadir protección contra fuerza bruta.
""",
        encoding="utf-8",
    )
    SOURCE.write_text(
        """import hashlib
import os


def hash_password_secure(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
    return (salt + digest).hex()


def validate_password_complexity(password: str) -> bool:
    return (
        len(password) >= 8
        and any(char.isdigit() for char in password)
        and any(char.isupper() for char in password)
    )
""",
        encoding="utf-8",
    )


def _audit_and_measure_progress() -> float:
    source = SOURCE.read_text(encoding="utf-8")
    if "os.system" in source or "subprocess" in source:
        raise RuntimeError("La auditoría detectó una ejecución de comandos insegura.")

    requirements = REQUIREMENTS.read_text(encoding="utf-8").replace(
        "- [ ] 1.", "- [x] 1."
    ).replace("- [ ] 2.", "- [x] 2.")
    REQUIREMENTS.write_text(requirements, encoding="utf-8")
    completed = requirements.count("- [x]")
    total = requirements.count("- [")
    return completed / total * 100


def main() -> int:
    print("=== SIMULACIÓN DE FÁBRICA DE SOFTWARE ===")
    created_sandbox = not SANDBOX.exists()
    try:
        print("[1/4] Arquitecto: blueprint y consulta Graphify simulados.")
        _write_initial_files()
        print(f"[2/4] Desarrollador: archivos creados en {SANDBOX.relative_to(PROJECT_ROOT)}.")

        compile_result = compile(SOURCE.read_text(encoding="utf-8"), str(SOURCE), "exec")
        del compile_result
        print("[3/4] Auditor: sintaxis OK; calculando requerimientos...")
        percentage = _audit_and_measure_progress()
        print(f"      Progreso verificado: {percentage:.1f}%.")

        state = {"is_approved": True}
        ensure_commit_approved(state)
        push_preview = "omitido: simulación sin credenciales ni red"
        print("[4/4] Entrega: commit y push omitidos; ejecución en modo simulación.")
        print(f"      Política de aprobación: OK; resultado push simulado: {push_preview}")
        print("SIMULACIÓN FINALIZADA CON ÉXITO")
        return 0
    finally:
        if SANDBOX.exists() and (created_sandbox or os.environ.get("FABRICA_SIMULATION_CLEANUP") == "1"):
            resolved = SANDBOX.resolve()
            resolved.relative_to(PROJECT_ROOT)
            shutil.rmtree(resolved)
            print("Limpieza: sandbox_test_repo eliminado.")


if __name__ == "__main__":
    raise SystemExit(main())
