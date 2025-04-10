"""Serviço para operações com itens."""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.db.models.item import Item
from app.schemas import item as item_schema


def get_item(db: Session, item_id: int) -> Optional[Item]:
    """Obtém um item pelo ID."""
    return db.query(Item).filter(Item.id == item_id).first()


def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[Item]:
    """Obtém uma lista de itens."""
    return db.query(Item).offset(skip).limit(limit).all()


def get_items_by_owner(db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> List[Item]:
    """Obtém uma lista de itens de um proprietário específico."""
    return (
        db.query(Item)
        .filter(Item.owner_id == owner_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_item(db: Session, item: item_schema.ItemCreate, owner_id: Optional[int] = None) -> Item:
    """Cria um novo item."""
    db_item = Item(
        title=item.title,
        description=item.description,
        price=item.price,
        owner_id=owner_id,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item_id: int, item: item_schema.ItemUpdate) -> Item:
    """Atualiza os dados de um item existente."""
    db_item = get_item(db, item_id)

    update_data = item.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_item, field, value)

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int) -> None:
    """Remove um item."""
    db_item = get_item(db, item_id)
    db.delete(db_item)
    db.commit()
