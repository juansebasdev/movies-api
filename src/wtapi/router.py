from typing import Optional
from fastapi import APIRouter, HTTPException, status

from src.wtapi.client import WTClient


router = APIRouter()


@router.get("", tags=["World Time API"])
async def time(area_location: str, region: Optional[str] = None):
    if "/" not in area_location:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid area/location format. Use area/location.",
        )
    area, location = area_location.split("/")
    client = WTClient(area, location, region)
    data_response = client.get_time()
    return {
        "datetime": data_response["datetime"],
        "utc_datetime": data_response["utc_datetime"],
        "utc_offset": data_response["utc_offset"],
    }
