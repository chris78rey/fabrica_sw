"""Configuración de autonomía con límites explícitos y seguros."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal

AutonomyMode = Literal["safe", "balanced", "full"]


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on", "si", "sí"}


@dataclass(frozen=True)
class AutonomyConfig:
    """Límites de una ejecución de la fábrica.

    La instalación solo puede ocurrir dentro del workspace y requiere una
    habilitación explícita, incluso en los modos de mayor autonomía.
    """

    mode: AutonomyMode = "safe"
    allow_dependency_install: bool = False
    install_scope: str = "project"
    max_installs: int = 10
    global_timeout_seconds: int = 1200
    auto_repair: bool = True
    auto_commit: bool = False
    auto_push: bool = False
    allow_file_delete: bool = False
    allow_destructive_sql: bool = False
    create_recovery: bool = True

    @classmethod
    def safe(cls) -> "AutonomyConfig":
        return cls()

    @classmethod
    def from_env(
        cls,
        mode_override: AutonomyMode | None = None,
        allow_dependency_install: bool | None = None,
    ) -> "AutonomyConfig":
        raw_mode = mode_override or os.getenv("FACTORY_AUTONOMY_MODE", "safe").strip().lower()
        mode: AutonomyMode = raw_mode if raw_mode in {"safe", "balanced", "full"} else "safe"  # type: ignore[assignment]
        allow = (
            allow_dependency_install
            if allow_dependency_install is not None
            else _env_bool("FACTORY_ALLOW_DEPENDENCY_INSTALL", False)
        )
        scope = os.getenv("FACTORY_INSTALL_SCOPE", "project").strip().lower()
        if scope != "project":
            scope = "blocked"
        return cls(
            mode=mode,
            allow_dependency_install=allow and mode != "safe" and scope == "project",
            install_scope=scope,
            max_installs=max(1, int(os.getenv("FACTORY_MAX_INSTALLS", "10"))),
            global_timeout_seconds=max(30, int(os.getenv("FACTORY_GLOBAL_TIMEOUT_SECONDS", "1200"))),
            auto_repair=_env_bool("FACTORY_AUTO_REPAIR", True),
            auto_commit=_env_bool("FACTORY_AUTO_COMMIT", False),
            auto_push=_env_bool("FACTORY_AUTO_PUSH", False),
            create_recovery=_env_bool("FACTORY_CREATE_RECOVERY", True),
        )
