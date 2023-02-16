from fastapi import APIRouter

from .alive import router as alive_router

api_router = APIRouter()
api_router.include_router(alive_router)
