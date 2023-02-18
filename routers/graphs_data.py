from datetime import datetime, timedelta

from fastapi import APIRouter

from db.db import mongodb
from models.errors import Error, BaseError
from models.structs import ExhaustersData, GraphData

router = APIRouter()


@router.get("/by_date", response_model=list[GraphData] | BaseError)
async def graphs_data_by_date(
    date_from: datetime, date_to: datetime, exhauster_index: int
):
    # КОСТЫЛЬ!!!
    date_from = date_from + timedelta(hours=3)
    date_to = date_to + timedelta(hours=3)

    if exhauster_index < 0 or exhauster_index > 5:
        return BaseError(error=Error(status=1, desc="bad index"))

    mapped_data_list = await mongodb.get_data_by_date(
        date_from=date_from, date_to=date_to
    )

    parsed_data = []
    for data in mapped_data_list:
        exhausters_data = ExhaustersData(
            moment=data.moment,
            bearings_data=data.map_bearings(),
            oil_data=data.map_oil_systems(),
            electricity_data=data.map_main_gearings(),
            chiller_data=data.map_chillers(),
            gas_valve_data=data.map_valves(),
            gas_manifold_data=data.map_gas_manifolds(),
        )
        indexed_exhauster = exhausters_data.get_single_exhauster_data(
            index=exhauster_index
        ).get_graphs_data()
        parsed_data.append(indexed_exhauster)
    return parsed_data
