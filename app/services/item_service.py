"""Serviço para operações com itens usando SQLModel."""

from typing import List, Optional
from sqlmodel import Session, select  # Importar Session e select de sqlmodel

# Ajustar importações para os modelos/schemas SQLModel
from app.db.models.item import Item, ItemCreate, ItemUpdate


def get_item(db: Session, item_id: int) -> Optional[Item]:
    """Obtém um item pelo ID."""
    return db.get(Item, item_id)


def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[Item]:
    """Obtém uma lista de itens."""
    statement = select(Item).offset(skip).limit(limit)
    return db.exec(statement).all()


def get_items_by_owner(db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> List[Item]:
    """Obtém uma lista de itens de um proprietário específico."""
    statement = select(Item).where(
        Item.owner_id == owner_id).offset(skip).limit(limit)
    return db.exec(statement).all()


def create_item(db: Session, item: ItemCreate, owner_id: Optional[int] = None) -> Item:
    """Cria um novo item."""
    # Criar instância do modelo SQLModel diretamente
    # O owner_id será atribuído separadamente se fornecido
    db_item = Item.model_validate(item)
    if owner_id is not None:
        db_item.owner_id = owner_id

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item_id: int, item_update: ItemUpdate) -> Optional[Item]:
    """Atualiza os dados de um item existente."""
    db_item = db.get(Item, item_id)
    if not db_item:
        return None

    item_data = item_update.model_dump(exclude_unset=True)
    for key, value in item_data.items():
        setattr(db_item, key, value)

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int) -> Optional[Item]:
    """Remove um item."""
    db_item = db.get(Item, item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
        return db_item
    return None
