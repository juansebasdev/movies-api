from datetime import datetime, UTC
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.config import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    director = Column(String)
    year = Column(Integer)
    genre = Column(String)
    rating = Column(Float)
    is_public = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.now(UTC))
    broadcast = Column(String, nullable=True)
    area_location = Column(String, nullable=True)
    localtime = Column(String, nullable=True)
    utc_datetime = Column(String, nullable=True)
    utc_offset = Column(String, nullable=True)

    owner = relationship("User", back_populates="movies")

    def __repr__(self):
        return f"<Movie(title={self.title}, year={self.year})>"
