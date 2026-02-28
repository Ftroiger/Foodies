from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool = False


class GroupCreate(GroupBase):
    pass


class GroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    cover_image_url: Optional[str] = None
    is_public: Optional[bool] = None


class GroupResponse(GroupBase):
    id: int
    cover_image_url: Optional[str] = None
    created_by: int
    created_at: datetime

    model_config = {"from_attributes": True}


class GroupMemberResponse(BaseModel):
    id: int
    group_id: int
    user_id: int
    role: str
    joined_at: datetime

    model_config = {"from_attributes": True}


class GroupPlaceCreate(BaseModel):
    place_id: int
    note: Optional[str] = None


class GroupPlaceResponse(BaseModel):
    id: int
    group_id: int
    place_id: int
    added_by: int
    note: Optional[str] = None
    added_at: datetime

    model_config = {"from_attributes": True}
