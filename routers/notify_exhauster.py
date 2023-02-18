import asyncio
import datetime
import json
from typing import Union

from fastapi import APIRouter
from starlette.websockets import WebSocket
from websockets.exceptions import ConnectionClosedOK

from consumer.data_consumer import last_data
from consumer.mapper import ExMapper
from models.errors import BaseError, Error
from models.exhauster_info import ExhausterInfoResponse, BearingExhausterResponse
from routers.utils import parse_exhauster_data

router = APIRouter()


def create_exhauster_info(
    data: dict, index: int
) -> Union[ExhausterInfoResponse, BaseError]:
    mapped_data = ExMapper(data)
    return parse_exhauster_data(mapped_data=mapped_data, index=index)


@router.websocket("/notify_exhauster/{index}")
async def notify_general_ws(websocket: WebSocket, index: int):
    await websocket.accept()
    old_timestamp = 0
    while True:
        await asyncio.sleep(0.33)
        if last_data.timestamp == old_timestamp:
            continue

        await websocket.send_text(
            json.dumps(
                create_exhauster_info(last_data.data, index).dict(),
                ensure_ascii=False,
                default=lambda x: str(x)
                if not isinstance(x, datetime.datetime)
                else x.timestamp(),
            )
        )
        old_timestamp = last_data.timestamp
