from fastapi import APIRouter

from app.api.endpoints import user, auth
from app.settings import settings

api_router = APIRouter(prefix=settings.API_V1_STR)

api_router.include_router(auth.router)
api_router.include_router(user.router)
