"""Rotas para o módulo de usuários."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session  # Importar Session de sqlmodel

from app.db import get_db
# Ajustar importações para os modelos/schemas SQLModel
from app.db.models.user import User, UserCreate, UserUpdate, UserRead
from app.services import user_service

router = APIRouter()


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
# Renomeado para evitar conflito
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    """Cria um novo usuário."""
    db_user = user_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já registrado"
        )
    return user_service.create_user(db=db, user=user)


@router.get("/", response_model=List[UserRead])
def read_users_route(  # Renomeado para evitar conflito
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Retorna uma lista de usuários."""
    users = user_service.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=UserRead)
# Renomeado para evitar conflito
def read_user_route(user_id: int, db: Session = Depends(get_db)):
    """Retorna um usuário específico pelo ID."""
    db_user = user_service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return db_user


@router.put("/{user_id}", response_model=UserRead)
def update_user_route(  # Renomeado para evitar conflito
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza um usuário."""
    updated_user = user_service.update_user(
        db=db, user_id=user_id, user_update=user)
    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado para atualização"
        )
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
# Renomeado para evitar conflito
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    """Remove um usuário."""
    deleted_user = user_service.delete_user(db=db, user_id=user_id)
    if deleted_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado para remoção"
        )
    return None  # HTTP 204 No Content
