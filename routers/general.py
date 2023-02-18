import datetime

from fastapi import APIRouter

from consumer.mapper import ExMapper
from db.db import mongodb
from models.general import (
    GeneralPageResponse,
    SinterMachine,
    Exhauster,
    BearingResponse,
)

router = APIRouter()


@router.get("/general", response_model=GeneralPageResponse)
async def general_page():
    last_data = await mongodb.get_last_data()
    mapped_data = ExMapper(last_data["value"])

    exhauster_bearings = mapped_data.map_bearings()
    works_mapped = mapped_data.map_exhauster_works()
    oil_mapped = mapped_data.map_oil_systems()
    exhausters = []
    for i in range(len(exhauster_bearings)):
        current_bearings = []
        # TODO)_))!#)(!)(_@*&*Z@^(@#^(#@(78
        for j in range(len(exhauster_bearings[i].bearings)):
            new_bearing = BearingResponse(
                index=exhauster_bearings[i].bearings[j].index,
                is_temp_warning=(
                    exhauster_bearings[i].bearings[j].temps.temp is None
                    or exhauster_bearings[i].bearings[j].temps.setting_temp.warning_min
                    is None
                    or exhauster_bearings[i].bearings[j].temps.setting_temp.warning_max
                    is None
                    or exhauster_bearings[i].bearings[j].temps.temp
                    >= exhauster_bearings[i].bearings[j].temps.setting_temp.warning_max
                    or exhauster_bearings[i].bearings[j].temps.temp
                    <= exhauster_bearings[i].bearings[j].temps.setting_temp.warning_min
                ),
                is_temp_alarm=(
                    exhauster_bearings[i].bearings[j].temps.temp is None
                    or exhauster_bearings[i].bearings[j].temps.setting_temp.alarm_max
                    is None
                    or exhauster_bearings[i].bearings[j].temps.setting_temp.alarm_min
                    is None
                    or exhauster_bearings[i].bearings[j].temps.temp
                    >= exhauster_bearings[i].bearings[j].temps.setting_temp.alarm_max
                    or exhauster_bearings[i].bearings[j].temps.temp
                    <= exhauster_bearings[i].bearings[j].temps.setting_temp.alarm_min
                ),
                is_vibration_warning=(
                    exhauster_bearings[i].bearings[j].vibration.vertical_vibration
                    is None
                    or exhauster_bearings[i]
                    .bearings[j]
                    .vibration.vertical_vibration_stats.warning_max
                    is None
                    or exhauster_bearings[i]
                    .bearings[j]
                    .vibration.vertical_vibration_stats.warning_min
                    is None
                    or exhauster_bearings[i]
                    .bearings[j]
                    .vibration.axial_vibration_stats.warning_max
                    is None
                    or exhauster_bearings[i]
                    .bearings[j]
                    .vibration.axial_vibration_stats.warning_min
                    is None
                    or exhauster_bearings[i]
                    .bearings[j]
                    .vibration.horizontal_vibration_stats.warning_max
                    is None
                    or exhauster_bearings[i]
                    .bearings[j]
                    .vibration.horizontal_vibration_stats.warning_min
                    is None
                    or exhauster_bearings[i].bearings[j].vibration.vertical_vibration
                    >= exhauster_bearings[i]
                    .bearings[j]
                    .vibration.vertical_vibration_stats.warning_max
                    or exhauster_bearings[i].bearings[j].vibration.vertical_vibration
                    <= exhauster_bearings[i]
                    .bearings[j]
                    .vibration.vertical_vibration_stats.warning_min
                    or exhauster_bearings[i].bearings[j].vibration.axial_vibration
                    >= exhauster_bearings[i]
                    .bearings[j]
                    .vibration.axial_vibration_stats.warning_max
                    or exhauster_bearings[i].bearings[j].vibration.axial_vibration
                    <= exhauster_bearings[i]
                    .bearings[j]
                    .vibration.axial_vibration_stats.warning_min
                    or exhauster_bearings[i].bearings[j].vibration.horizontal_vibration
                    >= exhauster_bearings[i]
                    .bearings[j]
                    .vibration.horizontal_vibration_stats.warning_max
                    or exhauster_bearings[i].bearings[j].vibration.horizontal_vibration
                    <= exhauster_bearings[i]
                    .bearings[j]
                    .vibration.horizontal_vibration_stats.warning_min
                )
                if exhauster_bearings[i].bearings[j].vibration is not None
                else None,
                is_vibration_alarm=(
                    exhauster_bearings[i].bearings[j].vibration.vertical_vibration
                    is None
                    or exhauster_bearings[i]
                    .bearings[j]
                    .vibration.vertical_vibration_stats.alarm_max
                    is None
                    or exhauster_bearings[i]
                    .bearings[j]
                    .vibration.vertical_vibration_stats.alarm_min
                    is None
                    or exhauster_bearings[i]
                    .bearings[j]
                    .vibration.axial_vibration_stats.alarm_max
                    is None
                    or exhauster_bearings[i]
                    .bearings[j]
                    .vibration.axial_vibration_stats.alarm_min
                    is None
                    or exhauster_bearings[i]
                    .bearings[j]
                    .vibration.horizontal_vibration_stats.alarm_max
                    is None
                    or exhauster_bearings[i]
                    .bearings[j]
                    .vibration.horizontal_vibration_stats.alarm_min
                    is None
                    or exhauster_bearings[i].bearings[j].vibration.vertical_vibration
                    >= exhauster_bearings[i]
                    .bearings[j]
                    .vibration.vertical_vibration_stats.alarm_max
                    or exhauster_bearings[i].bearings[j].vibration.vertical_vibration
                    <= exhauster_bearings[i]
                    .bearings[j]
                    .vibration.vertical_vibration_stats.alarm_min
                    or exhauster_bearings[i].bearings[j].vibration.axial_vibration
                    >= exhauster_bearings[i]
                    .bearings[j]
                    .vibration.axial_vibration_stats.alarm_max
                    or exhauster_bearings[i].bearings[j].vibration.axial_vibration
                    <= exhauster_bearings[i]
                    .bearings[j]
                    .vibration.axial_vibration_stats.alarm_min
                    or exhauster_bearings[i].bearings[j].vibration.horizontal_vibration
                    >= exhauster_bearings[i]
                    .bearings[j]
                    .vibration.horizontal_vibration_stats.alarm_max
                    or exhauster_bearings[i].bearings[j].vibration.horizontal_vibration
                    <= exhauster_bearings[i]
                    .bearings[j]
                    .vibration.horizontal_vibration_stats.alarm_min
                )
                if exhauster_bearings[i].bearings[j].vibration is not None
                else None,
            )
            current_bearings.append(new_bearing)
        exhausters.append(
            Exhauster(
                title=exhauster_bearings[i].exhauster_name,
                is_work=works_mapped[i].work,
                rotor_title="no data?",  # todo
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

    print(len(exhausters))
    machines = [
        SinterMachine(exhausters=exhausters[i : i + 2])
        for i in range(0, len(exhausters), 2)
    ]

    return GeneralPageResponse(sinter_machines=[machine for machine in machines])