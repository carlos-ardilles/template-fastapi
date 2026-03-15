"""Modelo de banco de dados e schema para usuários usando SQLModel."""

from typing import List, Optional, TYPE_CHECKING
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

# Use TYPE_CHECKING para imports que são apenas para tipagem
if TYPE_CHECKING:
    from .item import Item


class UserBase(SQLModel):
    """Schema base para usuários."""
    email: EmailStr = Field(unique=True, index=True)
    name: str
    is_active: bool = True


class User(UserBase, table=True):
    """Modelo de usuário no banco de dados."""
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

    # Relacionamentos - use string para forward reference
    items: List["Item"] = Relationship(back_populates="owner")


class UserCreate(UserBase):
    """Schema para criação de usuários."""
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(SQLModel):
    """Schema para atualização de usuários."""
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(default=None, min_length=8, max_length=128)


class UserRead(UserBase):
    """Schema para leitura de usuários, incluindo o ID."""
    id: int
