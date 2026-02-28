from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class GroupPlace(Base):
    __tablename__ = "group_places"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("user_groups.id"), nullable=False)
    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)
    added_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    note = Column(String)
    added_at = Column(DateTime(timezone=True), server_default=func.now())

    group = relationship("UserGroup", back_populates="group_places")
    place = relationship("Place", back_populates="group_places")
    user = relationship("User")
