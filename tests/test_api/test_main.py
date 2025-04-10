"""Testes para as rotas principais da aplicação."""

from fastapi.testclient import TestClient

from app.core.config import settings


def test_read_root(client: TestClient):
    """Testa o endpoint raiz (health check) da aplicação."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "status": "online",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }
