FROM python:3.9-slim

# Define variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.5.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

# Define o diretório de trabalho
WORKDIR /app

# Instala o Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copia os arquivos de configuração
COPY pyproject.toml poetry.lock* /app/

# Instala as dependências
RUN poetry install --no-dev

# Copia o restante do código
COPY . /app/

# Executa a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]