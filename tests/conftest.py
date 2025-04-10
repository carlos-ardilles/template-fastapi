"""Fixtures compartilhadas para testes."""

import os
from typing import Any, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.db import Base, get_db
from app.main import create_application


# Use DATABASE_TEST_URL do ambiente ou use o padrão para SQLite
test_database_url = settings.DATABASE_TEST_URL or "sqlite:///./test.db"

# Cria o motor de banco de dados para testes
engine = create_engine(test_database_url, connect_args={
                       "check_same_thread": False})

# Cria uma classe de sessão local
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def app() -> Generator[FastAPI, Any, None]:
    """
    Cria um aplicativo FastAPI para os testes.
    """
    app = create_application()
    yield app


@pytest.fixture(scope="session")
def db() -> Generator[Session, Any, None]:
    """
    Cria um banco de dados de teste limpo para cada sessão de teste.
    """
    # Cria as tabelas no banco de dados de teste
    Base.metadata.create_all(bind=engine)

    # Cria uma sessão de teste
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Ao final dos testes, remove as tabelas
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(app: FastAPI, db: Session) -> Generator[TestClient, Any, None]:
    """
    Cria um cliente de teste para cada função de teste.

    Substitui a dependência get_db para usar o banco de dados de teste.
    """
    def _get_test_db():
        try:
            yield db
        finally:
            pass

    # Sobrescreve a dependência para usar a sessão de teste
    app.dependency_overrides[get_db] = _get_test_db

    with TestClient(app) as client:
        yield client

    # Remove a substituição de dependência após o teste
    app.dependency_overrides = {}
