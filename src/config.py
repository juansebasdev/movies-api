import os
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

# Environment variables
PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "127.0.0.1")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
SQL_URL = os.getenv("SQL_URL")

# Database
Base = declarative_base()
