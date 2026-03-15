"""Testes para as rotas de usuários com SQLModel."""

import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.db.models.user import User
from app.services import user_service


def test_create_user(client: TestClient, user_create_data: dict):
    """Testa a criação de um novo usuário."""
    response = client.post(f"{settings.API_V1_STR}/users/", json=user_create_data)
    assert response.status_code == 201, response.text

    data = response.json()
    assert data["email"] == user_create_data["email"]
    assert data["name"] == user_create_data["name"]
    assert data["is_active"] == user_create_data["is_active"]
    assert "id" in data
    assert "password" not in data


def test_read_users_returns_only_authenticated_user(
    client: TestClient, test_user: User, auth_headers: dict[str, str]
):
    """Testa que a listagem de usuários não expõe outros registros."""
    response = client.get(f"{settings.API_V1_STR}/users/", headers=auth_headers)
    assert response.status_code == 200, response.text

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["email"] == test_user.email
    assert data[0]["id"] == test_user.id


def test_read_me(client: TestClient, test_user: User, auth_headers: dict[str, str]):
    """Testa o endpoint /users/me."""
    response = client.get(f"{settings.API_V1_STR}/users/me", headers=auth_headers)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["email"] == test_user.email
    assert data["id"] == test_user.id


def test_read_user(client: TestClient, test_user: User, auth_headers: dict[str, str]):
    """Testa leitura do próprio usuário."""
    response = client.get(f"{settings.API_V1_STR}/users/{test_user.id}", headers=auth_headers)
    assert response.status_code == 200, response.text


def test_read_user_forbidden(client: TestClient, auth_headers: dict[str, str]):
    """Testa bloqueio de leitura de outro usuário."""
    response = client.get(f"{settings.API_V1_STR}/users/999999", headers=auth_headers)
    assert response.status_code == 403, response.text


def test_update_user(client: TestClient, test_user: User, auth_headers: dict[str, str]):
    """Testa a atualização do próprio usuário."""
    update_data = {"name": "Nome Atualizado SQLModel", "email": f"updated-{uuid.uuid4()}@example.com"}

    response = client.put(
        f"{settings.API_V1_STR}/users/{test_user.id}", json=update_data, headers=auth_headers
    )
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["email"] == update_data["email"]
    assert data["id"] == test_user.id


def test_delete_user(
    client: TestClient, test_user: User, db_session: Session, auth_headers: dict[str, str]
):
    """Testa a remoção do próprio usuário."""
    response = client.delete(f"{settings.API_V1_STR}/users/{test_user.id}", headers=auth_headers)
    assert response.status_code == 204, response.text

    user_in_db = user_service.get_user(db=db_session, user_id=test_user.id)
    assert user_in_db is None


def test_create_user_duplicate_email(client: TestClient, test_user: User):
    """Testa a criação de usuário com email duplicado."""
    user_data_duplicate = {
        "email": test_user.email,
        "password": "newpassword123",
        "name": "Outro Usuario",
        "is_active": True,
    }
    response = client.post(f"{settings.API_V1_STR}/users/", json=user_data_duplicate)
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Email já registrado"


def test_read_users_requires_authentication(client: TestClient):
    """Testa que listagem de usuários exige autenticação."""
    response = client.get(f"{settings.API_V1_STR}/users/")
    assert response.status_code == 401, response.text
