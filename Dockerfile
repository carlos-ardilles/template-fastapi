FROM python:3.13-slim

# Define variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Define o diretório de trabalho
WORKDIR /app

# Instala o uv
RUN pip install uv

# Copia os arquivos de configuração
COPY pyproject.toml /app/

# Instala as dependências usando uv
RUN uv pip install --system  -r pyproject.toml

# Copia o restante do código
COPY . /app/

# Executa a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]