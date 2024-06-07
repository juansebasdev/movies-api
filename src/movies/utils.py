import pytz
from datetime import datetime
from fastapi import HTTPException, status

from src.auth.service import UserService
from src.auth.utils import UserExtractor
from src.movies.config import ERRORS
from src.wtapi.client import WTClient


def get_user(credentials):
    user_extractor = UserExtractor(credentials)
    user_service = UserService()
    user = user_service.get_user_by_email(user_extractor.get_email())
    return user

def set_broadcast_data(data):
    if data.get("broadcast") and data.get("area_location"):
        if "/" not in data["area_location"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ERRORS["BAD_REQUEST"],
            )
        area, location = data["area_location"].split("/")
        wt_client = WTClient(area=area, location=location)
        data["utc_offset"] = wt_client.get_time()["utc_offset"]
        data["localtime"], data["utc_datetime"] = set_datetime_with_offset(
            data["localtime"], data["utc_offset"]
        )
    return data

def set_datetime_with_offset(local_dt_str, utc_offset_str):
        localtime, utc_datetime = localize(local_dt_str, utc_offset_str)
        return localtime, utc_datetime

def localize(local_dt_str, utc_offset_str):
    local_dt = datetime.strptime(local_dt_str, "%Y-%m-%d %H:%M:%S")
    offset_hours, offset_minutes = map(int, utc_offset_str.split(':'))
    offset = pytz.FixedOffset(offset_hours * 60 + offset_minutes)
    local_dt = offset.localize(local_dt)
    utc_dt = local_dt.astimezone(pytz.utc)
    return local_dt.isoformat(), utc_dt.isoformat()