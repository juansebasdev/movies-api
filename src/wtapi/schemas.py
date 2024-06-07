from pydantic import BaseModel


class WTResponse(BaseModel):
    datetime: str
    utc_datetime: str
    utc_offset: str
