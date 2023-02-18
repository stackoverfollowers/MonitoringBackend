import datetime

import pydantic


class ExEvent(pydantic.BaseModel):
    timestamp: float
    exhauster_index: int
    exhauster_title: str
    bearing_index: int


class ExEventResponse(pydantic.BaseModel):
    events: list[ExEvent]
