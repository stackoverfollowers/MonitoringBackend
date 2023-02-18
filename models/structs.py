from dataclasses import dataclass

from consumer.structs import (
    OilSystem,
    ExhausterInfo,
    MainGearing,
    Chiller,
    ValvePosition,
    GasManifold,
)


@dataclass
class SingleExhausterData:
    bearings_data: ExhausterInfo | None = None
    oil_data: OilSystem | None = None
    electricity_data: MainGearing | None = None
    chiller_data: Chiller | None = None
    gas_valve_data: ValvePosition | None = None
    gas_manifold_data: GasManifold | None = None


@dataclass
class ExhaustersData:
    bearings_data: list[ExhausterInfo] = None
    oil_data: list[OilSystem] = None
    electricity_data: list[MainGearing] = None
    chiller_data: list[Chiller] = None
    gas_valve_data: list[ValvePosition] = None
    gas_manifold_data: list[GasManifold] = None

    def get_single_exhauster_data(self, index: int):
        return SingleExhausterData(
            bearings_data=self.bearings_data[index],
            oil_data=self.oil_data[index],
            electricity_data=self.electricity_data[index],
            chiller_data=self.chiller_data[index],
            gas_valve_data=self.gas_valve_data[index],
            gas_manifold_data=self.gas_manifold_data[index],
        )
