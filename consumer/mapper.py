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
    ExhausterPreMapInfo,
    ExhausterInfo,
)


class ExMapper:
    def __init__(self, exhauster_data: dict):
        self.data = exhauster_data
        self.ex_prefix = "SM_Exgauster\\"
        self.moment = datetime.fromisoformat(self.data["moment"])

    def _signals_iter(self) -> Iterator[tuple[int, int, float]]:
        for key, value in self.data.items():
            key_data = key.lstrip(self.ex_prefix)
            if key_data == "moment":
                continue
            if "." in key_data:
                continue
            first_key, second_key = map(
                int, key_data.replace("[", "").replace("]", "").split(":")
            )
            yield first_key, second_key, float(value)

    def _get_index(self, attr_name: str, key: int, items: ExhausterPreMapInfo):
        "эээ"
        index = getattr(items, attr_name).index(key)
        if index >= 2:
            index += 4
        return index

    def map_bearings(self) -> list[ExhausterInfo]:
        exhauster_infos = [
            ExhausterPreMapInfo(
                exhauster_name="У-171",
                rotor_index=22,
                exhauster_pre_index=2,
                temperatures=[27, 28, 29, 30, 31, 32, 33, 34, 35],
                alarm_maxes=list(range(65, 73 + 1)),
                alarm_mins=list(range(74, 82 + 1)),
                warning_maxes=list(range(83, 91 + 1)),
                warning_mins=list(range(92, 100 + 1)),
                axial_vibrations=list(range(2, 11 + 1, 3)),
                axial_vibrations_alarm_maxes=list(range(139, 148 + 1, 3)),
                axial_vibrations_alarm_mins=list(range(151, 160 + 1, 3)),
                axial_vibrations_warning_maxes=list(range(163, 172 + 1, 3)),
                axial_vibrations_warning_mins=list(range(175, 184 + 1, 3)),
                horizontal_vibration=list(range(0, 9 + 1, 3)),
                horizontal_vibration_alarm_maxes=list(range(137, 146 + 1, 3)),
                horizontal_vibration_alarm_mins=list(range(149, 158 + 1, 3)),
                horizontal_vibration_warning_maxes=list(range(161, 170 + 1, 3)),
                horizontal_vibration_warning_mins=list(range(173, 182 + 1, 3)),
                vertical_vibration=list(range(1, 10 + 1, 3)),
                vertical_vibration_alarm_maxes=list(range(138, 147 + 1, 3)),
                vertical_vibration_alarm_mins=list(range(150, 159 + 1, 3)),
                vertical_vibration_warning_maxes=list(range(162, 171 + 1, 3)),
                vertical_vibration_warning_mins=list(range(174, 183 + 1, 3)),
            ),
            ExhausterPreMapInfo(
                exhauster_name="У-172",
                rotor_index=29,
                exhauster_pre_index=2,
                temperatures=[43, 44, 45, 47, 48, 49, 50, 51, 52],
                alarm_maxes=list(range(101, 109 + 1)),
                alarm_mins=list(range(110, 118 + 1)),
                warning_maxes=list(range(119, 127 + 1)),
                warning_mins=list(range(128, 136 + 1)),
                axial_vibrations=list(range(14, 23 + 1, 3)),
                axial_vibrations_alarm_maxes=list(range(187, 196 + 1, 3)),
                axial_vibrations_alarm_mins=list(range(199, 208 + 1, 3)),
                axial_vibrations_warning_maxes=list(range(211, 220 + 1, 3)),
                axial_vibrations_warning_mins=list(range(223, 232 + 1, 3)),
                horizontal_vibration=list(range(12, 21 + 1, 3)),
                horizontal_vibration_alarm_maxes=list(range(185, 194 + 1, 3)),
                horizontal_vibration_alarm_mins=list(range(197, 206 + 1, 3)),
                horizontal_vibration_warning_maxes=list(range(209, 218 + 1, 3)),
                horizontal_vibration_warning_mins=list(range(221, 230 + 1, 3)),
                vertical_vibration=list(range(13, 22 + 1, 3)),
                vertical_vibration_alarm_maxes=list(range(186, 195 + 1, 3)),
                vertical_vibration_alarm_mins=list(range(198, 207 + 1, 3)),
                vertical_vibration_warning_maxes=list(range(210, 219 + 1, 3)),
                vertical_vibration_warning_mins=list(range(222, 231 + 1, 3)),
            ),
            ExhausterPreMapInfo(
                exhauster_name="Ф-171",
                rotor_index=37,
                exhauster_pre_index=0,
                temperatures=[27, 28, 29, 30, 31, 32, 33, 34, 35],
                alarm_maxes=list(range(63, 71 + 1)),
                alarm_mins=list(range(72, 80 + 1)),
                warning_maxes=list(range(81, 89 + 1)),
                warning_mins=list(range(90, 98 + 1)),
                axial_vibrations=list(range(2, 11 + 1, 3)),
                axial_vibrations_alarm_maxes=list(range(137, 146 + 1, 3)),
                axial_vibrations_alarm_mins=list(range(149, 158 + 1, 3)),
                axial_vibrations_warning_maxes=list(range(161, 170 + 1, 3)),
                axial_vibrations_warning_mins=list(range(173, 182 + 1, 3)),
                horizontal_vibration=list(range(0, 9 + 1, 3)),
                horizontal_vibration_alarm_maxes=list(range(135, 144 + 1, 3)),
                horizontal_vibration_alarm_mins=list(range(147, 156 + 1, 3)),
                horizontal_vibration_warning_maxes=list(range(159, 168 + 1, 3)),
                horizontal_vibration_warning_mins=list(range(171, 180 + 1, 3)),
                vertical_vibration=list(range(1, 10 + 1, 3)),
                vertical_vibration_alarm_maxes=list(range(136, 145 + 1, 3)),
                vertical_vibration_alarm_mins=list(range(148, 157 + 1, 3)),
                vertical_vibration_warning_maxes=list(range(160, 169 + 1, 3)),
                vertical_vibration_warning_mins=list(range(172, 181 + 1, 3)),
            ),
            ExhausterPreMapInfo(
                exhauster_name="Ф-172",
                rotor_index=27,
                exhauster_pre_index=0,
                temperatures=[43, 44, 45, 47, 48, 49, 50, 51, 52],
                alarm_maxes=list(range(99, 107 + 1)),
                alarm_mins=list(range(108, 116 + 1)),
                warning_maxes=list(range(117, 125 + 1)),
                warning_mins=list(range(126, 134 + 1)),
                axial_vibrations=list(range(14, 23 + 1, 3)),
                axial_vibrations_alarm_maxes=list(range(185, 194 + 1, 3)),
                axial_vibrations_alarm_mins=list(range(197, 206 + 1, 3)),
                axial_vibrations_warning_maxes=list(range(209, 218 + 1, 3)),
                axial_vibrations_warning_mins=list(range(221, 230 + 1, 3)),
                horizontal_vibration=list(range(12, 21 + 1, 3)),
                horizontal_vibration_alarm_maxes=list(range(183, 192 + 1, 3)),
                horizontal_vibration_alarm_mins=list(range(195, 204 + 1, 3)),
                horizontal_vibration_warning_maxes=list(range(207, 216 + 1, 3)),
                horizontal_vibration_warning_mins=list(range(219, 228 + 1, 3)),
                vertical_vibration=list(range(13, 22 + 1, 3)),
                vertical_vibration_alarm_maxes=list(range(184, 193 + 1, 3)),
                vertical_vibration_alarm_mins=list(range(196, 205 + 1, 3)),
                vertical_vibration_warning_maxes=list(range(208, 217 + 1, 3)),
                vertical_vibration_warning_mins=list(range(220, 229 + 1, 3)),
            ),
            ExhausterPreMapInfo(
                exhauster_name="Х-171",
                rotor_index=39,
                exhauster_pre_index=3,
                temperatures=[27, 28, 29, 30, 31, 32, 33, 34, 35],
                alarm_maxes=list(range(63, 71 + 1)),
                alarm_mins=list(range(72, 80 + 1)),
                warning_maxes=list(range(81, 89 + 1)),
                warning_mins=list(range(90, 98 + 1)),
                axial_vibrations=list(range(2, 11 + 1, 3)),
                axial_vibrations_alarm_maxes=list(range(137, 146 + 1, 3)),
                axial_vibrations_alarm_mins=list(range(149, 158 + 1, 3)),
                axial_vibrations_warning_maxes=list(range(161, 170 + 1, 3)),
                axial_vibrations_warning_mins=list(range(173, 182 + 1, 3)),
                horizontal_vibration=list(range(0, 9 + 1, 3)),
                horizontal_vibration_alarm_maxes=list(range(135, 144 + 1, 3)),
                horizontal_vibration_alarm_mins=list(range(147, 156 + 1, 3)),
                horizontal_vibration_warning_maxes=list(range(159, 168 + 1, 3)),
                horizontal_vibration_warning_mins=list(range(171, 180 + 1, 3)),
                vertical_vibration=list(range(1, 10 + 1, 3)),
                vertical_vibration_alarm_maxes=list(range(136, 145 + 1, 3)),
                vertical_vibration_alarm_mins=list(range(148, 157 + 1, 3)),
                vertical_vibration_warning_maxes=list(range(160, 169 + 1, 3)),
                vertical_vibration_warning_mins=list(range(172, 181 + 1, 3)),
            ),
            ExhausterPreMapInfo(
                exhauster_name="Х-172",
                rotor_index=45,
                exhauster_pre_index=3,
                temperatures=[43, 44, 45, 47, 48, 49, 50, 51, 52],
                alarm_maxes=list(range(99, 107 + 1)),
                alarm_mins=list(range(108, 116 + 1)),
                warning_maxes=list(range(117, 125 + 1)),
                warning_mins=list(range(126, 134 + 1)),
                axial_vibrations=list(range(14, 23 + 1, 3)),
                axial_vibrations_alarm_maxes=list(range(185, 194 + 1, 3)),
                axial_vibrations_alarm_mins=list(range(197, 206 + 1, 3)),
                axial_vibrations_warning_maxes=list(range(209, 218 + 1, 3)),
                axial_vibrations_warning_mins=list(range(221, 230 + 1, 3)),
                horizontal_vibration=list(range(12, 21 + 1, 3)),
                horizontal_vibration_alarm_maxes=list(range(183, 192 + 1, 3)),
                horizontal_vibration_alarm_mins=list(range(195, 204 + 1, 3)),
                horizontal_vibration_warning_maxes=list(range(207, 216 + 1, 3)),
                horizontal_vibration_warning_mins=list(range(219, 228 + 1, 3)),
                vertical_vibration=list(range(13, 22 + 1, 3)),
                vertical_vibration_alarm_maxes=list(range(184, 193 + 1, 3)),
                vertical_vibration_alarm_mins=list(range(196, 205 + 1, 3)),
                vertical_vibration_warning_maxes=list(range(208, 217 + 1, 3)),
                vertical_vibration_warning_mins=list(range(220, 229 + 1, 3)),
            ),
        ]

        exhausters_parsed = [
            ExhausterInfo(
                exhauster_name=exhauster.exhauster_name,
                rotor_index=exhauster.rotor_index,
            )
            for exhauster in exhauster_infos
        ]
        # сначала созадем просто все подшипники потом туда суем дату
        for first_key, second_key, value in self._signals_iter():
            for exhauster in exhauster_infos:
                if first_key != exhauster.exhauster_pre_index:
                    continue
                if second_key in exhauster.temperatures:
                    parsed_exhauster: ExhausterInfo = list(
                        filter(
                            lambda x: x.exhauster_name == exhauster.exhauster_name,
                            exhausters_parsed,
                        )
                    )[0]
                    parsed_exhauster.bearings.append(
                        Bearing(
                            temps=Temps(temp=value, setting_temp=SettingStats()),
                            index=list(exhauster.temperatures).index(second_key) + 1,
                        )
                    )

        for first_key, second_key, value in self._signals_iter():
            for exhauster in filter(
                lambda x: x.exhauster_pre_index == first_key, exhauster_infos
            ):
                parsed_exhauster: ExhausterInfo = list(
                    filter(
                        lambda x: x.exhauster_name == exhauster.exhauster_name,
                        exhausters_parsed,
                    )
                )[0]
                if second_key in exhauster.alarm_maxes:
                    parsed_exhauster.bearings[
                        exhauster.alarm_maxes.index(second_key)
                    ].temps.setting_temp.alarm_max = value
                elif second_key in exhauster.alarm_mins:
                    parsed_exhauster.bearings[
                        exhauster.alarm_mins.index(second_key)
                    ].temps.setting_temp.alarm_min = value
                elif second_key in exhauster.warning_maxes:
                    parsed_exhauster.bearings[
                        exhauster.warning_maxes.index(second_key)
                    ].temps.setting_temp.warning_max = value
                elif second_key in exhauster.warning_mins:
                    parsed_exhauster.bearings[
                        exhauster.warning_mins.index(second_key)
                    ].temps.setting_temp.warning_min = value
                # elif эээ ээээ ну ээээ:
                #     continue
                elif second_key in exhauster.horizontal_vibration:
                    parsed_exhauster.bearings[
                        self._get_index("horizontal_vibration", second_key, exhauster)
                    ].vibration = Vibration(horizontal_vibration=value)
                elif second_key in exhauster.horizontal_vibration_alarm_maxes:
                    parsed_exhauster.bearings[
                        self._get_index(
                            "horizontal_vibration_alarm_maxes", second_key, exhauster
                        )
                    ].vibration.horizontal_vibration_stats = SettingStats(
                        alarm_max=value
                    )
                elif second_key in exhauster.horizontal_vibration_alarm_mins:
                    parsed_exhauster.bearings[
                        self._get_index(
                            "horizontal_vibration_alarm_mins", second_key, exhauster
                        )
                    ].vibration.horizontal_vibration_stats.alarm_min = value
                elif second_key in exhauster.horizontal_vibration_warning_maxes:
                    parsed_exhauster.bearings[
                        self._get_index(
                            "horizontal_vibration_warning_maxes", second_key, exhauster
                        )
                    ].vibration.horizontal_vibration_stats.warning_max = value
                elif second_key in exhauster.horizontal_vibration_warning_mins:
                    parsed_exhauster.bearings[
                        self._get_index(
                            "horizontal_vibration_warning_mins", second_key, exhauster
                        )
                    ].vibration.horizontal_vibration_stats.warning_min = value

                elif second_key in exhauster.vertical_vibration:
                    parsed_exhauster.bearings[
                        self._get_index("vertical_vibration", second_key, exhauster)
                    ].vibration.vertical_vibration = value
                elif second_key in exhauster.vertical_vibration_alarm_maxes:
                    parsed_exhauster.bearings[
                        self._get_index(
                            "vertical_vibration_alarm_maxes", second_key, exhauster
                        )
                    ].vibration.vertical_vibration_stats = SettingStats(alarm_max=value)
                elif second_key in exhauster.vertical_vibration_alarm_mins:
                    parsed_exhauster.bearings[
                        self._get_index(
                            "vertical_vibration_alarm_mins", second_key, exhauster
                        )
                    ].vibration.vertical_vibration_stats.alarm_min = value
                elif second_key in exhauster.vertical_vibration_warning_maxes:
                    parsed_exhauster.bearings[
                        self._get_index(
                            "vertical_vibration_warning_maxes", second_key, exhauster
                        )
                    ].vibration.vertical_vibration_stats.warning_max = value
                elif second_key in exhauster.vertical_vibration_warning_mins:
                    parsed_exhauster.bearings[
                        self._get_index(
                            "vertical_vibration_warning_mins", second_key, exhauster
                        )
                    ].vibration.vertical_vibration_stats.warning_min = value

                elif second_key in exhauster.axial_vibrations:
                    parsed_exhauster.bearings[
                        self._get_index("axial_vibrations", second_key, exhauster)
                    ].vibration.axial_vibration = value
                elif second_key in exhauster.axial_vibrations_alarm_maxes:
                    parsed_exhauster.bearings[
                        self._get_index(
                            "axial_vibrations_alarm_maxes", second_key, exhauster
                        )
                    ].vibration.axial_vibration_stats = SettingStats(alarm_max=value)
                elif second_key in exhauster.axial_vibrations_alarm_mins:
                    parsed_exhauster.bearings[
                        self._get_index(
                            "axial_vibrations_alarm_mins", second_key, exhauster
                        )
                    ].vibration.axial_vibration_stats.alarm_min = value
                elif second_key in exhauster.axial_vibrations_warning_maxes:
                    parsed_exhauster.bearings[
                        self._get_index(
                            "axial_vibrations_warning_maxes", second_key, exhauster
                        )
                    ].vibration.axial_vibration_stats.warning_max = value
                elif second_key in exhauster.axial_vibrations_warning_mins:
                    parsed_exhauster.bearings[
                        self._get_index(
                            "axial_vibrations_warning_mins", second_key, exhauster
                        )
                    ].vibration.axial_vibration_stats.warning_min = value
        return exhausters_parsed

    def map_chillers(self) -> list[Chiller]:
        return [
            Chiller(
                oil_temp=MiniTemps(
                    temperature_after=self.data[f"{self.ex_prefix}[2:42]"],
                    temperature_before=self.data[f"{self.ex_prefix}[2:41]"],
                ),
                water_temp=MiniTemps(
                    temperature_after=self.data[f"{self.ex_prefix}[2:37]"],
                    temperature_before=self.data[f"{self.ex_prefix}[2:36]"],
                ),
            ),
            Chiller(
                oil_temp=MiniTemps(
                    temperature_after=self.data[f"{self.ex_prefix}[2:60]"],
                    temperature_before=self.data[f"{self.ex_prefix}[2:59]"],
                ),
                water_temp=MiniTemps(
                    temperature_after=self.data[f"{self.ex_prefix}[2:54]"],
                    temperature_before=self.data[f"{self.ex_prefix}[2:53]"],
                ),
            ),
            Chiller(
                oil_temp=MiniTemps(
                    temperature_after=self.data[f"{self.ex_prefix}[0:42]"],
                    temperature_before=self.data[f"{self.ex_prefix}[0:41]"],
                ),
                water_temp=MiniTemps(
                    temperature_after=self.data[f"{self.ex_prefix}[0:37]"],
                    temperature_before=self.data[f"{self.ex_prefix}[0:36]"],
                ),
            ),
            Chiller(
                oil_temp=MiniTemps(
                    temperature_after=self.data[f"{self.ex_prefix}[0:60]"],
                    temperature_before=self.data[f"{self.ex_prefix}[0:59]"],
                ),
                water_temp=MiniTemps(
                    temperature_after=self.data[f"{self.ex_prefix}[0:54]"],
                    temperature_before=self.data[f"{self.ex_prefix}[0:53]"],
                ),
            ),
            Chiller(
                oil_temp=MiniTemps(
                    temperature_after=self.data[f"{self.ex_prefix}[3:42]"],
                    temperature_before=self.data[f"{self.ex_prefix}[3:41]"],
                ),
                water_temp=MiniTemps(
                    temperature_after=self.data[f"{self.ex_prefix}[3:37]"],
                    temperature_before=self.data[f"{self.ex_prefix}[3:36]"],
                ),
            ),
            Chiller(
                oil_temp=MiniTemps(
                    temperature_after=self.data[f"{self.ex_prefix}[3:60]"],
                    temperature_before=self.data[f"{self.ex_prefix}[3:59]"],
                ),
                water_temp=MiniTemps(
                    temperature_after=self.data[f"{self.ex_prefix}[3:54]"],
                    temperature_before=self.data[f"{self.ex_prefix}[3:53]"],
                ),
            ),
        ]

    def map_gas_manifolds(self) -> list[GasManifold]:
        return [
            GasManifold(
                temperature_before=self.data[f"{self.ex_prefix}[2:24]"],
                underpressure_before=self.data[f"{self.ex_prefix}[2:61]"],
            ),
            GasManifold(
                temperature_before=self.data[f"{self.ex_prefix}[2:25]"],
                underpressure_before=self.data[f"{self.ex_prefix}[2:62]"],
            ),
            GasManifold(
                temperature_before=self.data[f"{self.ex_prefix}[0:24]"],
                underpressure_before=self.data[f"{self.ex_prefix}[0:61]"],
            ),
            GasManifold(
                temperature_before=self.data[f"{self.ex_prefix}[0:25]"],
                underpressure_before=self.data[f"{self.ex_prefix}[0:62]"],
            ),
            GasManifold(
                temperature_before=self.data[f"{self.ex_prefix}[3:24]"],
                underpressure_before=self.data[f"{self.ex_prefix}[3:61]"],
            ),
            GasManifold(
                temperature_before=self.data[f"{self.ex_prefix}[3:25]"],
                underpressure_before=self.data[f"{self.ex_prefix}[3:62]"],
            ),
        ]

    # todo: gas_valve_closed и gas_valve_open могут быть 1 одновременно
    def map_valves(self) -> list[ValvePosition]:
        return [
            ValvePosition(
                gas_valve_closed=self.data[f"{self.ex_prefix}[4.1]"] == 1,
                gas_valve_open=self.data[f"{self.ex_prefix}[4.2]"] == 1,
                gas_valve_position=self.data.get(f"{self.ex_prefix}[4:6]", 0.0),
            ),
            ValvePosition(
                gas_valve_closed=self.data[f"{self.ex_prefix}[4.6]"] == 1,
                gas_valve_open=self.data[f"{self.ex_prefix}[4.7]"] == 1,
                gas_valve_position=self.data.get(f"{self.ex_prefix}[4:13]", 0.0),
            ),
            ValvePosition(
                gas_valve_closed=self.data[f"{self.ex_prefix}[1.1]"] == 1,
                gas_valve_open=self.data[f"{self.ex_prefix}[1.2]"] == 1,
                gas_valve_position=self.data.get(f"{self.ex_prefix}[1:6]", 0.0),
            ),
            ValvePosition(
                gas_valve_closed=self.data[f"{self.ex_prefix}[1.6]"] == 1,
                gas_valve_open=self.data[f"{self.ex_prefix}[1.7]"] == 1,
                gas_valve_position=self.data.get(f"{self.ex_prefix}[1:13]", 0.0),
            ),
            ValvePosition(
                gas_valve_closed=self.data[f"{self.ex_prefix}[5.1]"] == 1,
                gas_valve_open=self.data[f"{self.ex_prefix}[5.2]"] == 1,
                gas_valve_position=self.data.get(f"{self.ex_prefix}[5:6]", 0.0),
            ),
            ValvePosition(
                gas_valve_closed=self.data[f"{self.ex_prefix}[5.6]"] == 1,
                gas_valve_open=self.data[f"{self.ex_prefix}[5.7]"] == 1,
                gas_valve_position=self.data.get(f"{self.ex_prefix}[5:13]", 0.0),
            ),
        ]

    def map_main_gearings(self) -> list[MainGearing]:
        return [
            MainGearing(
                rotor_current=self.data.get(f"{self.ex_prefix}[4:2]", 0.0),
                rotor_voltage=self.data.get(f"{self.ex_prefix}[4:4]", 0.0),
                stator_current=self.data.get(f"{self.ex_prefix}[4:3]", 0.0),
                stator_voltage=self.data.get(f"{self.ex_prefix}[4:5]", 0.0),
            ),
            MainGearing(
                rotor_current=self.data.get(f"{self.ex_prefix}[4:9]", 0.0),
                rotor_voltage=self.data.get(f"{self.ex_prefix}[4:11]", 0.0),
                stator_current=self.data.get(f"{self.ex_prefix}[4:10]", 0.0),
                stator_voltage=self.data.get(f"{self.ex_prefix}[4:12]", 0.0),
            ),
            MainGearing(
                rotor_current=self.data.get(f"{self.ex_prefix}[1:2]", 0.0),
                rotor_voltage=self.data.get(f"{self.ex_prefix}[1:4]", 0.0),
                stator_current=self.data.get(f"{self.ex_prefix}[1:3]", 0.0),
                stator_voltage=self.data.get(f"{self.ex_prefix}[1:5]", 0.0),
            ),
            MainGearing(
                rotor_current=self.data.get(f"{self.ex_prefix}[1:9]", 0.0),
                rotor_voltage=self.data.get(f"{self.ex_prefix}[1:11]", 0.0),
                stator_current=self.data.get(f"{self.ex_prefix}[1:10]", 0.0),
                stator_voltage=self.data.get(f"{self.ex_prefix}[1:12]", 0.0),
            ),
            MainGearing(
                rotor_current=self.data.get(f"{self.ex_prefix}[5:2]", 0.0),
                rotor_voltage=self.data.get(f"{self.ex_prefix}[5:4]", 0.0),
                stator_current=self.data.get(f"{self.ex_prefix}[5:3]", 0.0),
                stator_voltage=self.data.get(f"{self.ex_prefix}[5:5]", 0.0),
            ),
            MainGearing(
                rotor_current=self.data.get(f"{self.ex_prefix}[5:9]", 0.0),
                rotor_voltage=self.data.get(f"{self.ex_prefix}[5:11]", 0.0),
                stator_current=self.data.get(f"{self.ex_prefix}[5:10]", 0.0),
                stator_voltage=self.data.get(f"{self.ex_prefix}[5:12]", 0.0),
            ),
        ]

    def map_oil_systems(self) -> list[OilSystem]:
        return [
            OilSystem(
                oil_level=self.data[f"{self.ex_prefix}[4:0]"],
                oil_pressure=self.data[f"{self.ex_prefix}[4:1]"],
            ),
            OilSystem(
                oil_level=self.data[f"{self.ex_prefix}[4:7]"],
                oil_pressure=self.data[f"{self.ex_prefix}[4:8]"],
            ),
            OilSystem(
                oil_level=self.data[f"{self.ex_prefix}[1:0]"],
                oil_pressure=self.data[f"{self.ex_prefix}[1:1]"],
            ),
            OilSystem(
                oil_level=self.data[f"{self.ex_prefix}[1:7]"],
                oil_pressure=self.data[f"{self.ex_prefix}[1:8]"],
            ),
            OilSystem(
                oil_level=self.data[f"{self.ex_prefix}[5:0]"],
                oil_pressure=self.data[f"{self.ex_prefix}[5:1]"],
            ),
            OilSystem(
                oil_level=self.data[f"{self.ex_prefix}[5:7]"],
                oil_pressure=self.data[f"{self.ex_prefix}[5:8]"],
            ),
        ]

    def map_exhauster_works(self) -> list[ExhausterWork]:
        return [
            ExhausterWork(
                work=self.data[f"{self.ex_prefix}[2.0]"] == 1,
            ),
            ExhausterWork(
                work=self.data[f"{self.ex_prefix}[2.1]"] == 1,
            ),
            ExhausterWork(
                work=self.data[f"{self.ex_prefix}[0.0]"] == 1,
            ),
            ExhausterWork(
                work=self.data[f"{self.ex_prefix}[0.1]"] == 1,
            ),
            ExhausterWork(
                work=self.data[f"{self.ex_prefix}[3.0]"] == 1,
            ),
            ExhausterWork(
                work=self.data[f"{self.ex_prefix}[3.1]"] == 1,
            ),
        ]


if __name__ == "__main__":
    import json

    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    mapper = ExMapper(exhauster_data=data)
    exhausters = mapper.map_bearings()
    for b in exhausters[0].bearings:
        print(b)
