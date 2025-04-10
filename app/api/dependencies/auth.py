"""Dependências para autenticação e autorização."""

from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import verify_password
from app.db import get_db
from app.services import user_service

# Esquema de token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


class TokenData(BaseModel):
    """Dados extraídos do token JWT."""
    email: str


def authenticate_user(db: Session, email: str, password: str):
    """Autentica um usuário verificando email e senha."""
    user = user_service.get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """Obtém o usuário atual a partir do token JWT."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    user = user_service.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception

    return user


def get_current_active_user(current_user=Depends(get_current_user)):
    """Verifica se o usuário atual está ativo."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Usuário inativo")
    return current_user
