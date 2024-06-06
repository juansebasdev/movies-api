from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi_pagination import paginate
from fastapi_pagination.links import Page

from src.auth.utils import JWTBearer, OptionalJWTBearer
from src.movies.config import ERRORS
from src.movies.schemas import MovieCreate, MovieListPublic, MovieListUser
from src.movies.service import MovieService
from src.movies.utils import get_user


router = APIRouter()


@router.post("", tags=["movies"], response_model=MovieListUser, status_code=status.HTTP_201_CREATED)
async def create_movie(
    movie: MovieCreate = Body(...), credentials: dict = Depends(JWTBearer())
):
    user = get_user(credentials)
    movie_service = MovieService()
    movie = movie_service.create_movie(movie, user.id)
    return movie


@router.get("", response_model=Page[MovieListPublic], tags=["movies"])
async def get_movies():
    movies = MovieService().get_all_movies()
    return paginate(movies)


@router.get("/me", tags=["movies"], response_model=Page[MovieListUser])
async def get_user_movies(credentials: dict = Depends(JWTBearer())):
    user = get_user(credentials)
    return paginate(user.movies)


@router.get("/{movie_id}", tags=["movies"], response_model=MovieListPublic)
async def get_movie(movie_id: int, credentials: dict = Depends(OptionalJWTBearer())):
    movie = MovieService().get_movie(movie_id)
    if movie.is_public is False:
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ERRORS["NOT_AUTHORIZED"],
            )
        user = get_user(credentials)
        if movie.owner is not user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=ERRORS["FORBIDDEN"],
            )
    return movie


@router.patch("/{movie_id}", tags=["movies"], response_model=MovieListUser)
async def update_movie(
    movie_id: int,
    movie: MovieCreate = Body(...),
    credentials: dict = Depends(JWTBearer()),
):
    user = get_user(credentials)
    movie_service = MovieService()
    movie = movie_service.update_movie(movie_id, movie, user.id)
    return movie
