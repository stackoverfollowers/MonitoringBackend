from dataclasses import dataclass


@dataclass
class SettingStats:
    alarm_max: float
    alarm_min: float
    warning_max: float
    warning_min: float


@dataclass
class Temps:
    temp: float
    setting_temp: SettingStats


@dataclass
class Vibration:
    axial_vibration: float
    axial_vibration_stats: SettingStats
    horizontal_vibration: float
    horizontal_vibration_stats: SettingStats
    vertical_vibration: float
    vertical_vibration_stats: SettingStats


@dataclass
class Bearing:
    temps: Temps
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
    gas_valve_closed: float
    gas_valve_open: float
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
    work: float
