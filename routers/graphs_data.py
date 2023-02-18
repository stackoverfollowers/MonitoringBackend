from datetime import datetime

from fastapi import APIRouter

from db.db import mongodb

router = APIRouter()


@router.get("/by_date", response_model=None)
async def graphs_data_by_date(date_from: datetime, date_to: datetime):
    await mongodb.get_data_by_date(date_from=date_from, date_to=date_to)

