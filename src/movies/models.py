from datetime import datetime, UTC
import pytz
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

    def set_datetime_with_offset(self, local_dt_str, utc_offset_str):
        self.time, self.utc_datetime = self.localize(local_dt_str, utc_offset_str)

    @staticmethod
    def localize(local_dt_str, utc_offset_str):
        local_dt = datetime.strptime(local_dt_str, "%Y-%m-%d %H:%M:%S")
        offset_hours, offset_minutes = map(int, utc_offset_str.split(':'))
        offset = pytz.FixedOffset(offset_hours * 60 + offset_minutes)
        local_dt = offset.localize(local_dt)
        utc_dt = local_dt.astimezone(pytz.utc)
        return local_dt.isoformat(), utc_dt.isoformat()
