from fastapi import APIRouter

router = APIRouter()


@router.get("/alive")
async def is_alive():
    return {"iam": "alive"}
