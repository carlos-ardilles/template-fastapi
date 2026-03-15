"""Rotas para o módulo de usuários."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.api.dependencies.auth import get_current_active_user
from app.db import get_db
from app.db.models.user import User, UserCreate, UserUpdate, UserRead
from app.services import user_service

router = APIRouter()


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    """Cria um novo usuário."""
    db_user = user_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já registrado",
        )
    return user_service.create_user(db=db, user=user)


@router.get("/me", response_model=UserRead)
def read_me_route(current_user: User = Depends(get_current_active_user)):
    """Retorna os dados do usuário autenticado."""
    return current_user


@router.get("/", response_model=List[UserRead])
def read_users_route(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Retorna apenas o usuário autenticado para evitar enumeração indevida."""
    _ = (skip, limit, db)
    return [current_user]


@router.get("/{user_id}", response_model=UserRead)
def read_user_route(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
):
    """Retorna um usuário específico pelo ID, apenas para o próprio usuário."""
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para acessar este usuário",
        )
    return current_user


@router.put("/{user_id}", response_model=UserRead)
def update_user_route(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Atualiza o próprio usuário."""
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para atualizar este usuário",
        )

    updated_user = user_service.update_user(db=db, user_id=user_id, user_update=user)
    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado para atualização",
        )
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_route(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Remove o próprio usuário."""
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para remover este usuário",
        )

    deleted_user = user_service.delete_user(db=db, user_id=user_id)
    if deleted_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado para remoção",
        )
    return None
