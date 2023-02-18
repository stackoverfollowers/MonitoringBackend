from datetime import datetime

from fastapi import APIRouter

from db.db import mongodb
from models.structs import ExhaustersData, SingleExhausterData

router = APIRouter()


@router.get("/by_date", response_model=list[SingleExhausterData])
async def graphs_data_by_date(date_from: datetime, date_to: datetime, exhauster_index: int):
    mapped_data_list = await mongodb.get_data_by_date(date_from=date_from, date_to=date_to)
    parsed_data = []
    for data in mapped_data_list:
        exhausters_data = ExhaustersData(
            bearings_data=data.map_bearings(),
            oil_data=data.map_oil_systems(),
            electricity_data=data.map_main_gearings(),
            chiller_data=data.map_chillers(),
            gas_valve_data=data.map_valves(),
            gas_manifold_data=data.map_gas_manifolds(),
        )
        indexed_exhauster = exhausters_data.get_single_exhauster_data(index=exhauster_index)
        parsed_data.append(indexed_exhauster)
    return parsed_data
