from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    google_place_id = Column(String, unique=True, index=True)
    name = Column(String, nullable=False, index=True)
    address = Column(String)
    city = Column(String, index=True)
    state = Column(String)
    country = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    phone = Column(String)
    website = Column(String)
    google_maps_url = Column(String)
    google_rating = Column(Float)
    google_ratings_total = Column(Integer)
    price_level = Column(String)
    category = Column(String, index=True)  # bar | restaurant | cafe
    opening_hours = Column(JSON)
    photos_urls = Column(JSON)
    last_synced_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    reviews = relationship("Review", back_populates="place")
    favorites = relationship("Favorite", back_populates="place")
    group_places = relationship("GroupPlace", back_populates="place")
    categories = relationship(
        "PlaceCategory", secondary="place_place_categories", back_populates="places"
    )
