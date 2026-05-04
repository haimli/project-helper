from fastapi import APIRouter

from app.api.projects import router as projects_router
from app.api.chat import router as chat_router

api_router = APIRouter()
api_router.include_router(projects_router, prefix="/projects", tags=["projects"])
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])
