from fastapi import HTTPException, status

from src.database import ConfigDatabase
from src.movies.config import ERRORS
from src.movies.models import Movie
from src.movies.schemas import MovieCreate


class MovieService:
    def __init__(self):
        self.db = ConfigDatabase()

    def create_movie(self, movie: MovieCreate, user_id: int):
        movie = Movie(**movie.model_dump(), owner_id=user_id)
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
