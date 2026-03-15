"""Utilitários de segurança para autenticação e senha."""

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt
from pwdlib import PasswordHash

from app.core.config import settings

pwd_hasher = PasswordHash.recommended()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha fornecida corresponde ao hash armazenado."""
    return pwd_hasher.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Gera hash robusto para senha."""
    return pwd_hasher.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Cria um token de acesso JWT."""
    to_encode = data.copy()
    now = datetime.now(timezone.utc)

    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "iat": now, "nbf": now})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
