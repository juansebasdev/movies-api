from pydantic import BaseModel


class LoginResponse(BaseModel):
    url: str
