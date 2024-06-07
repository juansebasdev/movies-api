from typing import Union
from fastapi import HTTPException, status

from src.config import DATA_REPOSITORY
from src.database import NoSQLDatabase, SQLDatabase
from src.movies.config import ERRORS
from src.movies.models import Movie
from src.movies.schemas import MovieCreate
from src.movies.utils import set_broadcast_data


class MovieService:
    def __init__(self):
        if DATA_REPOSITORY == "NOSQL":
            from src.nosql_repository import NoSQLRepository
            self.repo = NoSQLRepository(NoSQLDatabase(), "movies", Movie)
        else:
            from src.sql_repository import SQLRepository
            self.repo = SQLRepository(SQLDatabase(), Movie)

    def create_movie(self, movie: MovieCreate, user_id: int):
        data = movie.model_dump()
        data["owner_id"] = user_id
        data = set_broadcast_data(data)
        movie = self.repo.create(data)
        return movie

    def get_all_movies(self):
        return self.repo.get_all(filters={"is_public": True})
    
    def get_all_movies_for_user(self, user_id: Union[int, str]):
        return self.repo.get_all_for_user(user_id)

    def get_movie(self, movie_id: Union[int, str]):
        movie = self.repo.get(id=movie_id)
        if not movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=ERRORS["NOT_FOUND"]
            )
        return movie

    def update_movie(self, movie_id: int, data: MovieCreate, user_id: int):
        movie = self.repo.get(id=movie_id)
        if movie:
            if str(movie.owner_id) != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=ERRORS["FORBIDDEN"],
                )
            data = data.model_dump()
            data = set_broadcast_data(data)
            for key, value in data.items():
                if value is None:
                    data[key] = movie.__dict__[key]
            movie = self.repo.update(movie_id, data)
            return movie
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ERRORS["NOT_FOUND"],
            )
