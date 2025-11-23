"""Modelo de banco de dados e schema para itens usando SQLModel."""

from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

# Use TYPE_CHECKING para imports que são apenas para tipagem
if TYPE_CHECKING:
    from .user import User


class ItemBase(SQLModel):
    """Schema base para itens."""
    title: str
    description: Optional[str] = None
    price: float = Field(default=0.0, ge=0.0)


class Item(ItemBase, table=True):
    """Modelo de item no banco de dados."""
    __tablename__ = "items"

    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: Optional[int] = Field(
        default=None, foreign_key="users.id", nullable=True)

    # Relacionamentos - use string para forward reference
    owner: Optional["User"] = Relationship(back_populates="items")


class ItemCreate(ItemBase):
    """Schema para criação de itens."""
    pass


class ItemUpdate(SQLModel):
    """Schema para atualização de itens."""
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(default=None, ge=0.0)


class ItemRead(ItemBase):
    """Schema para leitura de itens, incluindo IDs."""
    id: int
    owner_id: Optional[int] = None
