from typing import Union
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi_pagination import paginate
from fastapi_pagination.links import Page

from src.auth.utils import JWTBearer
from src.decorators import is_authorized
from src.movies.config import ERRORS
from src.movies.schemas import MovieCreate, MovieListPublic, MovieListUser
from src.movies.service import MovieService
from src.movies.utils import get_user


router = APIRouter()


@router.post(
    "",
    tags=["Movies"],
    response_model=MovieListUser,
    status_code=status.HTTP_201_CREATED,
    description="Create a new movie, owned by current user",
)
@is_authorized
async def create_movie(
    movie: MovieCreate = Body(...), credentials: dict = Depends(JWTBearer())
):
    user = get_user(credentials)
    movie_service = MovieService()
    movie = movie_service.create_movie(movie, user.id)
    return movie


@router.get(
    "",
    response_model=Page[MovieListPublic],
    tags=["Movies"],
    description="Get all public movies",
)
async def get_movies():
    movies = MovieService().get_all_movies()
    return paginate(movies)


@router.get(
    "/me",
    tags=["Movies"],
    response_model=Page[MovieListUser],
    description="Get all movies owned by current user",
)
@is_authorized
async def get_user_movies(credentials: dict = Depends(JWTBearer())):
    user = get_user(credentials)
    movies = MovieService().get_all_movies_for_user(user.id)
    return paginate(movies)


@router.get(
    "/{movie_id}",
    tags=["Movies"],
    response_model=MovieListPublic,
    description="Get a movie by ID",
)
async def get_movie(
    movie_id: Union[int, str], credentials: dict = Depends(JWTBearer())
):
    movie = MovieService().get_movie(movie_id)
    if movie.is_public is False:
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ERRORS["NOT_AUTHORIZED"],
            )
        user = get_user(credentials)
        if movie.owner_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=ERRORS["FORBIDDEN"],
            )
    return movie


@router.patch(
    "/{movie_id}",
    tags=["Movies"],
    response_model=MovieListUser,
    description="Update a movie owned by current user",
)
@is_authorized
async def update_movie(
    movie_id: Union[int, str],
    movie: MovieCreate = Body(...),
    credentials: dict = Depends(JWTBearer()),
):
    user = get_user(credentials)
    movie_service = MovieService()
    movie = movie_service.update_movie(movie_id, movie, user.id)
    return movie
