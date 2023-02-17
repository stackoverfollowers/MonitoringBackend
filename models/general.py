import datetime

import pydantic


class Bearing(pydantic.BaseModel):
    index: int
    is_warning: bool
    is_alarm: bool


class Exhauster(pydantic.BaseModel):
    title: str
    is_work: bool
    rotor_title: str
    date_last_change: datetime.datetime
    days_last_change: int
    days_forecast: int
    forecast_warning: bool
    forecast_alarm: bool
    bearings: list[Bearing]
    oil_level: float
    oil_pressure: float


class SinterMachine(pydantic.BaseModel):
    exhausters: list[Exhauster]


class GeneralPageResponse(pydantic.BaseModel):
    sinter_machines: list[SinterMachine]
