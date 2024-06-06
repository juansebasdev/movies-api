import requests
from fastapi import HTTPException, status

from src.wtapi.exceptions import NotFound


class WTClient:
    URL = "http://worldtimeapi.org/api/timezone"

    def __init__(self, area, location, region=None):
        self.area = area
        self.location = location
        self.region = region

    def get_time(self):
        url = f"{self.URL}/{self.area}/{self.location}"
        if self.region:
            url = f"{url}/{self.region}"
        try:
            response = requests.get(url)
            if response.status_code == 404:
                raise NotFound(detail=response.json()["error"])
            return response.json()
        except NotFound as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
