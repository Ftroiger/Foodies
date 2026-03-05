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


@router.post(
        "/", 
        summary="Crear grupo",
        description="Crea un nuevo grupo.",
        response_model=GroupResponse
)
def create_group(
    group_data: GroupCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = GroupService(db)
    return service.create_group(current_user.id, group_data)


@router.get(
        "/", 
        summary="Listar grupos",
        description="Devuelve una lista de los grupos del usuario autenticado.",
        response_model=list[GroupResponse]
)
def list_my_groups(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = GroupService(db)
    return service.get_user_groups(current_user.id)


@router.get(
        "/{group_id}",
        summary="Obtener grupo",
        description="Devuelve los detalles de un grupo específico.",
        response_model=GroupResponse
)
def get_group(group_id: int, db: Session = Depends(get_db)):
    service = GroupService(db)
    return service.get_group(group_id)


@router.put(
        "/{group_id}",
        summary="Actualizar grupo",
        description="Actualiza los detalles de un grupo existente.",
        response_model=GroupResponse
)
def update_group(
    group_id: int,
    group_data: GroupUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = GroupService(db)
    return service.update_group(group_id, current_user.id, group_data)


@router.post(
        "/{group_id}/members",
        summary="Invitar miembro",
        description="Invita a un nuevo miembro a un grupo existente."
)
def invite_member(
    group_id: int,
    user_identifier: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = GroupService(db)
    return service.add_member(group_id, current_user.id, user_identifier)


@router.get(
        "/{group_id}/members",
        summary="Listar miembros",
        description="Devuelve una lista de los miembros de un grupo.",
        response_model=list[GroupMemberResponse]
)
def list_members(group_id: int, db: Session = Depends(get_db)):
    service = GroupService(db)
    return service.get_members(group_id)


@router.delete(
        "/{group_id}/members/{user_id}",
        summary="Eliminar miembro",
        description="Elimina un miembro de un grupo existente."
)
def remove_member(
    group_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = GroupService(db)
    service.remove_member(group_id, current_user.id, user_id)
    return {"message": "Miembro eliminado"}


@router.post(
        "/{group_id}/places",
        summary="Agregar lugar al grupo",
        description="Agrega un lugar a un grupo existente.",
        response_model=GroupPlaceResponse
)
def add_place_to_group(
    group_id: int,
    place_data: GroupPlaceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = GroupService(db)
    return service.add_place(group_id, current_user.id, place_data)


@router.get(
        "/{group_id}/places",
        summary="Listar lugares del grupo",
        description="Devuelve una lista de los lugares de un grupo.",
        response_model=list[GroupPlaceResponse]
)
def list_group_places(group_id: int, db: Session = Depends(get_db)):
    service = GroupService(db)
    return service.get_group_places(group_id)
