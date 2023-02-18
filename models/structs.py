from dataclasses import dataclass

from consumer.structs import OilSystem, ExhausterInfo, MainGearing, Chiller, ValvePosition, GasManifold


@dataclass
class SingleExhausterData:
    bearings_data: ExhausterInfo
    oil_data: OilSystem
    electricity_data: MainGearing
    chiller_data: Chiller
    gas_valve_data: ValvePosition
    gas_manifold_data: GasManifold


@dataclass
class ExhaustersData:
    bearings_data: list[ExhausterInfo]
    oil_data: list[OilSystem]
    electricity_data: list[MainGearing]
    chiller_data: list[Chiller]
    gas_valve_data: list[ValvePosition]
    gas_manifold_data: list[GasManifold]

    def get_single_exhauster_data(self, index: int):
        return SingleExhausterData(
            bearings_data=self.bearings_data[index],
            oil_data=self.oil_data[index],
            electricity_data=self.electricity_data[index],
            chiller_data=self.chiller_data[index],
            gas_valve_data=self.gas_valve_data[index],
            gas_manifold_data=self.gas_manifold_data[index],
        )