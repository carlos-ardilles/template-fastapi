"""Rotas para o módulo de itens."""

from typing import List, Optional  # Optional pode ser necessário para owner_id
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session  # Importar Session de sqlmodel

from app.db import get_db
# Ajustar importações para os modelos/schemas SQLModel
from app.db.models.item import Item, ItemCreate, ItemUpdate, ItemRead
# Para obter o usuário atual e associar itens a ele (exemplo)
# Renomeado para evitar conflito se User for usado como modelo de resposta
from app.db.models.user import UserRead as User
from app.api.dependencies.auth import get_current_active_user

from app.services import item_service

router = APIRouter()


@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item_route(  # Renomeado para evitar conflito
    item: ItemCreate,
    db: Session = Depends(get_db),
    # Exemplo: associar item ao usuário logado
    current_user: User = Depends(get_current_active_user)
):
    """Cria um novo item."""
    return item_service.create_item(db=db, item=item, owner_id=current_user.id)


@router.get("/", response_model=List[ItemRead])
def read_items_route(  # Renomeado para evitar conflito
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Retorna uma lista de itens do usuário autenticado."""
    items = item_service.get_items_by_owner(
        db, owner_id=current_user.id, skip=skip, limit=limit)
    return items


@router.get("/mine", response_model=List[ItemRead])
def read_my_items(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100
):
    """Retorna uma lista de itens pertencentes ao usuário logado."""
    items = item_service.get_items_by_owner(
        db, owner_id=current_user.id, skip=skip, limit=limit)
    return items


@router.get("/{item_id}", response_model=ItemRead)
# Renomeado para evitar conflito
def read_item_route(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Retorna um item específico pelo ID se pertencer ao usuário."""
    db_item = item_service.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item não encontrado"
        )

    # Verificar se o usuário logado é o proprietário do item
    if db_item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item não encontrado"
        )

    return db_item


@router.put("/{item_id}", response_model=ItemRead)
def update_item_route(  # Renomeado para evitar conflito
    item_id: int,
    item: ItemUpdate,
    db: Session = Depends(get_db),
    # Para verificar permissão
    current_user: User = Depends(get_current_active_user)
):
    """Atualiza um item."""
    db_item = item_service.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item não encontrado para atualização"
        )
    # Opcional: Verificar se o usuário logado é o proprietário do item
    if db_item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não tem permissão para atualizar este item"
        )
    updated_item = item_service.update_item(
        db=db, item_id=item_id, item_update=item)
    return updated_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item_route(  # Renomeado para evitar conflito
    item_id: int,
    db: Session = Depends(get_db),
    # Para verificar permissão
    current_user: User = Depends(get_current_active_user)
):
    """Remove um item."""
    db_item = item_service.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item não encontrado para remoção"
        )
    # Opcional: Verificar se o usuário logado é o proprietário do item
    if db_item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não tem permissão para remover este item"
        )

    deleted_item = item_service.delete_item(db=db, item_id=item_id)
    # Não é necessário verificar deleted_item aqui pois o get_item já fez isso.
    # Se chegou aqui, o item existia e foi (ou tentou ser) deletado.
    return None  # HTTP 204 No Content
