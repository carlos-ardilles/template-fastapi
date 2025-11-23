"""Fixtures compartilhadas para testes."""

import os
from typing import Any, Generator
import uuid

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, SQLModel  # Importações do SQLModel

from app.core.config import settings
from app.db import get_db  # get_db foi atualizado para usar Session(engine)
from app.main import create_application
from app.db.models.user import User, UserCreate
from app.services import user_service


# Use DATABASE_TEST_URL do ambiente ou use o padrão para SQLite
# Usar os.getenv para consistência
test_database_url = os.getenv("DATABASE_TEST_URL", settings.DATABASE_TEST_URL)


# Cria o motor de banco de dados para testes
# Para SQLite com SQLModel, é importante `connect_args={"check_same_thread": False}`
engine = create_engine(test_database_url, connect_args={
                       "check_same_thread": False} if "sqlite" in test_database_url else {})

# TestingSessionLocal não é mais necessária da mesma forma, pois get_db será sobrescrito
# e a sessão será gerenciada diretamente.
# No entanto, para criar tabelas e limpar, ainda precisamos de uma sessão.


# autouse=True para garantir que as tabelas sejam criadas antes dos testes
@pytest.fixture(scope="session", autouse=True)
def setup_db() -> Generator[None, Any, None]:
    """
    Cria tabelas de teste antes de todos os testes e as remove depois.
    Este fixture é session-scoped e auto-used.
    """
    SQLModel.metadata.create_all(bind=engine)
    yield
    SQLModel.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(setup_db: None) -> Generator[Session, Any, None]:
    """
    Fornece uma sessão de banco de dados de teste para cada função de teste.
    As transações são revertidas após cada teste.
    """
    # Cria conexão diretamente do engine para controle manual da transação
    connection = engine.connect()
    transaction = connection.begin()

    try:
        # Cria sessão ligada à conexão com transação controlada
        session = Session(bind=connection)
        yield session
    finally:
        session.close()
        transaction.rollback()  # Reverte quaisquer alterações feitas durante o teste
        connection.close()


@pytest.fixture(scope="session")
def app() -> Generator[FastAPI, Any, None]:
    """
    Cria um aplicativo FastAPI para os testes (session-scoped).
    """
    _app = create_application()
    yield _app


@pytest.fixture(scope="function")
def client(app: FastAPI, db_session: Session) -> Generator[TestClient, Any, None]:
    """
    Cria um cliente de teste para cada função de teste.
    Substitui a dependência get_db para usar a sessão de banco de dados de teste.
    """
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass  # A sessão é gerenciada pelo fixture db_session

    app.dependency_overrides[get_db] = _get_test_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()  # Limpar overrides


@pytest.fixture
def user_create_data() -> dict:
    """Dados únicos para criação de usuário."""
    return {
        "email": f"teste-{uuid.uuid4()}@example.com",
        "password": "senha123",
        "name": "Usuário de Teste",
        "is_active": True
    }


@pytest.fixture
def test_user(db_session: Session, user_create_data: dict) -> User:
    """Cria um usuário de teste no banco de dados usando SQLModel."""
    user_in = UserCreate(**user_create_data)
    created_user = user_service.create_user(db=db_session, user=user_in)
    db_session.commit()
    db_session.refresh(created_user)
    return created_user
