from fastapi import HTTPException, status

from src.database import ConfigDatabase
from src.movies.config import ERRORS
from src.movies.models import Movie
from src.movies.schemas import MovieCreate
from src.wtapi.client import WTClient


class MovieService:
    def __init__(self):
        self.db = ConfigDatabase()

    def create_movie(self, movie: MovieCreate, user_id: int):
        data = movie.model_dump()
        movie = Movie(**data, owner_id=user_id)
        if data.get("broadcast") and data.get("area_location"):
            if '/' not in data["area_location"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=ERRORS["BAD_REQUEST"],
                )
            area, location = data["area_location"].split("/")
            wt_client = WTClient(area=area, location=location)
            movie.utc_offset = wt_client.get_time()["utc_offset"]
            movie.set_datetime_with_offset(data.get("localtime"), movie.utc_offset)
        self.db.session.add(movie)
        self.db.session.commit()
        return movie

    def get_all_movies(self):
        return self.db.session.query(Movie).filter(Movie.is_public).all()

    def get_movie(self, movie_id: int):
        movie = self.db.session.query(Movie).filter(Movie.id == movie_id).first()
        if not movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=ERRORS["NOT_FOUND"]
            )
        return movie

    def update_movie(self, movie_id: int, data: MovieCreate, user_id: int):
        movie = self.db.session.query(Movie).filter(Movie.id == movie_id).first()
        if movie:
            if movie.owner_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=ERRORS["FORBIDDEN"],
                )
            movie.title = data.title
            movie.description = data.description
            movie.director = data.director
            movie.year = data.year
            movie.genre = data.genre
            movie.rating = data.rating
            movie.is_public = data.is_public
            self.db.session.commit()
            return movie
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ERRORS["NOT_FOUND"],
            )
