"""Serviço para operações com usuários usando SQLModel."""

from typing import List, Optional
from sqlmodel import Session, select  # Importar Session e select de sqlmodel

from app.core.security import get_password_hash
# Ajustar importações para os modelos/schemas SQLModel
from app.db.models.user import User, UserCreate, UserUpdate


def get_user(db: Session, user_id: int) -> Optional[User]:
    """Obtém um usuário pelo ID."""
    # SQLModel usa session.get() para buscar por chave primária
    return db.get(User, user_id)


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Obtém um usuário pelo email."""
    # Usar session.exec(select(...)).first() ou one_or_none()
    statement = select(User).where(User.email == email)
    return db.exec(statement).one_or_none()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Obtém uma lista de usuários."""
    statement = select(User).offset(skip).limit(limit)
    return db.exec(statement).all()


def create_user(db: Session, user: UserCreate) -> User:
    """Cria um novo usuário."""
    hashed_password = get_password_hash(user.password)
    # Criar instância do modelo SQLModel diretamente
    db_user = User.model_validate(
        user, update={"hashed_password": hashed_password})
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """Atualiza os dados de um usuário existente."""
    db_user = db.get(User, user_id)
    if not db_user:
        return None

    user_data = user_update.model_dump(exclude_unset=True)

    if "password" in user_data and user_data["password"] is not None:
        hashed_password = get_password_hash(user_data.pop("password"))
        db_user.hashed_password = hashed_password

    for key, value in user_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> Optional[User]:
    """Remove um usuário."""
    db_user = db.get(User, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user
    return None
