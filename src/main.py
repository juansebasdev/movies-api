from fastapi import FastAPI

from src.auth.router import router as auth_router
from src.config import HOST, PORT, Base
from src.database import ConfigDatabase

Base.metadata.create_all(bind=ConfigDatabase().engine)

app = FastAPI()
app.include_router(auth_router, prefix="/auth")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
