import logging
from fastapi import APIRouter, HTTPException


from src.auth.schemas import LoginResponse
from src.auth.service import GoogleAuthenticator, UserService
from src.auth.utils import UserExtractor
from src.config import GOOGLE_CLIENT_ID, HOST, PORT


router = APIRouter()


@router.get(
    "/login",
    tags=["Auth"],
    description="Returns the URL to login with Google",
    response_model=LoginResponse,
)
async def login():
    redirect_uri = f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri=http://{HOST}:{PORT}/auth/callback&scope=openid%20profile%20email&access_type=offline"
    return {"url": redirect_uri}


@router.get("/callback", tags=["Auth"], include_in_schema=False)
async def callback(code: str):
    try:
        authenticator = GoogleAuthenticator(code)
        response = authenticator.authenticate()
        google_user_extractor = UserExtractor(response.get("id_token"))
        email = google_user_extractor.get_email()
        user_service = UserService()
        if not user_service.user_exists(email):
            user_service.create_user(email)
        return response
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=400, detail="Failed to authorize access token")
