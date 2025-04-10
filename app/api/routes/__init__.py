"""Roteador principal da API."""

from fastapi import APIRouter

from app.api.routes.auth import router as auth_router
from app.api.routes.items import router as items_router
from app.api.routes.users import router as users_router

# Roteador principal que agrega todas as rotas
api_router = APIRouter()

# Adiciona os roteadores dos diferentes módulos
api_router.include_router(auth_router, prefix="/auth", tags=["authentication"])
api_router.include_router(items_router, prefix="/items", tags=["items"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
