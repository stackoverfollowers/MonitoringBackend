import asyncio
import datetime
import json
from typing import Union

from fastapi import APIRouter
from starlette.websockets import WebSocket

from consumer.data_consumer import last_data
from consumer.mapper import ExMapper
from models.errors import BaseError, Error
from models.exhauster_info import ExhausterInfoResponse, BearingExhausterResponse

router = APIRouter()


def create_response(data: dict, index: int) -> Union[ExhausterInfoResponse, BaseError]:
    mapped_data = ExMapper(data)
    bearings_data_all = mapped_data.map_bearings()

    if len(bearings_data_all) <= index or index < 0:
        return BaseError(error=Error(status=1, desc="bad index"))

    bearings_data = bearings_data_all[index]
    oil_data = mapped_data.map_oil_systems()[index]
    electricity_data = mapped_data.map_main_gearings()[index]
    chiller_data = mapped_data.map_chillers()[index]
    gas_valve_data = mapped_data.map_valves()[index]
    gas_manifold_data = mapped_data.map_gas_manifolds()[index]

    bearings = [
        BearingExhausterResponse(
            index=bearing.index,
            temperature=bearing.temps.temp,
            axial_vibration=bearing.vibration.axial_vibration
            if bearing.vibration is not None
            else None,
            horizontal_vibration=bearing.vibration.horizontal_vibration
            if bearing.vibration is not None
            else None,
            vertical_vibration=bearing.vibration.vertical_vibration
            if bearing.vibration is not None
            else None,
        )
        for bearing in bearings_data.bearings
    ]
    return ExhausterInfoResponse(
        bearings=bearings,
        oil_level=oil_data.oil_level,
        oil_pressure=oil_data.oil_pressure,
        rotor_current=electricity_data.rotor_current,
        stator_current=electricity_data.stator_current,
        rotor_voltage=electricity_data.rotor_voltage,
        stator_voltage=electricity_data.stator_voltage,
        oil_temp_before=chiller_data.oil_temp.temperature_before,
        oil_temp_after=chiller_data.oil_temp.temperature_after,
        water_temp_before=chiller_data.water_temp.temperature_before,
        water_temp_after=chiller_data.water_temp.temperature_after,
        gas_valve_open=gas_valve_data.gas_valve_open,
        gas_valve_closed=gas_valve_data.gas_valve_closed,
        gas_valve_position=gas_valve_data.gas_valve_position,
        gas_temp_before=gas_manifold_data.temperature_before,
        gas_underpressure_before=gas_manifold_data.underpressure_before,
    )


@router.websocket("/ws/notify_exhauster/{index}")
async def notify_general_ws(websocket: WebSocket, index: int):
    await websocket.accept()
    old_timestamp = 0
    while True:
        await asyncio.sleep(0.33)
        if last_data.timestamp == old_timestamp:
            continue

        await websocket.send_text(
            json.dumps(
                create_response(last_data.data, index).dict(), ensure_ascii=False,
                default=lambda x: str(x) if not isinstance(x, datetime.datetime) else x.timestamp()
            )
        )
        old_timestamp = last_data.timestamp
