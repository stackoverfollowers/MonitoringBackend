from typing import Union

from fastapi import APIRouter

from consumer.mapper import ExMapper
from db.db import mongodb
from models.errors import BaseError
from models.exhauster_info import ExhausterInfoResponse, BearingExhausterResponse

router = APIRouter()


@router.get(
    "/exhauster/{index}", response_model=Union[ExhausterInfoResponse, BaseError]
)
async def get_exhauster(index: int):
    last_data = await mongodb.get_last_data()
    mapped_data = ExMapper(last_data["value"])
    bearings_data_all = mapped_data.map_bearings()

    if len(bearings_data_all) <= index or index < 0:
        return {"error": {"status": 1, "desc": "bad index"}}

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
