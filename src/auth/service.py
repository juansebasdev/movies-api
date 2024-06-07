import requests
from src.auth.models import User
from src.database import NoSQLDatabase, SQLDatabase
from src.config import (
    DATA_REPOSITORY,
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    HOST,
    PORT,
)


class GoogleAuthenticator:
    TOKEN_URL = "https://accounts.google.com/o/oauth2/token"

    def __init__(self, code: str) -> None:
        self.config_data = {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "redirect_uri": f"http://{HOST}:{PORT}/auth/callback",
            "code": code,
        }

    def authenticate(self):
        response = requests.post(self.TOKEN_URL, data=self.config_data)
        id_token = response.json().get("id_token")
        refresh_token = response.json().get("refresh_token")
        return {"id_token": id_token, "refresh_token": refresh_token}


class UserService:
    def __init__(self) -> None:
        if DATA_REPOSITORY == "NOSQL":
            from src.nosql_repository import NoSQLRepository

            self.repo = NoSQLRepository(NoSQLDatabase(), "users", User)
        else:
            from src.sql_repository import SQLRepository

            self.repo = SQLRepository(SQLDatabase(), User)

    def create_user(self, email: str) -> None:
        data = {"email": email, "is_active": True}
        self.repo.create(data)

    def get_user_by_email(self, email: str) -> User:
        return self.repo.get(filters={"email": email})

    def user_exists(self, email: str) -> bool:
        user = self.repo.get(filters={"email": email})
        return True if user else False
