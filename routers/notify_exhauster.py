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

router = APIRouter()


def create_exhauster_info(
    data: dict, index: int
) -> Union[ExhausterInfoResponse, BaseError]:
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

    bearings = []
    for bearing in bearings_data.bearings:
        temp_status = (
            "alarm"
            if (75 < bearing.temps.temp >= 65)
            else ("warning" if (bearing.temps.temp >= 75) else "default")
        )
        if bearing.vibration is None:
            vert_vibration_status = (
                hor_vibration_status
            ) = axial_vibration_status = "default"
        else:
            vert_vibration_status = (
                "alarm"
                if (7.1 < bearing.vibration.vertical_vibration >= 4.5)
                else (
                    "warning"
                    if (bearing.vibration.vertical_vibration >= 7.1)
                    else "default"
                )
            )
            hor_vibration_status = (
                "alarm"
                if (7.1 < bearing.vibration.horizontal_vibration >= 4.5)
                else (
                    "warning"
                    if (bearing.vibration.horizontal_vibration >= 7.1)
                    else "default"
                )
            )
            axial_vibration_status = (
                "warning"
                if (7.1 < bearing.vibration.axial_vibration >= 4.5)
                else (
                    "alarm" if (bearing.vibration.axial_vibration >= 7.1) else "default"
                )
            )

        new_bearing = BearingExhausterResponse(
            index=bearing.index,
            temperature=bearing.temps.temp,
            temp_status=temp_status,
            axial_vibration=bearing.vibration.axial_vibration
            if bearing.vibration is not None
            else None,
            axial_vibration_status=axial_vibration_status,
            horizontal_vibration=bearing.vibration.horizontal_vibration
            if bearing.vibration is not None
            else None,
            hor_vibration_status=hor_vibration_status,
            vertical_vibration=bearing.vibration.vertical_vibration
            if bearing.vibration is not None
            else None,
            vert_vibration_status=vert_vibration_status,
        )
        bearings.append(new_bearing)

    oil_level_status = (
        "warning"
        if oil_data.oil_level < 20.0
        else ("alarm" if oil_data.oil_level < 10.0 else "default")
    )

    if index in (0, 1):
        oil_pressure_status = "alarm" if oil_data.oil_pressure < 0.5 else "default"
        rotor_current_status = (
            "warning" if electricity_data.rotor_current >= 250 else "default"
        )

    else:
        oil_pressure_status = "alarm" if oil_data.oil_pressure < 0.2 else "default"
        rotor_current_status = (
            "warning" if electricity_data.rotor_current >= 200 else "default"
        )

    stator_current_status = (
        "alarm"
        if (electricity_data.stator_current >= 280)
        else (
            "warning" if (280 < electricity_data.stator_current >= 230) else "default"
        )
    )

    oil_temp_before_status = (
        "warning" if chiller_data.oil_temp.temperature_before >= 30 else "default"
    )

    oil_temp_after_status = (
        "warning" if chiller_data.oil_temp.temperature_after >= 30 else "default"
    )

    water_temp_before_status = (
        "warning" if chiller_data.water_temp.temperature_before >= 30 else "default"
    )

    water_temp_after_status = (
        "warning" if chiller_data.water_temp.temperature_after >= 30 else "default"
    )

    return ExhausterInfoResponse(
        bearings=bearings,
        oil_level=oil_data.oil_level,
        oil_level_status=oil_level_status,
        oil_pressure=oil_data.oil_pressure,
        oil_pressure_status=oil_pressure_status,
        rotor_current=electricity_data.rotor_current,
        rotor_current_status=rotor_current_status,
        stator_current=electricity_data.stator_current,
        stator_current_status=stator_current_status,
        rotor_voltage=electricity_data.rotor_voltage,
        stator_voltage=electricity_data.stator_voltage,
        oil_temp_before=chiller_data.oil_temp.temperature_before,
        oil_temp_before_status=oil_temp_before_status,
        oil_temp_after=chiller_data.oil_temp.temperature_after,
        oil_temp_after_status=oil_temp_after_status,
        water_temp_before=chiller_data.water_temp.temperature_before,
        water_temp_before_status=water_temp_before_status,
        water_temp_after=chiller_data.water_temp.temperature_after,
        water_temp_after_status=water_temp_after_status,
        gas_valve_open=gas_valve_data.gas_valve_open,
        gas_valve_closed=gas_valve_data.gas_valve_closed,
        gas_valve_position=gas_valve_data.gas_valve_position,
        gas_temp_before=gas_manifold_data.temperature_before,
        gas_underpressure_before=gas_manifold_data.underpressure_before,
    )


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
