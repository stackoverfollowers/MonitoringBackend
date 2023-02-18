from dataclasses import dataclass
from datetime import datetime

from consumer.structs import (
    OilSystem,
    ExhausterInfo,
    MainGearing,
    Chiller,
    ValvePosition,
    GasManifold, Bearing,
)


@dataclass
class BearingGraphData:
    temp: float
    index: int = 1
    axial_vibration: float | None = None
    horizontal_vibration: float | None = None
    vertical_vibration: float | None = None

    @classmethod
    def from_bearing_data(cls, bearing_data: Bearing):
        temp = bearing_data.temps.temp
        if bearing_data.vibration is None:
            return cls(
                temp=temp
            )
        return cls(
            temp=temp,
            axial_vibration=bearing_data.vibration.axial_vibration,
            horizontal_vibration=bearing_data.vibration.horizontal_vibration,
            vertical_vibration=bearing_data.vibration.vertical_vibration
        )


@dataclass
class ChillerGraphData:
    oil_temp_before: float
    oil_temp_after: float
    water_temp_before: float
    water_temp_after: float

    @classmethod
    def from_chiller_data(cls, chiller: Chiller):
        if chiller is None:
            return
        return cls(
            oil_temp_after=chiller.oil_temp.temperature_after,
            oil_temp_before=chiller.oil_temp.temperature_before,
            water_temp_after=chiller.water_temp.temperature_after,
            water_temp_before=chiller.water_temp.temperature_before
        )


@dataclass
class GraphData:
    moment: datetime
    bearings_data: list[BearingGraphData]
    oil_data: OilSystem
    electricity_data: MainGearing
    gas_manifold_data: GasManifold
    chiller_data: ChillerGraphData


@dataclass
class SingleExhausterData:
    moment: datetime
    bearings_data: ExhausterInfo | None = None
    oil_data: OilSystem | None = None
    electricity_data: MainGearing | None = None
    chiller_data: Chiller | None = None
    gas_valve_data: ValvePosition | None = None
    gas_manifold_data: GasManifold | None = None

    def get_graphs_data(self):
        return GraphData(
            moment=self.moment,
            bearings_data=[
                BearingGraphData.from_bearing_data(bearing)
                for bearing in self.bearings_data.bearings
            ],
            oil_data=self.oil_data,
            electricity_data=self.electricity_data,
            gas_manifold_data=self.gas_manifold_data,
            chiller_data=ChillerGraphData.from_chiller_data(self.chiller_data)
        )


@dataclass
class ExhaustersData:
    moment: datetime
    bearings_data: list[ExhausterInfo] = None
    oil_data: list[OilSystem] = None
    electricity_data: list[MainGearing] = None
    chiller_data: list[Chiller] = None
    gas_valve_data: list[ValvePosition] = None
    gas_manifold_data: list[GasManifold] = None

    def get_single_exhauster_data(self, index: int):
        return SingleExhausterData(
            moment=self.moment,
            bearings_data=self.bearings_data[index],
            oil_data=self.oil_data[index],
            electricity_data=self.electricity_data[index],
            chiller_data=self.chiller_data[index],
            gas_valve_data=self.gas_valve_data[index],
            gas_manifold_data=self.gas_manifold_data[index],
        )
