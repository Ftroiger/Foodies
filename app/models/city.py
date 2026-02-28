from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    state = Column(String)
    country = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
