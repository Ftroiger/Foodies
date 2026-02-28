from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class PlaceCategory(Base):
    __tablename__ = "place_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    icon = Column(String)

    places = relationship(
        "Place", secondary="place_place_categories", back_populates="categories"
    )


class PlacePlaceCategory(Base):
    __tablename__ = "place_place_categories"

    place_id = Column(Integer, ForeignKey("places.id"), primary_key=True)
    category_id = Column(Integer, ForeignKey("place_categories.id"), primary_key=True)
