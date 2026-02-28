from pydantic import BaseModel
from typing import Optional


class CityBase(BaseModel):
    name: str
    state: Optional[str] = None
    country: Optional[str] = None


class CityCreate(CityBase):
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class CityResponse(CityBase):
    id: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    model_config = {"from_attributes": True}
