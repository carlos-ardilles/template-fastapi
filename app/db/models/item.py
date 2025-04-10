"""Modelo de banco de dados para itens."""

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class Item(Base):
    """Modelo de item no banco de dados."""
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relacionamentos
    owner = relationship("User", back_populates="items")
