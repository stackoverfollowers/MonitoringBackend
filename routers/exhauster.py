from typing import Union

from fastapi import APIRouter

from consumer.mapper import ExMapper
from db.db import mongodb
from models.errors import BaseError
from models.exhauster_info import ExhausterInfoResponse, BearingExhausterResponse
from models.structs import ExhaustersData
from routers.utils import parse_exhauster_data

router = APIRouter()


@router.get(
    "/exhauster/{index}", response_model=Union[ExhausterInfoResponse, BaseError]
)
async def get_exhauster(index: int):
    last_data = await mongodb.get_last_data()
    mapped_data = ExMapper(last_data["value"])
    return parse_exhauster_data(mapped_data=mapped_data, index=index)
