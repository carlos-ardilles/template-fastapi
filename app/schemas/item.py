"""Esquemas Pydantic para itens."""

from typing import Optional
from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    """Esquema base para itens."""
    title: str
    description: Optional[str] = None
    price: float = Field(..., ge=0.0)


class ItemCreate(ItemBase):
    """Esquema para criação de itens."""
    pass


class ItemUpdate(BaseModel):
    """Esquema para atualização de itens."""
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0.0)


class Item(ItemBase):
    """Esquema para retorno de itens."""
    id: int
    owner_id: Optional[int] = None

    class Config:
        """Configuração para o esquema."""
        from_attributes = True
