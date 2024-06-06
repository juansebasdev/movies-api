from pydantic import BaseModel


class MovieBase(BaseModel):
    title: str
    description: str
    director: str
    year: int
    genre: str
    rating: float


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
            }
        }


class MovieListPublic(MovieBase):
    id: int


class MovieListUser(MovieListPublic):
    is_public: bool
