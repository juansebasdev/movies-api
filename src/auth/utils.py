import logging
from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from google.oauth2 import id_token
from google.auth.transport import requests
import jwt

from src.config import GOOGLE_CLIENT_SECRET


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer" or not JWTBearer.verify_jwt(
                credentials.credentials
            ):
                return None
            return credentials.credentials
        else:
            return None

    @staticmethod
    def verify_jwt(jwt_token: str) -> bool:
        try:
            _ = id_token.verify_oauth2_token(jwt_token, requests.Request())
            return True
        except Exception as e:
            logging.error(e)
            return False


class UserExtractor:
    def __init__(self, id_token: str) -> None:
        self.user_data = jwt.decode(
            id_token,
            GOOGLE_CLIENT_SECRET,
            algorithms=["RS256"],
            options={"verify_signature": False},
        )

    def get_email(self) -> str:
        return self.user_data.get("email")
