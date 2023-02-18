import asyncio
import datetime
import json
from typing import Union

from fastapi import APIRouter
from starlette.websockets import WebSocket

from consumer.data_consumer import last_data
from consumer.mapper import ExMapper
from models.errors import BaseError, Error
from models.event import ExEventResponse, ExEvent
from models.exhauster_info import BearingExhausterResponse
from routers.notify_exhauster import create_exhauster_info

router = APIRouter()


def create_response(data: dict) -> ExEventResponse:
    mapped_data = ExMapper(data)
    bearings_data_all = mapped_data.map_bearings()
    events_all = []
    current_timestamp = datetime.datetime.now().timestamp()
    for i, exhauster in enumerate(bearings_data_all):
        exhauster_info = create_exhauster_info(data, i)
        for bearing in exhauster_info.bearings:
            is_event = any(
                map(
                    lambda status: status in ["warning", "alarm"],
                    [
                        bearing.temp_status,
                        bearing.vert_vibration_status,
                        bearing.hor_vibration_status,
                        bearing.vert_vibration_status,
                    ],
                ),
            )
            if is_event:
                events_all.append(
                    ExEvent(
                        timestamp=current_timestamp,
                        exhauster_index=exhauster.rotor_index,
                        exhauster_title=exhauster.exhauster_name,
                        bearing_index=bearing.index,
                    )
                )

    return ExEventResponse(events=events_all)


@router.websocket("/notify_events")
async def notify_events_ws(websocket: WebSocket):
    await websocket.accept()
    while True:
        await asyncio.sleep(1)
        await websocket.send_text(
            json.dumps(
                create_response(last_data.data).dict(),
                ensure_ascii=False,
                default=lambda x: str(x)
                if not isinstance(x, datetime.datetime)
                else x.timestamp(),
            )
        )
