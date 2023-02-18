import datetime
from typing import Optional

import pydantic


class BearingExhausterResponse(pydantic.BaseModel):
    index: int
    temperature: float
    temp_status: str
    axial_vibration: Optional[float] = None
    axial_vibration_status: str
    horizontal_vibration: Optional[float] = None
    hor_vibration_status: str
    vertical_vibration: Optional[float] = None
    vert_vibration_status: str


class ExhausterInfoResponse(pydantic.BaseModel):
    title: str
    is_work: bool
    rotor_title: str

    bearings: list[BearingExhausterResponse]

    oil_level: float
    oil_level_status: str

    oil_pressure: float
    oil_pressure_status: str

    rotor_current: float
    rotor_current_status: str
    stator_current: int
    stator_current_status: str
    rotor_voltage: int
    stator_voltage: int

    oil_temp_before: float
    oil_temp_before_status: str
    oil_temp_after: float
    oil_temp_after_status: str
    water_temp_before: float
    water_temp_before_status: str
    water_temp_after: float
    water_temp_after_status: str

    gas_valve_open: bool
    gas_valve_closed: bool
    gas_valve_position: float

    gas_temp_before: float
    gas_underpressure_before: float
