"""Serviço para operações com usuários."""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db.models.user import User
from app.schemas import user as user_schema


def get_user(db: Session, user_id: int) -> Optional[User]:
    """Obtém um usuário pelo ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Obtém um usuário pelo email."""
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Obtém uma lista de usuários."""
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: user_schema.UserCreate) -> User:
    """Cria um novo usuário."""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        name=user.name,
        hashed_password=hashed_password,
        is_active=user.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: user_schema.UserUpdate) -> User:
    """Atualiza os dados de um usuário existente."""
    db_user = get_user(db, user_id)

    update_data = user.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(
            update_data.pop("password"))

    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> None:
    """Remove um usuário."""
    db_user = get_user(db, user_id)
    db.delete(db_user)
    db.commit()
