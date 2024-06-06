from fastapi import FastAPI
from fastapi_pagination import add_pagination

from src.auth.router import router as auth_router
from src.movies.router import router as movies_router
from src.wtapi.router import router as wtapi_router
from src.config import HOST, PORT, Base
from src.database import ConfigDatabase

Base.metadata.create_all(bind=ConfigDatabase().engine)

app = FastAPI(
    title="Movies API",
)
app.include_router(auth_router, prefix="/auth")
app.include_router(movies_router, prefix="/movies")
app.include_router(wtapi_router, prefix="/wtapi")

add_pagination(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
