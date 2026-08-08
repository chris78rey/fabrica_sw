"""Push seguro a GitHub después de una aprobación y un commit local."""

from __future__ import annotations

import os
import re
import subprocess
import tempfile
from collections.abc import Mapping
from typing import Any

from .git_policy import ensure_commit_approved
from .safe_paths import WORKSPACE_DIR

GIT_TIMEOUT_SECONDS = 30
DEFAULT_REMOTE = "origin"
TOKEN_ENVIRONMENT_VARIABLE = "GITHUB_TOKEN"
_SAFE_REF_PATTERN = re.compile(r"^[A-Za-z0-9._/-]+$")


def _validate_ref(value: str, field_name: str) -> str:
    if (
        not isinstance(value, str)
        or not value.strip()
        or value != value.strip()
        or value.startswith("-")
        or not _SAFE_REF_PATTERN.fullmatch(value)
        or ".." in value
    ):
        raise ValueError(f"{field_name} contiene un valor Git inválido")
    return value


def _mask_token(text: str, token: str) -> str:
    return text.replace(token, "********") if token else text


def _write_askpass_helper(directory: str) -> str:
    """Crea un helper efímero que devuelve el token únicamente desde el entorno."""
    if os.name == "nt":
        path = os.path.join(directory, "git-askpass.cmd")
        content = "@echo off\r\necho %GITHUB_TOKEN%\r\n"
    else:
        path = os.path.join(directory, "git-askpass.sh")
        content = '#!/bin/sh\nprintf "%s\\n" "$GITHUB_TOKEN"\n'
    with open(path, "w", encoding="utf-8", newline="") as helper:
        helper.write(content)
    if os.name != "nt":
        os.chmod(path, 0o700)
    return path


def github_secure_push_tool(
    state: Mapping[str, Any],
    branch: str,
    *,
    remote: str = DEFAULT_REMOTE,
) -> str:
    """Publica el commit actual en GitHub sin exponer el token en comandos o logs."""
    ensure_commit_approved(state)
    branch = _validate_ref(branch, "branch")
    remote = _validate_ref(remote, "remote")

    token = os.environ.get(TOKEN_ENVIRONMENT_VARIABLE, "")
    if not token:
        return f"Error haciendo push: falta {TOKEN_ENVIRONMENT_VARIABLE}"

    verify_command = ["git", "rev-parse", "--verify", "HEAD"]
    push_command = ["git", "push", remote, branch]
    try:
        with tempfile.TemporaryDirectory(prefix="fabrica-git-") as helper_dir:
            safe_environment = os.environ.copy()
            safe_environment[TOKEN_ENVIRONMENT_VARIABLE] = token
            safe_environment["GIT_ASKPASS"] = _write_askpass_helper(helper_dir)
            safe_environment["GIT_TERMINAL_PROMPT"] = "0"

            commit_result = subprocess.run(
                verify_command,
                capture_output=True,
                text=True,
                timeout=GIT_TIMEOUT_SECONDS,
                cwd=str(WORKSPACE_DIR),
                shell=False,
                check=False,
                env=safe_environment,
            )
            if commit_result.returncode != 0:
                detail = _mask_token(
                    (commit_result.stderr or commit_result.stdout).strip(), token
                )
                return f"Error verificando commit local: {detail or 'no existe HEAD'}"

            push_result = subprocess.run(
                push_command,
                capture_output=True,
                text=True,
                timeout=GIT_TIMEOUT_SECONDS,
                cwd=str(WORKSPACE_DIR),
                shell=False,
                check=False,
                env=safe_environment,
            )
            if push_result.returncode != 0:
                detail = _mask_token(
                    (push_result.stderr or push_result.stdout).strip(), token
                )
                return f"Error haciendo push: {detail or 'git push falló'}"

            detail = _mask_token(
                (push_result.stdout or push_result.stderr).strip(), token
            )
            return f"Push exitoso a {remote}/{branch}" + (f": {detail}" if detail else "")
    except subprocess.TimeoutExpired:
        return "Error haciendo push: Git excedió el tiempo máximo permitido"
    except OSError as exc:
        return f"Error ejecutando Git: {_mask_token(str(exc), token)}"


__all__ = ["github_secure_push_tool"]
