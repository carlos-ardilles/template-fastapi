# Template FastAPI

Template para projetos FastAPI com SQLAlchemy e Alembic, utilizando uv como gerenciador de pacotes.

## Requisitos

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) para gerenciamento de pacotes e ambientes virtuais

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

Para iniciar o servidor de desenvolvimento:

```bash
uv run uvicorn app.main:app --reload
```

O servidor estará disponível em `http://localhost:8000`.

## Documentação da API

Depois de iniciar o servidor, você pode acessar:
- Documentação Swagger UI: `http://localhost:8000/docs`
- Documentação ReDoc: `http://localhost:8000/redoc`

## Migrações de banco de dados

Este template está configurado com Alembic para gerenciar migrações de banco de dados:

```bash
# Inicializar migrações
alembic init migrations

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
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   └── services/
├── migrations/
├── tests/
├── .gitignore
├── pyproject.toml
└── README.md
```

## Por que uv?

O uv é um gerenciador de pacotes Python de alta performance escrito em Rust que oferece:

- Instalação de pacotes 10-100x mais rápida que pip/poetry
- Compatibilidade com padrões existentes (pyproject.toml, requirements.txt)
- Resolução de dependências eficiente
- Criação e gerenciamento de ambientes virtuais
- Fácil integração com projetos existentes