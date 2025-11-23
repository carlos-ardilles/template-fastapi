"""Módulo para interação com banco de dados."""

# SQLModel usa Session do SQLAlchemy nos bastidores
from sqlmodel import create_engine, Session
# from sqlalchemy.ext.declarative import declarative_base # Não é mais necessário para SQLModel
# from sqlalchemy.orm import sessionmaker # Session é importada de sqlmodel

from app.core.config import settings

# Cria o motor de conexão com o banco de dados
# Para SQLModel, o connect_args pode ser útil para SQLite, como {"check_same_thread": False}
# mas vamos manter como está por enquanto, assumindo que settings.DATABASE_URL está configurado adequadamente.
engine = create_engine(settings.DATABASE_URL)

# Base para os modelos ORM - SQLModel.metadata é usado globalmente
# Base = declarative_base() # Removido


def get_db():
    """Função para obter uma sessão do banco de dados.

    Retorna um gerador que fornece uma sessão do banco de dados
    e garante que a sessão seja fechada após o uso.
    """
    # SessionLocal não é mais definida separadamente, usamos Session diretamente do SQLModel
    # que é um wrapper em torno da sessionmaker do SQLAlchemy.
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()
