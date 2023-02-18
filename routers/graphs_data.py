from datetime import datetime

from fastapi import APIRouter

from db.db import mongodb

router = APIRouter()


@router.get("/by_date", response_model=None)
async def graphs_data_by_date(date_from: datetime, date_to: datetime, exhauster_index: int):
    mapped_data_list = await mongodb.get_data_by_date(date_from=date_from, date_to=date_to)
    for data in mapped_data_list:
        exhauster_bearings = data.map_bearings()[exhauster_index]
        bearings_data = exhauster_bearings[exhauster_index]
        oil_data = mapped_data.map_oil_systems()[exhauster_index]
        electricity_data = mapped_data.map_main_gearings()[exhauster_index]
        chiller_data = mapped_data.map_chillers()[exhauster_index]
        gas_valve_data = mapped_data.map_valves()[exhauster_index]
        gas_manifold_data = mapped_data.map_gas_manifolds()[exhauster_index]
