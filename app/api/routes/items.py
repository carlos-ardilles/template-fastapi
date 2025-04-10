"""Rotas para o módulo de itens."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import item as item_schema
from app.services import item_service

router = APIRouter()


@router.post("/", response_model=item_schema.Item, status_code=status.HTTP_201_CREATED)
def create_item(
    item: item_schema.ItemCreate,
    db: Session = Depends(get_db)
):
    """Cria um novo item."""
    return item_service.create_item(db=db, item=item)


@router.get("/", response_model=List[item_schema.Item])
def read_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Retorna uma lista de itens."""
    items = item_service.get_items(db, skip=skip, limit=limit)
    return items


@router.get("/{item_id}", response_model=item_schema.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    """Retorna um item específico pelo ID."""
    db_item = item_service.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item não encontrado"
        )
    return db_item


@router.put("/{item_id}", response_model=item_schema.Item)
def update_item(
    item_id: int,
    item: item_schema.ItemUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza um item."""
    db_item = item_service.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item não encontrado"
        )
    return item_service.update_item(db=db, item_id=item_id, item=item)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Remove um item."""
    db_item = item_service.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item não encontrado"
        )
    item_service.delete_item(db=db, item_id=item_id)
    return None
