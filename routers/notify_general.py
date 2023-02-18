import asyncio
import datetime
import json

from fastapi import APIRouter
from starlette.websockets import WebSocket
from websockets.exceptions import ConnectionClosedOK

from consumer.data_consumer import last_data
from consumer.mapper import ExMapper
from models.general import (
    BearingResponse,
    Exhauster,
    SinterMachine,
    GeneralPageResponse,
)

router = APIRouter()


def create_response(data: dict):
    mapped_data = ExMapper(data)

    exhauster_bearings = mapped_data.map_bearings()
    works_mapped = mapped_data.map_exhauster_works()
    oil_mapped = mapped_data.map_oil_systems()
    exhausters = []
    for i in range(len(exhauster_bearings)):
        current_bearings = []
        # TODO)_))!#)(!)(_@*&*Z@^(@#^(#@(78
        for j in range(len(exhauster_bearings[i].bearings)):
            bearing = exhauster_bearings[i].bearings[j]
            bearing_temps = bearing.temps
            is_temp_alarm = (
                bearing.temps.temp is None
                or bearing.temps.setting_temp.alarm_max is None
                or bearing.temps.setting_temp.alarm_min is None
                or bearing.temps.temp >= bearing.temps.setting_temp.alarm_max
                or bearing.temps.temp <= bearing.temps.setting_temp.alarm_min
            )
            is_temp_warning = (
                bearing_temps.temp is None
                or bearing_temps.setting_temp.warning_min is None
                or bearing_temps.setting_temp.warning_max is None
                or bearing_temps.temp >= bearing_temps.setting_temp.warning_max
                or bearing_temps.temp <= bearing_temps.setting_temp.warning_min
            )
            temp_status = (
                "alarm"
                if is_temp_alarm
                else ("warning" if is_temp_warning else "default")
            )
            bearing_vibration = bearing.vibration

            is_vibration_warning = (
                (
                    bearing_vibration.vertical_vibration is None
                    or bearing_vibration.vertical_vibration_stats.warning_max is None
                    or bearing_vibration.vertical_vibration_stats.warning_min is None
                    or bearing_vibration.axial_vibration_stats.warning_max is None
                    or bearing_vibration.axial_vibration_stats.warning_min is None
                    or bearing_vibration.horizontal_vibration_stats.warning_max is None
                    or bearing_vibration.horizontal_vibration_stats.warning_min is None
                    or bearing_vibration.vertical_vibration
                    >= bearing_vibration.vertical_vibration_stats.warning_max
                    or bearing_vibration.vertical_vibration
                    <= bearing_vibration.vertical_vibration_stats.warning_min
                    or bearing_vibration.axial_vibration
                    >= bearing_vibration.axial_vibration_stats.warning_max
                    or bearing_vibration.axial_vibration
                    <= bearing_vibration.axial_vibration_stats.warning_min
                    or bearing_vibration.horizontal_vibration
                    >= bearing_vibration.horizontal_vibration_stats.warning_max
                    or bearing.vibration.horizontal_vibration
                    <= bearing_vibration.horizontal_vibration_stats.warning_min
                )
                if bearing_vibration is not None
                else None
            )

            is_vibration_alarm = (
                (
                    bearing_vibration.vertical_vibration is None
                    or bearing_vibration.vertical_vibration_stats.alarm_max is None
                    or bearing_vibration.vertical_vibration_stats.alarm_min is None
                    or bearing_vibration.axial_vibration_stats.alarm_max is None
                    or bearing_vibration.axial_vibration_stats.alarm_min is None
                    or bearing_vibration.horizontal_vibration_stats.alarm_max is None
                    or bearing_vibration.horizontal_vibration_stats.alarm_min is None
                    or bearing_vibration.vertical_vibration
                    >= bearing_vibration.vertical_vibration_stats.alarm_max
                    or bearing_vibration.vertical_vibration
                    <= bearing_vibration.vertical_vibration_stats.alarm_min
                    or bearing_vibration.axial_vibration
                    >= bearing_vibration.axial_vibration_stats.alarm_max
                    or bearing_vibration.axial_vibration
                    <= bearing_vibration.axial_vibration_stats.alarm_min
                    or bearing_vibration.horizontal_vibration
                    >= bearing_vibration.horizontal_vibration_stats.alarm_max
                    or bearing_vibration.horizontal_vibration
                    <= bearing_vibration.horizontal_vibration_stats.alarm_min
                )
                if bearing_vibration is not None
                else None
            )

            vibration_status = (
                "alarm"
                if is_vibration_alarm
                else ("warning" if is_vibration_warning else "default")
            )

            new_bearing = BearingResponse(
                index=bearing.index,
                is_temp_warning=is_temp_warning,
                is_temp_alarm=is_temp_alarm,
                is_vibration_warning=is_vibration_warning,
                is_vibration_alarm=is_vibration_alarm,
                vibration_status=vibration_status,
                temp_status=temp_status,
            )
            current_bearings.append(new_bearing)

        exhausters.append(
            Exhauster(
                title=exhauster_bearings[i].exhauster_name,
                is_work=works_mapped[i].work,
                rotor_title=exhauster_bearings[i].rotor_index,
                date_last_change=datetime.datetime.now(),  # todo
                days_last_change=1,  # todo
                days_forecast=1,  # todo
                forecast_warning=False,  # todo
                forecast_alarm=False,  # todo
                bearings=current_bearings,
                oil_level=oil_mapped[i].oil_level,
                oil_pressure=oil_mapped[i].oil_pressure,
            )
        )

    machines = [
        SinterMachine(exhausters=exhausters[i : i + 2])
        for i in range(0, len(exhausters), 2)
    ]

    return GeneralPageResponse(sinter_machines=[machine for machine in machines])


@router.websocket("/notify_general")
async def notify_general_ws(websocket: WebSocket):
    old_timestamp = 0
    await websocket.accept()
    while True:
        await asyncio.sleep(0.33)
        if last_data.timestamp == old_timestamp:
            continue

        await websocket.send_text(
            json.dumps(
                create_response(last_data.data).dict(),
                ensure_ascii=False,
                default=lambda x: str(x)
                if not isinstance(x, datetime.datetime)
                else x.timestamp(),
            )
        )
        old_timestamp = last_data.timestamp
