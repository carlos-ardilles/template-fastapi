"""Testes para as rotas de usuários."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db.models.user import User
from app.services import user_service


@pytest.fixture
def user_data():
    """Fornece dados de teste para usuário."""
    return {
        "email": "teste@example.com",
        "password": "senha123",
        "name": "Usuário de Teste",
        "is_active": True
    }


@pytest.fixture
def test_user(db: Session, user_data):
    """Cria um usuário de teste no banco de dados."""
    # Gera um e-mail único para evitar conflitos
    import uuid
    unique_email = f"teste-{uuid.uuid4()}@example.com"

    user = User(
        email=unique_email,
        name=user_data["name"],
        hashed_password=get_password_hash(user_data["password"]),
        is_active=user_data["is_active"]
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def test_create_user(client: TestClient, db: Session, user_data):
    """Testa a criação de um novo usuário."""
    # Usando um email diferente para evitar conflito com fixture
    user_data["email"] = "novo@example.com"

    response = client.post("/users/", json=user_data)
    assert response.status_code == 201

    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["name"] == user_data["name"]
    assert data["is_active"] == user_data["is_active"]
    assert "id" in data
    assert "password" not in data


def test_read_users(client: TestClient, test_user):
    """Testa a obtenção da lista de usuários."""
    response = client.get("/users/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(user["email"] == test_user.email for user in data)


def test_read_user(client: TestClient, test_user):
    """Testa a obtenção de um usuário específico."""
    response = client.get(f"/users/{test_user.id}")
    assert response.status_code == 200

    data = response.json()
    assert data["email"] == test_user.email
    assert data["name"] == test_user.name
    assert data["is_active"] == test_user.is_active
    assert data["id"] == test_user.id


def test_update_user(client: TestClient, test_user):
    """Testa a atualização de um usuário."""
    update_data = {"name": "Nome Atualizado"}

    response = client.put(f"/users/{test_user.id}", json=update_data)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["email"] == test_user.email  # Não modificado


def test_delete_user(client: TestClient, test_user, db: Session):
    """Testa a remoção de um usuário."""
    response = client.delete(f"/users/{test_user.id}")
    assert response.status_code == 204

    # Verifica se o usuário foi removido
    user = user_service.get_user(db, test_user.id)
    assert user is None
