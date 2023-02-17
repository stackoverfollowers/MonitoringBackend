from datetime import datetime
from typing import Iterator

from consumer.structs import (
    Bearing,
    Temps,
    SettingStats,
    MiniTemps,
    Chiller,
    GasManifold,
    ValvePosition,
    MainGearing,
    OilSystem,
    ExhausterWork,
    Vibration,
)


class ExMapper:
    def __init__(self, exhauster_data: dict):
        self.data = exhauster_data
        self.ex_prefix = "SM_Exgauster\\"
        self.bearing_prefix = 3

    def _bearings_iter(self) -> Iterator[tuple[int, int, float]]:
        for key, value in self.data.items():
            key_data = key.lstrip(self.ex_prefix)
            if "." in key_data:
                continue
            first_key, second_key = map(
                int, key_data.replace("[", "").replace("]", "").split(":")
            )
            if first_key != self.bearing_prefix:
                continue
            yield first_key, second_key, float(value)

    def map_bearings(self) -> list[Bearing]:
        temperatures = {43, 44, 45, 47, 48, 49, 50, 51, 52}

        alarm_maxes = list(range(99, 107 + 1))
        alarm_mins = list(range(108, 116 + 1))
        warning_maxes = list(range(117, 125 + 1))
        warning_mins = list(range(126, 134 + 1))

        axial_vibrations = list(range(14, 23 + 1, 3))
        axial_vibrations_alarm_maxes = list(range(185, 194 + 1, 3))
        axial_vibrations_alarm_mins = list(range(197, 206 + 1, 3))
        axial_vibrations_warning_maxes = list(range(209, 218 + 1, 3))
        axial_vibrations_warning_mins = list(range(221, 230 + 1, 3))

        horizontal_vibration = list(range(12, 21 + 1, 3))
        horizontal_vibration_alarm_maxes = list(range(183, 192 + 1, 3))
        horizontal_vibration_alarm_mins = list(range(195, 204 + 1, 3))
        horizontal_vibration_warning_maxes = list(range(207, 216 + 1, 3))
        horizontal_vibration_warning_mins = list(range(219, 228 + 1, 3))

        vertical_vibration = list(range(13, 22 + 1, 3))
        vertical_vibration_alarm_maxes = list(range(184, 193 + 1, 3))
        vertical_vibration_alarm_mins = list(range(196, 205 + 1, 3))
        vertical_vibration_warning_maxes = list(range(208, 217 + 1, 3))
        vertical_vibration_warning_mins = list(range(220, 229 + 1, 3))

        bearings = []
        moment = datetime.fromisoformat(self.data.pop("moment"))
        print(f"{moment=}")

        # сначала созадем просто все подшипники потом туда суем дату
        for first_key, second_key, value in self._bearings_iter():
            if second_key in temperatures:
                bearings.append(
                    Bearing(temps=Temps(temp=value, setting_temp=SettingStats()))
                )

        for first_key, second_key, value in self._bearings_iter():
            if second_key in alarm_maxes:
                bearings[
                    alarm_maxes.index(second_key)
                ].temps.setting_temp.alarm_max = value
            elif second_key in alarm_mins:
                bearings[
                    alarm_mins.index(second_key)
                ].temps.setting_temp.alarm_min = value
            elif second_key in warning_maxes:
                bearings[
                    warning_maxes.index(second_key)
                ].temps.setting_temp.warning_max = value
            elif second_key in warning_mins:
                bearings[
                    warning_mins.index(second_key)
                ].temps.setting_temp.warning_min = value

            elif second_key in horizontal_vibration:
                bearings[horizontal_vibration.index(second_key)].vibration = Vibration(
                    horizontal_vibration=value
                )
            elif second_key in horizontal_vibration_alarm_maxes:
                bearings[
                    horizontal_vibration_alarm_maxes.index(second_key)
                ].vibration.horizontal_vibration_stats = SettingStats(alarm_max=value)
            elif second_key in horizontal_vibration_alarm_mins:
                bearings[
                    horizontal_vibration_alarm_mins.index(second_key)
                ].vibration.horizontal_vibration_stats.alarm_min = value
            elif second_key in horizontal_vibration_warning_maxes:
                bearings[
                    horizontal_vibration_warning_maxes.index(second_key)
                ].vibration.horizontal_vibration_stats.warning_max = value
            elif second_key in horizontal_vibration_warning_mins:
                bearings[
                    horizontal_vibration_warning_mins.index(second_key)
                ].vibration.horizontal_vibration_stats.warning_min = value

            elif second_key in vertical_vibration:
                bearings[
                    vertical_vibration.index(second_key)
                ].vibration.vertical_vibration = value
            elif second_key in vertical_vibration_alarm_maxes:
                bearings[
                    vertical_vibration_alarm_maxes.index(second_key)
                ].vibration.vertical_vibration_stats = SettingStats(alarm_max=value)
            elif second_key in vertical_vibration_alarm_mins:
                bearings[
                    vertical_vibration_alarm_mins.index(second_key)
                ].vibration.vertical_vibration_stats.alarm_min = value
            elif second_key in vertical_vibration_warning_maxes:
                bearings[
                    vertical_vibration_warning_maxes.index(second_key)
                ].vibration.vertical_vibration_stats.warning_max = value
            elif second_key in vertical_vibration_warning_mins:
                bearings[
                    vertical_vibration_warning_mins.index(second_key)
                ].vibration.vertical_vibration_stats.warning_min = value

            elif second_key in axial_vibrations:
                bearings[
                    axial_vibrations.index(second_key)
                ].vibration.axial_vibration = value
            elif second_key in axial_vibrations_alarm_maxes:
                bearings[
                    axial_vibrations_alarm_maxes.index(second_key)
                ].vibration.axial_vibration_stats = SettingStats(alarm_max=value)
            elif second_key in axial_vibrations_alarm_mins:
                bearings[
                    axial_vibrations_alarm_mins.index(second_key)
                ].vibration.axial_vibration_stats.alarm_min = value
            elif second_key in axial_vibrations_warning_maxes:
                bearings[
                    axial_vibrations_warning_maxes.index(second_key)
                ].vibration.axial_vibration_stats.warning_max = value
            elif second_key in axial_vibrations_warning_mins:
                bearings[
                    axial_vibrations_warning_mins.index(second_key)
                ].vibration.axial_vibration_stats.warning_min = value

        return bearings

    def map_chiller(self) -> Chiller:
        return Chiller(
            oil_temp=MiniTemps(
                temperature_after=self.data[f"{self.ex_prefix}[3:60]"],
                temperature_before=self.data[f"{self.ex_prefix}[3:59]"],
            ),
            water_temp=MiniTemps(
                temperature_after=self.data[f"{self.ex_prefix}[3:54]"],
                temperature_before=self.data[f"{self.ex_prefix}[3:53]"],
            ),
        )

    def map_gas_manifold(self) -> GasManifold:
        return GasManifold(
            temperature_before=self.data[f"{self.ex_prefix}[3:25]"],
            underpressure_before=self.data[f"{self.ex_prefix}[3:62]"],
        )

    # todo: gas_valve_closed и gas_valve_open могут быть 1 одновременно
    def map_valve(self) -> ValvePosition:
        return ValvePosition(
            gas_valve_closed=self.data[f"{self.ex_prefix}[5.6]"] == 1,
            gas_valve_open=self.data[f"{self.ex_prefix}[5.7]"] == 1,
            gas_valve_position=self.data[f"{self.ex_prefix}[5:13]"],
        )

    def map_main_gearing(self) -> MainGearing:
        return MainGearing(
            rotor_current=self.data[f"{self.ex_prefix}[5:9]"],
            rotor_voltage=self.data[f"{self.ex_prefix}[5:11]"],
            stator_current=self.data[f"{self.ex_prefix}[5:10]"],
            stator_voltage=self.data[f"{self.ex_prefix}[5:12]"],
        )

    def map_oil_system(self) -> OilSystem:
        return OilSystem(
            oil_level=self.data[f"{self.ex_prefix}[5:7]"],
            oil_pressure=self.data[f"{self.ex_prefix}[5:8]"],
        )

    def map_exhauster_work(self) -> ExhausterWork:
        return ExhausterWork(
            work=self.data[f"{self.ex_prefix}[3.1]"] == 1,
        )
