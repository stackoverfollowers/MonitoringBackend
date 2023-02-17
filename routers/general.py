from fastapi import APIRouter

from consumer.mapper import ExMapper
from db.db import mongodb
from models.general import GeneralPageResponse, SinterMachine

router = APIRouter()


@router.get("/general", response_model=GeneralPageResponse)
async def general_page():
    last_data = await mongodb.get_last_data()
    mapped_data = ExMapper(last_data["value"])

    exhauseters = []
    machines = [SinterMachine(exhausters=[exhauseter for exhauseter in exhauseters])]

    return GeneralPageResponse(sinter_machines=[machine for machine in machines])
