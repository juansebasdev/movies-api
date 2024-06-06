from src.auth.service import UserService
from src.auth.utils import UserExtractor


def get_user(credentials):
    user_extractor = UserExtractor(credentials)
    user_service = UserService()
    user = user_service.get_user_by_email(user_extractor.get_email())
    return user
