# Template FastAPI

Template para projetos FastAPI com SQLAlchemy e Alembic, utilizando uv como gerenciador de pacotes. Inclui autenticação, estrutura de API organizada e suporte para Docker.

## Requisitos

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) para gerenciamento de pacotes e ambientes virtuais
- Docker e Docker Compose (opcional, para execução em contêineres)

## Instalação

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/template-fastapi.git
cd template-fastapi
```

Crie um ambiente virtual e instale as dependências com uv:

```bash
uv venv
source .venv/bin/activate  # No Windows use: .venv\Scripts\activate
uv pip install -e ".[dev]"
```

## Execução

### Localmente

Para iniciar o servidor de desenvolvimento localmente:

```bash
uv run uvicorn app.main:app --reload
```

O servidor estará disponível em `http://localhost:8000`.

### Com Docker

Você também pode executar o projeto usando Docker:

```bash
docker compose up
```

Isso iniciará tanto a aplicação FastAPI quanto um banco de dados PostgreSQL. O servidor estará disponível em `http://localhost:8000`.

## Documentação da API

Depois de iniciar o servidor, você pode acessar:
- Documentação Swagger UI: `http://localhost:8000/docs`
- Documentação ReDoc: `http://localhost:8000/redoc`

## Migrações de banco de dados

Este template já está configurado com Alembic para gerenciar migrações de banco de dados:

```bash
# Criar uma nova migração
alembic revision --autogenerate -m "descrição da migração"

# Aplicar migrações
alembic upgrade head
```

## Estrutura do Projeto

```
template-fastapi/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── dependencies/
│   │   │   └── auth.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── items.py
│   │       └── users.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   ├── __init__.py
│   │   └── models/
│   │       ├── item.py
│   │       └── user.py
│   ├── schemas/
│   │   ├── item.py
│   │   └── user.py
│   └── services/
│       ├── item_service.py
│       └── user_service.py
├── migrations/
│   ├── env.py
│   └── script.py.mako
├── tests/
│   ├── conftest.py
│   └── test_api/
│       ├── test_main.py
│       └── test_users.py
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── uv.lock
└── README.md
```

## Por que uv?

O uv é um gerenciador de pacotes Python de alta performance escrito em Rust que oferece:

- Instalação de pacotes 10-100x mais rápida que pip/poetry
- Compatibilidade com padrões existentes (pyproject.toml, requirements.txt)
- Resolução de dependências eficiente
- Criação e gerenciamento de ambientes virtuais
- Fácil integração com projetos existentes