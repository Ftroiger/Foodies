from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PlaceBase(BaseModel):
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    category: Optional[str] = None


class PlaceCreate(PlaceBase):
    google_place_id: str


class PlaceResponse(PlaceBase):
    id: int
    google_place_id: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    google_maps_url: Optional[str] = None
    google_rating: Optional[float] = None
    google_ratings_total: Optional[int] = None
    price_level: Optional[str] = None
    opening_hours: Optional[dict] = None
    photos_urls: Optional[list] = None
    platform_rating: Optional[float] = None
    last_synced_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class PlaceListResponse(BaseModel):
    id: int
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    category: Optional[str] = None
    google_rating: Optional[float] = None
    platform_rating: Optional[float] = None
    photos_urls: Optional[list] = None

    model_config = {"from_attributes": True}
