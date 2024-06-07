from typing import Optional, Union
from pydantic import BaseModel


class MovieBase(BaseModel):
    title: str
    description: str
    director: str
    year: int
    genre: str
    rating: float
    broadcast: Optional[str] = None
    area_location: Optional[str] = None
    localtime: Optional[str] = None
    utc_datetime: Optional[str] = None
    utc_offset: Optional[str] = None

    class Config:
        allow_population_by_field_name = True


class MovieCreate(MovieBase):
    is_public: bool

    class Config:
        json_schema_extra = {
            "example": {
                "title": "The Shawshank Redemption",
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                "director": "Frank Darabont",
                "year": 1994,
                "genre": "Drama",
                "rating": 9.3,
                "is_public": True,
                "broadcast": "Netflix",
                "area_location": "America/Santiago",
                "localtime": "2021-08-01 20:00:00",
            }
        }


class MovieListPublic(MovieBase):
    id: Union[int, str]


class MovieListUser(MovieListPublic):
    is_public: bool
