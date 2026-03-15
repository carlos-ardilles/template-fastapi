"""Testes para as rotas de items."""

import uuid

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.db.models.item import Item
from app.db.models.user import User
from app.services.item_service import create_item
from app.services.user_service import create_user


@pytest.fixture
def test_item(db_session: Session, test_user: User) -> Item:
    """Cria um item de teste."""
    from app.db.models.item import ItemCreate

    item_data = ItemCreate(
        title="Item de Teste",
        description="Descrição do item de teste",
        price=99.99
    )

    item = create_item(db_session, item_data, test_user.id)
    db_session.commit()
    db_session.refresh(item)
    return item


def test_create_item(client: TestClient, auth_headers: dict[str, str]):
    """Testa a criação de um novo item."""
    item_data = {
        "title": "Novo Item",
        "description": "Descrição do novo item",
        "price": 29.99
    }

    response = client.post(
        f"{settings.API_V1_STR}/items/",
        json=item_data,
        headers=auth_headers
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == item_data["title"]
    assert data["description"] == item_data["description"]
    assert data["price"] == item_data["price"]
    assert "id" in data
    assert "owner_id" in data


def test_create_item_unauthorized(client: TestClient):
    """Testa a criação de item sem autenticação."""
    item_data = {
        "title": "Novo Item",
        "description": "Descrição do novo item",
        "price": 29.99
    }

    response = client.post(
        f"{settings.API_V1_STR}/items/",
        json=item_data
    )

    assert response.status_code == 401


def test_read_items(client: TestClient, test_item: Item, auth_headers: dict[str, str]):
    """Testa a listagem de items do usuário."""
    response = client.get(
        f"{settings.API_V1_STR}/items/",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    # Verifica se o item de teste está na lista
    item_ids = [item["id"] for item in data]
    assert test_item.id in item_ids


def test_read_item(client: TestClient, test_item: Item, auth_headers: dict[str, str]):
    """Testa a obtenção de um item específico."""
    response = client.get(
        f"{settings.API_V1_STR}/items/{test_item.id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_item.id
    assert data["title"] == test_item.title
    assert data["description"] == test_item.description
    assert data["price"] == test_item.price


def test_read_item_not_found(client: TestClient, auth_headers: dict[str, str]):
    """Testa a obtenção de um item inexistente."""
    response = client.get(
        f"{settings.API_V1_STR}/items/999999",
        headers=auth_headers
    )

    assert response.status_code == 404


def test_read_item_unauthorized(client: TestClient, test_item: Item):
    """Testa a obtenção de item sem autenticação."""
    response = client.get(f"{settings.API_V1_STR}/items/{test_item.id}")
    assert response.status_code == 401


def test_update_item(client: TestClient, test_item: Item, auth_headers: dict[str, str]):
    """Testa a atualização de um item."""
    update_data = {
        "title": "Item Atualizado",
        "description": "Nova descrição do item",
        "price": 199.99
    }

    response = client.put(
        f"{settings.API_V1_STR}/items/{test_item.id}",
        json=update_data,
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]
    assert data["price"] == update_data["price"]
    assert data["id"] == test_item.id


def test_update_item_not_found(client: TestClient, auth_headers: dict[str, str]):
    """Testa a atualização de um item inexistente."""
    update_data = {
        "title": "Item Atualizado",
        "description": "Nova descrição do item",
        "price": 199.99
    }

    response = client.put(
        f"{settings.API_V1_STR}/items/999999",
        json=update_data,
        headers=auth_headers
    )

    assert response.status_code == 404


def test_delete_item(client: TestClient, test_item: Item, auth_headers: dict[str, str]):
    """Testa a remoção de um item."""
    response = client.delete(
        f"{settings.API_V1_STR}/items/{test_item.id}",
        headers=auth_headers
    )

    assert response.status_code == 204

    # Verifica se o item foi realmente removido
    response = client.get(
        f"{settings.API_V1_STR}/items/{test_item.id}",
        headers=auth_headers
    )
    assert response.status_code == 404


def test_delete_item_not_found(client: TestClient, auth_headers: dict[str, str]):
    """Testa a remoção de um item inexistente."""
    response = client.delete(
        f"{settings.API_V1_STR}/items/999999",
        headers=auth_headers
    )

    assert response.status_code == 404


def test_different_user_cannot_access_item(
    client: TestClient,
    test_item: Item,
    db_session: Session
):
    """Testa que um usuário não pode acessar items de outro usuário."""
    # Cria outro usuário
    from app.db.models.user import UserCreate
    other_user_data = UserCreate(
        email=f"outro-{uuid.uuid4()}@example.com",
        password="senha123",
        name="Outro Usuário",
        is_active=True
    )

    other_user = create_user(db_session, other_user_data)
    db_session.commit()

    # Faz login com o outro usuário
    login_data = {
        "username": other_user.email,
        "password": "senha123"
    }

    response = client.post(
        f"{settings.API_V1_STR}/auth/token",
        data=login_data
    )
    assert response.status_code == 200
    token_data = response.json()
    other_headers = {"Authorization": f"Bearer {token_data['access_token']}"}

    # Tenta acessar o item do primeiro usuário
    response = client.get(
        f"{settings.API_V1_STR}/items/{test_item.id}",
        headers=other_headers
    )

    assert response.status_code == 404  # Não encontrado para este usuário
