"""Construcción de modelos de chat para la fábrica segura.

La integración es perezosa: el paquete base puede importarse y probarse sin
instalar LangChain ni realizar llamadas de red. Las credenciales se leen del
entorno y nunca se incluyen en excepciones propias del módulo.
"""

from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Any, Literal, Mapping


SUPPORTED_PROVIDERS = ("openai", "openrouter")
ModelRole = Literal["architect", "developer", "auditor"]


class ModelFactoryError(RuntimeError):
    """Error controlado al configurar o construir el modelo."""


class ModelConfigurationError(ModelFactoryError, ValueError):
    """Configuración incompleta o inválida del proveedor."""


@dataclass(frozen=True)
class ModelConfig:
    """Configuración normalizada para un modelo compatible con OpenAI."""

    provider: str
    model: str
    api_key: str
    base_url: str | None = None
    temperature: float = 0.0
    max_tokens: int | None = None
    reasoning_effort: str | None = None
    request_timeout: float = 60.0
    max_retries: int = 0


def _environment(env: Mapping[str, str] | None) -> Mapping[str, str]:
    return os.environ if env is None else env


def _parse_float(value: str, name: str) -> float:
    try:
        parsed = float(value)
    except ValueError as exc:
        raise ModelConfigurationError(f"{name} debe ser un número.") from exc
    if not 0 <= parsed <= 2:
        raise ModelConfigurationError(f"{name} debe estar entre 0 y 2.")
    return parsed


def _parse_positive_int(value: str, name: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ModelConfigurationError(f"{name} debe ser un entero positivo.") from exc
    if parsed <= 0:
        raise ModelConfigurationError(f"{name} debe ser un entero positivo.")
    return parsed


def _parse_positive_float(value: str, name: str) -> float:
    try:
        parsed = float(value)
    except ValueError as exc:
        raise ModelConfigurationError(f"{name} debe ser un nÃºmero positivo.") from exc
    if parsed <= 0:
        raise ModelConfigurationError(f"{name} debe ser un nÃºmero positivo.")
    return parsed


def load_model_config(
    env: Mapping[str, str] | None = None,
    *,
    role: ModelRole | None = None,
) -> ModelConfig:
    if role is not None and role not in ("architect", "developer", "auditor"):
        raise ModelConfigurationError(
            "role debe ser architect, developer o auditor."
        )
    """Lee y valida la configuración del modelo desde variables de entorno."""

    if env is None:
        try:
            from dotenv import load_dotenv
        except ImportError:
            pass
        else:
            load_dotenv()
    values = _environment(env)
    role_prefix = f"FACTORY_{role.upper()}_" if role else ""
    provider = values.get(
        f"{role_prefix}PROVIDER" if role else "FACTORY_MODEL_PROVIDER",
        values.get("FACTORY_MODEL_PROVIDER", "openai"),
    ).strip().lower()
    provider = provider.replace("_", "-")
    if provider == "open-router":
        provider = "openrouter"
    if provider not in SUPPORTED_PROVIDERS:
        supported = ", ".join(SUPPORTED_PROVIDERS)
        raise ModelConfigurationError(
            f"Proveedor no soportado: {provider!r}. Use uno de: {supported}."
        )

    model = values.get(
        f"{role_prefix}MODEL" if role else "FACTORY_MODEL_NAME",
        values.get("FACTORY_MODEL_NAME", "gpt-4o-mini"),
    ).strip()
    if not model:
        raise ModelConfigurationError("FACTORY_MODEL_NAME no puede estar vacío.")

    key_name = "OPENROUTER_API_KEY" if provider == "openrouter" else "OPENAI_API_KEY"
    api_key = values.get(key_name, "").strip()
    if not api_key:
        raise ModelConfigurationError(f"Falta la credencial {key_name}.")

    if provider == "openrouter":
        base_url = values.get(
            "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"
        ).strip()
    else:
        base_url = values.get("OPENAI_BASE_URL", "").strip() or None

    temperature = _parse_float(
        values.get("FACTORY_TEMPERATURE", "0"), "FACTORY_TEMPERATURE"
    )
    max_tokens_value = values.get("FACTORY_MAX_TOKENS", "").strip()
    max_tokens = (
        _parse_positive_int(max_tokens_value, "FACTORY_MAX_TOKENS")
        if max_tokens_value
        else None
    )
    reasoning_effort = values.get("FACTORY_REASONING_EFFORT", "none").strip() or None
    request_timeout = _parse_positive_float(
        values.get("FACTORY_REQUEST_TIMEOUT_SECONDS", "60"),
        "FACTORY_REQUEST_TIMEOUT_SECONDS",
    )
    max_retries = _parse_positive_int(
        values.get("FACTORY_MAX_RETRIES", "0") or "0", "FACTORY_MAX_RETRIES"
    ) if values.get("FACTORY_MAX_RETRIES", "0") != "0" else 0

    return ModelConfig(
        provider=provider,
        model=model,
        api_key=api_key,
        base_url=base_url,
        temperature=temperature,
        max_tokens=max_tokens,
        reasoning_effort=reasoning_effort,
        request_timeout=request_timeout,
        max_retries=max_retries,
    )


def _load_chat_openai() -> Any:
    try:
        from langchain_openai import ChatOpenAI
    except ImportError as exc:
        raise ModelFactoryError(
            "Falta langchain-openai. Instálelo con "
            "'.\\.venv\\Scripts\\python.exe -m pip install -e \".[runtime]\"'."
        ) from exc
    return ChatOpenAI


def create_model(
    config: ModelConfig | None = None,
    *,
    env: Mapping[str, str] | None = None,
) -> Any:
    """Construye un ChatOpenAI para OpenAI u OpenRouter.

    OpenRouter expone una API compatible con OpenAI, por lo que ambos
    proveedores usan el mismo adaptador de LangChain y solo cambia el endpoint.
    """

    selected = config or load_model_config(env)
    chat_openai = _load_chat_openai()
    kwargs: dict[str, Any] = {
        "model": selected.model,
        "api_key": selected.api_key,
        "temperature": selected.temperature,
        "timeout": selected.request_timeout,
        "max_retries": selected.max_retries,
    }
    if selected.base_url:
        kwargs["base_url"] = selected.base_url
    if selected.max_tokens is not None:
        kwargs["max_tokens"] = selected.max_tokens
    if selected.reasoning_effort is not None:
        kwargs["reasoning_effort"] = selected.reasoning_effort
    return chat_openai(**kwargs)


def create_models(*, env: Mapping[str, str] | None = None) -> dict[str, Any]:
    """Construye un modelo independiente para cada rol de la fábrica."""
    return {
        role: create_model(load_model_config(env, role=role), env=env)
        for role in ("architect", "developer", "auditor")
    }


__all__ = [
    "ModelConfig",
    "ModelConfigurationError",
    "ModelFactoryError",
    "ModelRole",
    "SUPPORTED_PROVIDERS",
    "create_model",
    "create_models",
    "load_model_config",
]
