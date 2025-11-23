"""Testes para as rotas de usuários com SQLModel."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
import uuid

from app.core.config import settings
from app.db.models.user import User
from app.services import user_service


def test_create_user(client: TestClient, user_create_data: dict):
    """Testa a criação de um novo usuário."""
    # user_create_data já tem email único
    response = client.post(
        f"{settings.API_V1_STR}/users/", json=user_create_data)
    assert response.status_code == 201, response.text

    data = response.json()
    assert data["email"] == user_create_data["email"]
    assert data["name"] == user_create_data["name"]
    assert data["is_active"] == user_create_data["is_active"]
    assert "id" in data
    assert "password" not in data  # hashed_password não deve ser retornado


# test_user garante que há pelo menos um usuário
def test_read_users(client: TestClient, test_user: User):
    """Testa a obtenção da lista de usuários."""
    response = client.get(f"{settings.API_V1_STR}/users/")
    assert response.status_code == 200, response.text

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Verifica se o test_user (que foi criado com UserRead) está na lista
    found = any(user["email"] == test_user.email and user["id"]
                == test_user.id for user in data)
    assert found, "Usuário de teste não encontrado na lista"


def test_read_user(client: TestClient, test_user: User):
    """Testa a obtenção de um usuário específico."""
    response = client.get(f"{settings.API_V1_STR}/users/{test_user.id}")
    assert response.status_code == 200, response.text

    data = response.json()
    # test_user é um objeto User (SQLModel), data é um dict (UserRead)
    assert data["email"] == test_user.email
    assert data["name"] == test_user.name
    assert data["is_active"] == test_user.is_active
    assert data["id"] == test_user.id


def test_update_user(client: TestClient, test_user: User):
    """Testa a atualização de um usuário."""
    update_data = {"name": "Nome Atualizado SQLModel",
                   "email": f"updated-{uuid.uuid4()}@example.com"}

    response = client.put(
        f"{settings.API_V1_STR}/users/{test_user.id}", json=update_data)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["email"] == update_data["email"]  # Email deve ser atualizado
    assert data["id"] == test_user.id


# Usa db_session para verificar
def test_delete_user(client: TestClient, test_user: User, db_session: Session):
    """Testa a remoção de um usuário."""
    response = client.delete(f"{settings.API_V1_STR}/users/{test_user.id}")
    assert response.status_code == 204, response.text

    # Verifica se o usuário foi removido do banco de dados
    user_in_db = user_service.get_user(db=db_session, user_id=test_user.id)
    assert user_in_db is None

# Adicionar teste para email já existente


def test_create_user_duplicate_email(client: TestClient, test_user: User):
    """Testa a criação de usuário com email duplicado."""
    user_data_duplicate = {
        "email": test_user.email,  # Email existente
        "password": "newpassword123",
        "name": "Outro Usuario",
        "is_active": True
    }
    response = client.post(
        f"{settings.API_V1_STR}/users/", json=user_data_duplicate)
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Email já registrado"

# Adicionar teste para usuário não encontrado


def test_read_user_not_found(client: TestClient):
    """Testa a obtenção de um usuário inexistente."""
    response = client.get(
        f"{settings.API_V1_STR}/users/999999")  # ID improvável
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Usuário não encontrado"


# Adicionar importação de settings para API_V1_STR
