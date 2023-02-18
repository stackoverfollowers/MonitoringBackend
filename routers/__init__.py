from fastapi import APIRouter

from .alive import router as alive_router
from .notify_general import router as notify_general_router
from .notify_exhauster import router as notify_exhauster_router
from .notify_events import router as notify_events_router
from .general import router as general_router
from .exhauster import router as exhauster_router

api_router = APIRouter()
api_router.include_router(alive_router)
api_router.include_router(notify_general_router)
api_router.include_router(notify_exhauster_router)
api_router.include_router(general_router)
api_router.include_router(exhauster_router)
api_router.include_router(notify_events_router)
