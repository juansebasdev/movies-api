import os
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

# Environment variables
PORT = int(os.getenv("PORT", 8080))
HOST = os.getenv("HOST", "127.0.0.1")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
SQL_URL = os.getenv("SQL_URL")
MONGO_URL = os.getenv("MONGO_URL")
DATA_REPOSITORY = os.getenv("DATA_REPOSITORY", "DATABASE")
APP_URL = os.getenv("APP_URL", f"http://{HOST}:{PORT}")

if DATA_REPOSITORY not in ["SQL", "NOSQL"]:
    raise ValueError("DATA_REPOSITORY must be SQL or NOSQL")

# Database
Base = declarative_base()
