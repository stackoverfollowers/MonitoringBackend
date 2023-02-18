import datetime
from typing import Optional

import pydantic


class BearingExhausterResponse(pydantic.BaseModel):
    index: int
    temperature: float
    temp_status: str
    axial_vibration: Optional[float] = None
    horizontal_vibration: Optional[float] = None
    vertical_vibration: Optional[float] = None


class ExhausterInfoResponse(pydantic.BaseModel):
    bearings: list[BearingExhausterResponse]

    oil_level: float
    oil_pressure: float

    rotor_current: float
    stator_current: float
    rotor_voltage: float
    stator_voltage: float

    oil_temp_before: float
    oil_temp_after: float
    water_temp_before: float
    water_temp_after: float

    gas_valve_open: bool
    gas_valve_closed: bool
    gas_valve_position: float

    gas_temp_before: float
    gas_underpressure_before: float
