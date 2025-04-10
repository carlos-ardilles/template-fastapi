"""Modelo de banco de dados para usuários."""

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class User(Base):
    """Modelo de usuário no banco de dados."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    # Relacionamentos
    items = relationship("Item", back_populates="owner")
