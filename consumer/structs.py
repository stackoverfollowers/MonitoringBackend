from dataclasses import dataclass, field


@dataclass
class SettingStats:
    alarm_max: float = None
    alarm_min: float = None
    warning_max: float = None
    warning_min: float = None


@dataclass
class Temps:
    temp: float
    setting_temp: SettingStats = None


@dataclass
class Vibration:
    axial_vibration: float = None
    axial_vibration_stats: SettingStats = None
    horizontal_vibration: float = None
    horizontal_vibration_stats: SettingStats = None
    vertical_vibration: float = None
    vertical_vibration_stats: SettingStats = None


@dataclass
class Bearing:
    index: int
    temps: Temps = None
    vibration: Vibration | None = None


@dataclass
class MiniTemps:
    temperature_after: float
    temperature_before: float


@dataclass
class Chiller:
    oil_temp: MiniTemps
    water_temp: MiniTemps


@dataclass
class GasManifold:
    temperature_before: float
    underpressure_before: float


@dataclass
class ValvePosition:
    gas_valve_closed: bool
    gas_valve_open: bool
    gas_valve_position: float


@dataclass
class MainGearing:
    rotor_current: float
    rotor_voltage: float
    stator_current: float
    stator_voltage: float


@dataclass
class OilSystem:
    oil_level: float
    oil_pressure: float


@dataclass
class ExhausterWork:
    work: bool


@dataclass
class ExhausterPreMapInfo:
    exhauster_name: str
    rotor_index: int
    exhauster_pre_index: int

    temperatures: list

    alarm_maxes: list
    alarm_mins: list
    warning_maxes: list
    warning_mins: list

    axial_vibrations: list
    axial_vibrations_alarm_maxes: list
    axial_vibrations_alarm_mins: list
    axial_vibrations_warning_maxes: list
    axial_vibrations_warning_mins: list

    horizontal_vibration: list
    horizontal_vibration_alarm_maxes: list
    horizontal_vibration_alarm_mins: list
    horizontal_vibration_warning_maxes: list
    horizontal_vibration_warning_mins: list

    vertical_vibration: list
    vertical_vibration_alarm_maxes: list
    vertical_vibration_alarm_mins: list
    vertical_vibration_warning_maxes: list
    vertical_vibration_warning_mins: list


@dataclass
class ExhausterInfo:
    exhauster_name: str
    rotor_index: int
    bearings: list[Bearing] = field(default_factory=list)
