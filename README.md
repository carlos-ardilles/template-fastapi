# Template FastAPI

Template para projetos FastAPI com **SQLModel** e Alembic, utilizando uv como gerenciador de pacotes. Inclui autenticação JWT, estrutura de API organizada e suporte para Docker.

## ✨ Características

- **SQLModel**: Modelos unificados que servem tanto para banco de dados quanto para validação de API
  - Elimina duplicação de código entre schemas Pydantic e modelos SQLAlchemy
  - Type safety completo com auto-completamento
  - Validação automática de dados
  - Serialização/deserialização JSON nativa
- **FastAPI**: Framework moderno e rápido para criação de APIs
- **Autenticação JWT**: Sistema completo de autenticação com tokens
- **Alembic**: Migrações de banco de dados automáticas
- **uv**: Gerenciador de pacotes ultra-rápido
- **Testes**: Suite completa de testes com pytest (19 testes implementados)
- **Docker**: Suporte para containerização
- **Arquitetura Limpa**: Separação clara entre camadas (models, services, routes)
- **Tipo Safety**: Tipagem completa com Python e Pydantic

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

## Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Banco de Dados
DATABASE_URL=sqlite:///./test.db

# Segurança
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API
API_V1_STR=/api/v1
PROJECT_NAME=Template FastAPI
```

**Nota**: Em produção, use um banco PostgreSQL e gere uma chave secreta segura:

```bash
# Gerar chave secreta segura
python -c "import secrets; print(secrets.token_urlsafe(32))"
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
# Desenvolvimento com hot-reload
docker compose up

# Build para produção
docker compose -f docker-compose.prod.yml up --build
```

Isso iniciará tanto a aplicação FastAPI quanto um banco de dados PostgreSQL. O servidor estará disponível em `http://localhost:8000`.

### Deployment

Para produção, considere usar:

- **Railway/Render/Fly.io**: Plataformas simples para deployment
- **AWS/GCP/Azure**: Soluções cloud robustas
- **Docker**: Container pronto para qualquer orquestrador

Exemplo de comando para produção:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Documentação da API

Depois de iniciar o servidor, você pode acessar:
- Documentação Swagger UI: `http://localhost:8000/docs`
- Documentação ReDoc: `http://localhost:8000/redoc`

## Funcionalidades da API

### Autenticação
- **POST** `/api/v1/auth/login` - Login com email/senha, retorna token JWT
- Autenticação via Bearer token nos endpoints protegidos

### Usuários
- **POST** `/api/v1/users/` - Criar novo usuário
- **GET** `/api/v1/users/me` - Obter dados do usuário autenticado (requer auth)
- **PUT** `/api/v1/users/me` - Atualizar dados do usuário autenticado (requer auth)

### Items
- **POST** `/api/v1/items/` - Criar novo item (requer auth)
- **GET** `/api/v1/items/` - Listar items do usuário autenticado (requer auth)
- **GET** `/api/v1/items/{item_id}` - Obter item específico (requer auth + propriedade)
- **PUT** `/api/v1/items/{item_id}` - Atualizar item (requer auth + propriedade)
- **DELETE** `/api/v1/items/{item_id}` - Deletar item (requer auth + propriedade)

### Exemplo de Uso

```bash
# Criar usuário
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "senha123"}'

# Fazer login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=senha123"

# Criar item (usando token)
curl -X POST "http://localhost:8000/api/v1/items/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Meu Item", "description": "Descrição do item"}'
```

## Migrações de banco de dados

Este template já está configurado com Alembic para gerenciar migrações de banco de dados:

```bash
# Criar uma nova migração
alembic revision --autogenerate -m "descrição da migração"

# Aplicar migrações
alembic upgrade head
```

## Testes

O projeto inclui uma suite completa de testes com 19 testes implementados:

```bash
# Executar todos os testes
uv run pytest

# Executar testes com cobertura
uv run pytest --cov=app

# Executar testes específicos
uv run pytest tests/test_api/test_users.py
uv run pytest tests/test_api/test_items.py
```

### Cobertura de Testes

- **Usuários**: 8 testes cobrindo CRUD completo e autenticação
- **Items**: 11 testes incluindo autorização e validação de propriedade
- **Autenticação**: Testes de login, tokens JWT e permissões
- **Fixtures compartilhadas**: Configuração reutilizável de testes

### Estrutura dos Testes

- `conftest.py`: Configuração global e fixtures compartilhadas
- `test_users.py`: Testes para API de usuários
- `test_items.py`: Testes para API de items com autorização
- `test_main.py`: Testes básicos da aplicação

## Estrutura do Projeto

```
template-fastapi/
├── app/
│   ├── __init__.py
│   ├── main.py                    # Ponto de entrada da aplicação
│   ├── api/
│   │   ├── dependencies/
│   │   │   └── auth.py           # Dependências de autenticação
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── auth.py           # Rotas de autenticação (login)
│   │       ├── items.py          # CRUD de items com autorização
│   │       └── users.py          # CRUD de usuários
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py             # Configurações da aplicação
│   │   └── security.py           # Utilitários de segurança (JWT, hash)
│   ├── db/
│   │   ├── __init__.py           # Configuração do banco de dados
│   │   └── models/
│   │       ├── item.py           # Modelo SQLModel para Items
│   │       └── user.py           # Modelo SQLModel para Users
│   └── services/
│       ├── item_service.py       # Lógica de negócio para Items
│       └── user_service.py       # Lógica de negócio para Users
├── migrations/                   # Migrações Alembic
│   ├── env.py                   # Configuração do Alembic
│   ├── script.py.mako
│   └── versions/                # Arquivos de migração
├── tests/
│   ├── conftest.py              # Configuração dos testes
│   └── test_api/
│       ├── test_items.py        # Testes para API de items (11 testes)
│       ├── test_main.py         # Testes básicos da aplicação
│       └── test_users.py        # Testes para API de usuários (8 testes)
├── alembic.ini                  # Configuração do Alembic
├── docker-compose.yml           # Docker Compose para desenvolvimento
├── Dockerfile                   # Imagem Docker da aplicação
├── pyproject.toml              # Configuração do projeto e dependências
├── uv.lock                     # Lock file do uv
└── README.md
```

### Benefícios da Arquitetura SQLModel

Este template utiliza **SQLModel**, uma biblioteca criada pelo mesmo autor do FastAPI que unifica:

1. **Modelos únicos**: Uma única classe serve como modelo de banco de dados e schema de API
2. **Redução de código**: Elimina a duplicação entre schemas Pydantic e modelos SQLAlchemy
3. **Type safety**: Tipagem completa em todo o pipeline de dados
4. **Validação automática**: Pydantic validators integrados aos modelos de banco
5. **Auto-completamento**: IDEs fornecem sugestões precisas baseadas nos tipos

## Por que uv?

O uv é um gerenciador de pacotes Python de alta performance escrito em Rust que oferece:

- **Performance**: Instalação de pacotes 10-100x mais rápida que pip/poetry
- **Compatibilidade**: Funciona com padrões existentes (pyproject.toml, requirements.txt)
- **Eficiência**: Resolução de dependências inteligente e cache otimizado
- **Simplicidade**: Comandos diretos e intuitivos
- **Confiabilidade**: Lock files determinísticos para builds reproduzíveis

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Links Úteis

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

---

**Template FastAPI com SQLModel** - Um template moderno e completo para desenvolvimento de APIs Python com tipagem forte, validação automática e arquitetura limpa.