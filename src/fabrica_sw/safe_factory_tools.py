"""Herramientas de archivos restringidas al workspace de la fábrica."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from .safe_paths import validate_safe_path

WORKSPACE_COMMAND_DIR = validate_safe_path(".")
GRAPH_PATH = WORKSPACE_COMMAND_DIR / "graphify-out" / "graph.json"
GRAPHIFY_COMMAND = str(Path(sys.executable).with_name("graphify.exe"))
ALLOWED_COMMANDS = {
    "pytest", "python", "python3", "ruff", "black", "flake8", "mypy",
    "npm", "jest", "cargo", "go", "git", "graphify",
}


def _is_safe_command(command_args: list[str]) -> bool:
    """Permite perfiles de verificación, no intérpretes ni operaciones mutantes."""
    base_cmd, arguments = command_args[0], command_args[1:]
    if base_cmd in {"python", "python3"}:
        return len(arguments) >= 2 and arguments[:2] in (["-m", "unittest"], ["-m", "pytest"])
    if base_cmd == "npm":
        return arguments in (["test"], ["run", "test"])
    if base_cmd in {"pytest", "jest"}:
        return True
    if base_cmd in {"ruff", "black", "flake8", "mypy"}:
        return True
    if base_cmd == "git":
        return bool(arguments) and arguments[0] in {"status", "diff", "log", "show", "rev-parse"}
    if base_cmd == "cargo":
        return bool(arguments) and arguments[0] in {"test", "check"}
    if base_cmd == "go":
        return bool(arguments) and arguments[0] == "test"
    return False


def read_file_tool(file_path: str) -> str:
    """Lee un archivo de texto UTF-8 dentro del workspace seguro."""
    try:
        safe_path = validate_safe_path(file_path)
        if not safe_path.exists():
            return f"Error: El archivo '{file_path}' no existe."
        if not safe_path.is_file():
            return f"Error: La ruta '{file_path}' no es un archivo válido."
        return safe_path.read_text(encoding="utf-8")
    except Exception as exc:
        return f"Error leyendo el archivo: {exc}"


def write_file_tool(file_path: str, content: str) -> str:
    """Escribe texto UTF-8 y crea directorios padres dentro del workspace."""
    try:
        safe_path = validate_safe_path(file_path)
        safe_path.parent.mkdir(parents=True, exist_ok=True)
        safe_path.write_text(content, encoding="utf-8")
        return f"Éxito: Archivo escrito correctamente en '{file_path}'."
    except Exception as exc:
        return f"Error escribiendo el archivo: {exc}"


def list_directory_tool(dir_path: str = ".") -> str:
    """Lista, ordenados, los archivos y carpetas de un directorio seguro."""
    try:
        safe_path = validate_safe_path(dir_path)
        if not safe_path.exists():
            return f"Error: El directorio '{dir_path}' no existe."
        if not safe_path.is_dir():
            return f"Error: La ruta '{dir_path}' no es un directorio."

        result = []
        for item in sorted(os.listdir(safe_path)):
            item_path = safe_path / item
            prefix = "[DIR]" if item_path.is_dir() else "[FILE]"
            result.append(f"{prefix} {item}")
        return "\n".join(result) if result else "Directorio vacío."
    except Exception as exc:
        return f"Error listando el directorio: {exc}"


def execute_test_command(command_args: list[str]) -> str:
    """Ejecuta un comando permitido sin shell y con timeout de 30 segundos."""
    if not isinstance(command_args, list) or not command_args:
        return "Error: No se proporcionaron argumentos de comando."
    if not all(isinstance(argument, str) and argument for argument in command_args):
        return "Error: Los argumentos del comando deben ser textos no vacíos."

    base_cmd = command_args[0]
    if base_cmd not in ALLOWED_COMMANDS:
        return (
            f"Acceso Denegado: El comando '{base_cmd}' no está en la lista de "
            "comandos permitidos para ejecución segura."
        )
    if not _is_safe_command(command_args):
        return (
            "Acceso Denegado: el perfil de ejecución no permite este comando o sus "
            "argumentos. Use una operación de prueba o inspección explícita."
        )

    try:
        result = subprocess.run(
            command_args,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(WORKSPACE_COMMAND_DIR),
            shell=False,
            check=False,
        )
        output = []
        if result.stdout:
            output.append(f"--- STDOUT ---\n{result.stdout}")
        if result.stderr:
            output.append(f"--- STDERR ---\n{result.stderr}")
        output.append(f"Comando finalizado con código de salida {result.returncode}.")
        return "\n\n".join(output)
    except subprocess.TimeoutExpired:
        return f"Error: Tiempo de espera agotado (30s) al ejecutar '{' '.join(command_args)}'."
    except Exception as exc:
        return f"Error de ejecución: {exc}"


def graphify_query_tool(question: str) -> str:
    """Consulta el grafo de conocimiento de Graphify sin cargar el código completo."""
    if not isinstance(question, str) or not question.strip():
        return "Error: La pregunta de Graphify debe ser un texto no vacío."
    if not GRAPH_PATH.exists():
        return (
            "Error: No se encuentra graphify-out/graph.json. "
            "Asegúrese de ejecutar primero 'graphify .' en el repositorio."
        )

    try:
        result = subprocess.run(
            [GRAPHIFY_COMMAND, "query", question, "--graph", str(GRAPH_PATH)],
            capture_output=True,
            text=True,
            timeout=15,
            cwd=str(WORKSPACE_COMMAND_DIR),
            shell=False,
            check=False,
        )
        if result.returncode != 0:
            return f"Error en la consulta de Graphify: {result.stderr or result.stdout}"
        return result.stdout
    except subprocess.TimeoutExpired:
        return "Error: Tiempo de espera agotado (15s) al ejecutar graphify query."
    except Exception as exc:
        return f"Error al ejecutar graphify query: {exc}"


def graphify_shortest_path_tool(source_symbol: str, target_symbol: str) -> str:
    """Encuentra el camino más corto de dependencias entre dos símbolos."""
    if not isinstance(source_symbol, str) or not source_symbol.strip():
        return "Error: source_symbol debe ser un texto no vacío."
    if not isinstance(target_symbol, str) or not target_symbol.strip():
        return "Error: target_symbol debe ser un texto no vacío."
    if not GRAPH_PATH.exists():
        return "Error: No se encuentra graphify-out/graph.json."

    try:
        result = subprocess.run(
            [
                GRAPHIFY_COMMAND,
                "path",
                source_symbol,
                target_symbol,
                "--graph",
                str(GRAPH_PATH),
            ],
            capture_output=True,
            text=True,
            timeout=15,
            cwd=str(WORKSPACE_COMMAND_DIR),
            shell=False,
            check=False,
        )
        if result.returncode != 0:
            return f"Error en la consulta de dependencias: {result.stderr or result.stdout}"
        return result.stdout
    except subprocess.TimeoutExpired:
        return "Error: Tiempo de espera agotado (15s) al ejecutar graphify path."
    except Exception as exc:
        return f"Error al ejecutar graphify path: {exc}"


SAFE_DEVELOPMENT_TOOLS = [
    read_file_tool,
    write_file_tool,
    list_directory_tool,
    execute_test_command,
    graphify_query_tool,
    graphify_shortest_path_tool,
]


__all__ = [
    "read_file_tool",
    "write_file_tool",
    "list_directory_tool",
    "execute_test_command",
    "graphify_query_tool",
    "graphify_shortest_path_tool",
    "SAFE_DEVELOPMENT_TOOLS",
]
