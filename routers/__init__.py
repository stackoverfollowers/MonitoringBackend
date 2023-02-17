from fastapi import APIRouter

from .alive import router as alive_router
from .general import router as general_router

api_router = APIRouter()
api_router.include_router(alive_router)
api_router.include_router(general_router)
