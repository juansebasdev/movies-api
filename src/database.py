from pymongo import MongoClient
import sqlalchemy
from requests import Session
from sqlalchemy import Connection, Engine
from sqlalchemy.orm import sessionmaker

from src.config import MONGO_URL, SQL_URL
from src.utils import Singleton


class SQLDatabase(metaclass=Singleton):  # noqa: F821
    engine: Engine = None
    connection: Connection = None
    session: Session = None

    def __init__(self):
        self.engine = sqlalchemy.create_engine(SQL_URL, echo=True)
        self.connection = self.engine.connect()
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.session = SessionLocal()


class NoSQLDatabase(metaclass=Singleton):
    client: MongoClient = None

    def __init__(self):
        self.client = MongoClient(MONGO_URL)
        self.db_name = self.client["movies-api"]
