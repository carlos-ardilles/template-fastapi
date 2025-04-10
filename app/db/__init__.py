"""Módulo para interação com banco de dados."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Cria o motor de conexão com o banco de dados
engine = create_engine(settings.DATABASE_URL)

# Classe para criar sessões do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos ORM
Base = declarative_base()


def get_db():
    """Função para obter uma sessão do banco de dados.

    Retorna um gerador que fornece uma sessão do banco de dados
    e garante que a sessão seja fechada após o uso.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
