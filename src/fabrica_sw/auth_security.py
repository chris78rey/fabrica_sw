"""Controles reutilizables para credenciales."""

from __future__ import annotations

import hashlib
import os


def hash_password_secure(password: str) -> str:
    """Genera un hash PBKDF2 con una sal aleatoria por contraseña."""
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
    return (salt + digest).hex()


def validate_password_complexity(password: str) -> bool:
    """Valida longitud mínima, una mayúscula y un dígito."""
    return (
        len(password) >= 8
        and any(char.isdigit() for char in password)
        and any(char.isupper() for char in password)
    )
