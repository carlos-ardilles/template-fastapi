from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes import api_router


def create_application() -> FastAPI:
    """
    Cria e configura a aplicação FastAPI.

    Returns:
        FastAPI: A aplicação configurada
    """
    application = FastAPI(
        title=settings.PROJECT_NAME,
        description="Template para projetos FastAPI",
        version="0.1.0",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
    )

    # Configuração do CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Adiciona as rotas da API
    application.include_router(api_router)

    @application.get("/")
    async def root():
        return {
            "status": "online",
            "app_name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
        }

    return application


app = create_application()
