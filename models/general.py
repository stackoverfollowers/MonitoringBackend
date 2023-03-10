import datetime
from typing import Optional

import pydantic


class BearingResponse(pydantic.BaseModel):
    index: int
    is_temp_warning: bool
    is_temp_alarm: bool

    is_vibration_warning: Optional[bool] = None
    is_vibration_alarm: Optional[bool] = None
    vibration_status: str
    temp_status: str


class Exhauster(pydantic.BaseModel):
    index: int
    title: str
    is_work: bool
    rotor_title: str
    date_last_change: datetime.datetime
    days_last_change: int
    days_forecast: int
    forecast_warning: bool
    forecast_alarm: bool
    bearings: list[BearingResponse]
    oil_level: float
    oil_pressure: float


class SinterMachine(pydantic.BaseModel):
    exhausters: list[Exhauster]


class GeneralPageResponse(pydantic.BaseModel):
    sinter_machines: list[SinterMachine]
