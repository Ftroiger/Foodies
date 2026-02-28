from pydantic import BaseModel
from datetime import datetime


class FavoriteCreate(BaseModel):
    place_id: int


class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    place_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
