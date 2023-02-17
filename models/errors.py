import pydantic


class Error(pydantic.BaseModel):
    status: int
    desc: str


class BaseError(pydantic.BaseModel):
    error: Error
