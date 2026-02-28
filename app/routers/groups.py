from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.group import (
    GroupCreate,
    GroupUpdate,
    GroupResponse,
    GroupMemberResponse,
    GroupPlaceCreate,
    GroupPlaceResponse,
)
from app.services.group_service import GroupService
from app.models.user import User

router = APIRouter(prefix="/groups", tags=["Grupos"])


@router.post("/", response_model=GroupResponse)
def create_group(
    group_data: GroupCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = GroupService(db)
    return service.create_group(current_user.id, group_data)


@router.get("/", response_model=list[GroupResponse])
def list_my_groups(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = GroupService(db)
    return service.get_user_groups(current_user.id)


@router.get("/{group_id}", response_model=GroupResponse)
def get_group(group_id: int, db: Session = Depends(get_db)):
    service = GroupService(db)
    return service.get_group(group_id)


@router.put("/{group_id}", response_model=GroupResponse)
def update_group(
    group_id: int,
    group_data: GroupUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = GroupService(db)
    return service.update_group(group_id, current_user.id, group_data)


@router.post("/{group_id}/members")
def invite_member(
    group_id: int,
    user_identifier: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = GroupService(db)
    return service.add_member(group_id, current_user.id, user_identifier)


@router.get("/{group_id}/members", response_model=list[GroupMemberResponse])
def list_members(group_id: int, db: Session = Depends(get_db)):
    service = GroupService(db)
    return service.get_members(group_id)


@router.delete("/{group_id}/members/{user_id}")
def remove_member(
    group_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = GroupService(db)
    service.remove_member(group_id, current_user.id, user_id)
    return {"message": "Miembro eliminado"}


@router.post("/{group_id}/places", response_model=GroupPlaceResponse)
def add_place_to_group(
    group_id: int,
    place_data: GroupPlaceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = GroupService(db)
    return service.add_place(group_id, current_user.id, place_data)


@router.get("/{group_id}/places", response_model=list[GroupPlaceResponse])
def list_group_places(group_id: int, db: Session = Depends(get_db)):
    service = GroupService(db)
    return service.get_group_places(group_id)
