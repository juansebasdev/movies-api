from fastapi.testclient import TestClient
from unittest.mock import patch

from src.auth.models import User
from src.auth.utils import JWTBearer
from src.main import app
from src.movies.config import ERRORS
from src.movies.models import Movie

client = TestClient(app)


def override_verify_jwt(token: str) -> bool:
    return True  # Assume the token is always valid for testing


@patch.object(JWTBearer, "verify_jwt", override_verify_jwt)
def test_create_movie():
    headers = {"Authorization": "Bearer token"}
    with patch("src.movies.router.get_user") as mock_get_user:
        mock_get_user.return_value = User(id=1)
        with patch("src.movies.router.MovieService.create_movie") as mock_create_movie:
            mock_create_movie.return_value = {
                "id": 1,
                "title": "The Matrix",
                "description": "Welcome to the Real World",
                "director": "The Wachowskis",
                "year": 1999,
                "genre": "Science Fiction",
                "rating": 8.7,
                "is_public": False,
                "owner_id": 1,
                "created_at": "2021-08-31T00:00:00+00:00",
                "broadcast": None,
                "area_location": None,
                "utc_offset": None,
                "localtime": None,
                "utc_datetime": None,
            }
            response = client.post(
                "/movies/",
                headers=headers,
                json={
                    "title": "The Matrix",
                    "description": "Welcome to the Real World",
                    "director": "The Wachowskis",
                    "year": 1999,
                    "genre": "Science Fiction",
                    "rating": 8.7,
                    "is_public": False,
                },
            )
            assert response.status_code == 201
            assert response.json() == {
                "id": 1,
                "title": "The Matrix",
                "description": "Welcome to the Real World",
                "director": "The Wachowskis",
                "year": 1999,
                "genre": "Science Fiction",
                "rating": 8.7,
                "is_public": False,
                "broadcast": None,
                "area_location": None,
                "utc_offset": None,
                "localtime": None,
                "utc_datetime": None,
            }


@patch.object(JWTBearer, "verify_jwt", override_verify_jwt)
def test_create_movie_with_broadcast():
    headers = {"Authorization": "Bearer token"}
    with patch("src.movies.router.get_user") as mock_get_user:
        mock_get_user.return_value = User(id=1)
        with patch("src.movies.router.MovieService.create_movie") as mock_create_movie:
            mock_create_movie.return_value = {
                "id": 1,
                "title": "The Matrix",
                "description": "Welcome to the Real World",
                "director": "The Wachowskis",
                "year": 1999,
                "genre": "Science Fiction",
                "rating": 8.7,
                "is_public": False,
                "owner_id": 1,
                "created_at": "2021-08-31T00:00:00+00:00",
                "broadcast": "Netflix",
                "area_location": "America/Santiago",
                "utc_offset": "-04:00",
                "localtime": "2024-08-01T20:00:00-04:00",
                "utc_datetime": "2024-08-01T08:00:00+00:00",
            }
            response = client.post(
                "/movies/",
                headers=headers,
                json={
                    "title": "The Matrix",
                    "description": "Welcome to the Real World",
                    "director": "The Wachowskis",
                    "year": 1999,
                    "genre": "Science Fiction",
                    "rating": 8.7,
                    "is_public": False,
                },
            )
            assert response.status_code == 201
            assert response.json() == {
                "id": 1,
                "title": "The Matrix",
                "description": "Welcome to the Real World",
                "director": "The Wachowskis",
                "year": 1999,
                "genre": "Science Fiction",
                "rating": 8.7,
                "is_public": False,
                "broadcast": "Netflix",
                "area_location": "America/Santiago",
                "utc_offset": "-04:00",
                "localtime": "2024-08-01T20:00:00-04:00",
                "utc_datetime": "2024-08-01T08:00:00+00:00",
            }


def test_get_movies():
    with patch("src.movies.router.MovieService.get_all_movies") as mock_get_all_movies:
        mock_get_all_movies.return_value = [
            Movie(
                id=1,
                title="The Matrix",
                year=1999,
                is_public=True,
                description="Welcome to the Real World",
                director="The Wachowskis",
                genre="Science Fiction",
                rating=8.7,
                broadcast=None,
                area_location=None,
                utc_offset=None,
                localtime=None,
                utc_datetime=None,
            ),
        ]
        response = client.get("/movies/")
        assert response.status_code == 200
        assert response.json() == {
            "items": [
                {
                    "id": 1,
                    "title": "The Matrix",
                    "description": "Welcome to the Real World",
                    "director": "The Wachowskis",
                    "year": 1999,
                    "genre": "Science Fiction",
                    "rating": 8.7,
                    "broadcast": None,
                    "area_location": None,
                    "utc_offset": None,
                    "localtime": None,
                    "utc_datetime": None,
                }
            ],
            "pages": 1,
            "page": 1,
            "size": 50,
            "total": 1,
            "links": {
                "first": "/movies?page=1",
                "last": "/movies?page=1",
                "self": "/movies",
                "next": None,
                "prev": None,
            },
        }


@patch.object(JWTBearer, "verify_jwt", override_verify_jwt)
def test_get_user_movies():
    headers = {"Authorization": "Bearer token"}
    with patch("src.movies.router.get_user") as mock_get_user:
        mock_get_user.return_value = User(
            id=1
        )
        with patch("src.movies.router.MovieService.get_all_movies_for_user") as mock_get_all_movies_for_user:
            mock_get_all_movies_for_user.return_value = [
                Movie(
                    id=1,
                    title="The Matrix",
                    year=1999,
                    is_public=False,
                    description="Welcome to the Real World",
                    director="The Wachowskis",
                    genre="Science Fiction",
                    rating=8.7,
                    broadcast=None,
                    area_location=None,
                    utc_offset=None,
                    localtime=None,
                    utc_datetime=None,
                ),
            ]
            response = client.get("/movies/me", params={"user_id": int(mock_get_user.id)}, headers=headers)
            assert response.status_code == 200
            assert response.json() == {
                "items": [
                    {
                        "id": 1,
                        "title": "The Matrix",
                        "description": "Welcome to the Real World",
                        "director": "The Wachowskis",
                        "year": 1999,
                        "genre": "Science Fiction",
                        "rating": 8.7,
                        "is_public": False,
                        "broadcast": None,
                        "area_location": None,
                        "utc_offset": None,
                        "localtime": None,
                        "utc_datetime": None,
                    }
                ],
                "pages": 1,
                "page": 1,
                "size": 50,
                "total": 1,
                "links": {
                    "first": f"/movies/me?user_id={int(mock_get_user.id)}&page=1",
                    "last": f"/movies/me?user_id={int(mock_get_user.id)}&page=1",
                    "self": f"/movies/me?user_id={int(mock_get_user.id)}",
                    "next": None,
                    "prev": None,
                },
            }


def test_get_public_movie():
    with patch("src.movies.router.MovieService.get_movie") as mock_get_movie:
        mock_get_movie.return_value = Movie(
            id=1,
            title="The Matrix",
            description="Welcome to the Real World",
            director="The Wachowskis",
            year=1999,
            genre="Science Fiction",
            rating=8.7,
            is_public=True,
            broadcast=None,
            area_location=None,
            utc_offset=None,
            localtime=None,
            utc_datetime=None,
        )
        response = client.get("/movies/1")
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "title": "The Matrix",
            "description": "Welcome to the Real World",
            "director": "The Wachowskis",
            "year": 1999,
            "genre": "Science Fiction",
            "rating": 8.7,
            "broadcast": None,
            "area_location": None,
            "utc_offset": None,
            "localtime": None,
            "utc_datetime": None,
        }


@patch.object(JWTBearer, "verify_jwt", override_verify_jwt)
def test_get_private_movie():
    with patch("src.movies.router.get_user") as mock_get_user:
        mock_get_user.return_value = User(id=1)
        with patch("src.movies.router.MovieService.get_movie") as mock_get_movie:
            mock_get_movie.return_value = Movie(
                id=1,
                title="The Matrix",
                description="Welcome to the Real World",
                director="The Wachowskis",
                year=1999,
                genre="Science Fiction",
                rating=8.7,
                is_public=False,
                owner=mock_get_user.return_value,
                broadcast=None,
                area_location=None,
                utc_offset=None,
                localtime=None,
                utc_datetime=None,
            )
            response = client.get(
                "/movies/1", headers={"Authorization": "Bearer token"}
            )
            assert response.status_code == 200
            assert response.json() == {
                "id": 1,
                "title": "The Matrix",
                "description": "Welcome to the Real World",
                "director": "The Wachowskis",
                "year": 1999,
                "genre": "Science Fiction",
                "rating": 8.7,
                "broadcast": None,
                "area_location": None,
                "utc_offset": None,
                "localtime": None,
                "utc_datetime": None,
            }


def test_get_private_movie_not_authorized():
    with patch("src.movies.router.MovieService.get_movie") as mock_get_movie:
        mock_get_movie.return_value = Movie(
            id=1,
            title="The Matrix",
            description="Welcome to the Real World",
            director="The Wachowskis",
            year=1999,
            genre="Science Fiction",
            rating=8.7,
            is_public=False,
            owner=User(id=2),
            broadcast=None,
            area_location=None,
            utc_offset=None,
            localtime=None,
            utc_datetime=None,
        )
        response = client.get("/movies/1")
        assert response.status_code == 401
        assert response.json() == {"detail": ERRORS["NOT_AUTHORIZED"]}


@patch.object(JWTBearer, "verify_jwt", override_verify_jwt)
def test_update_movie():
    headers = {"Authorization": "Bearer token"}
    with patch("src.movies.router.get_user") as mock_get_user:
        mock_get_user.return_value = User(id=1)
        with patch("src.movies.router.MovieService.update_movie") as mock_update_movie:
            mock_update_movie.return_value = {
                "id": 1,
                "title": "The Matrix",
                "description": "Welcome to the Real World",
                "director": "The Wachowskis",
                "year": 1999,
                "genre": "Science Fiction",
                "rating": 8.7,
                "is_public": False,
                "broadcast": None,
                "area_location": None,
                "utc_offset": None,
                "localtime": None,
                "utc_datetime": None,
            }
            response = client.patch(
                "/movies/1",
                headers=headers,
                json={
                    "title": "The Matrix",
                    "description": "Welcome to the Real World",
                    "director": "The Wachowskis",
                    "year": 2000,
                    "genre": "Science Fiction",
                    "rating": 8.7,
                    "is_public": False,
                    "broadcast": None,
                    "area_location": None,
                    "utc_offset": None,
                    "localtime": None,
                    "utc_datetime": None,
                },
            )
            assert response.status_code == 200
            assert response.json() == {
                "id": 1,
                "title": "The Matrix",
                "description": "Welcome to the Real World",
                "director": "The Wachowskis",
                "year": 1999,
                "genre": "Science Fiction",
                "rating": 8.7,
                "is_public": False,
                "broadcast": None,
                "area_location": None,
                "utc_offset": None,
                "localtime": None,
                "utc_datetime": None,
            }
