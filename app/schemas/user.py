"""Esquemas Pydantic para usuários."""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Esquema base para usuários."""
    email: EmailStr
    name: str
    is_active: bool = True


class UserCreate(UserBase):
    """Esquema para criação de usuários."""
    password: str


class UserUpdate(BaseModel):
    """Esquema para atualização de usuários."""
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


class User(UserBase):
    """Esquema para retorno de usuários."""
    id: int

    class Config:
        """Configuração para o esquema."""
        from_attributes = True
