"""Configuración de persistencia durable para la fábrica."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .state import FactoryState

try:
    from langgraph.checkpoint.sqlite import SqliteSaver
except ImportError:  # pragma: no cover - depende de las dependencias de ejecución
    SqliteSaver = None  # type: ignore[assignment,misc]


FACTORY_STATE_DB = Path("factory_state.db")


def resolve_database_path(db_path: str | Path = FACTORY_STATE_DB) -> Path:
    """Resuelve la base SQLite y crea solo su directorio padre."""

    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def build_thread_config(thread_id: str) -> dict[str, dict[str, str]]:
    """Construye la configuración que LangGraph usa para reanudar un hilo."""

    normalized = thread_id.strip()
    if not normalized:
        raise ValueError("thread_id debe contener texto")
    return {"configurable": {"thread_id": normalized}}


def open_checkpoint_saver(db_path: str | Path = FACTORY_STATE_DB) -> Any:
    """Abre un ``SqliteSaver`` para compilar un grafo con checkpoints."""

    if SqliteSaver is None:
        raise RuntimeError(
            "SqliteSaver no está disponible; instala langgraph-checkpoint-sqlite "
            "en el venv del proyecto"
        )
    database_path = resolve_database_path(db_path)
    return SqliteSaver.from_conn_string(str(database_path))


def build_persistence_config(
    thread_id: str,
    db_path: str | Path = FACTORY_STATE_DB,
) -> dict[str, Any]:
    """Devuelve la configuración explícita de una ejecución persistente."""

    database_path = resolve_database_path(db_path)
    return {
        "db_path": str(database_path),
        "config": build_thread_config(thread_id),
        "state_type": FactoryState,
    }
