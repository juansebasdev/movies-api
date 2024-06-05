import sqlalchemy
from requests import Session
from sqlalchemy import Connection, Engine
from sqlalchemy.orm import sessionmaker

from src.utils import Singleton


class ConfigDatabase(metaclass=Singleton):  # noqa: F821
    engine: Engine = None
    connection: Connection = None
    session: Session = None

    def __init__(self):
        self.engine = sqlalchemy.create_engine("sqlite:///./test.db", echo=True)
        self.connection = self.engine.connect()
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.session = SessionLocal()