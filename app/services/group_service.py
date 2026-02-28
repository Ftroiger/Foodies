from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.group import UserGroup
from app.models.group_member import GroupMember
from app.models.group_place import GroupPlace
from app.schemas.group import GroupCreate, GroupUpdate, GroupPlaceCreate


class GroupService:
    def __init__(self, db: Session):
        self.db = db

    def create_group(self, user_id: int, group_data: GroupCreate) -> UserGroup:
        group = UserGroup(
            name=group_data.name,
            description=group_data.description,
            is_public=group_data.is_public,
            created_by=user_id,
        )
        self.db.add(group)
        self.db.commit()
        self.db.refresh(group)

        # Agregar al creador como owner
        member = GroupMember(group_id=group.id, user_id=user_id, role="owner")
        self.db.add(member)
        self.db.commit()

        return group

    def get_group(self, group_id: int) -> UserGroup:
        group = self.db.query(UserGroup).filter(UserGroup.id == group_id).first()
        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Grupo no encontrado",
            )
        return group

    def get_user_groups(self, user_id: int):
        return (
            self.db.query(UserGroup)
            .join(GroupMember)
            .filter(GroupMember.user_id == user_id)
            .all()
        )

    def update_group(self, group_id: int, user_id: int, group_data: GroupUpdate) -> UserGroup:
        group = self.get_group(group_id)
        self._check_admin_permission(group_id, user_id)

        update_data = group_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(group, field, value)
        self.db.commit()
        self.db.refresh(group)
        return group

    def add_member(self, group_id: int, admin_user_id: int, user_identifier: str):
        self._check_admin_permission(group_id, admin_user_id)
        # TODO: Buscar usuario por email o username e invitarlo
        pass

    def get_members(self, group_id: int):
        return self.db.query(GroupMember).filter(GroupMember.group_id == group_id).all()

    def remove_member(self, group_id: int, admin_user_id: int, target_user_id: int):
        self._check_admin_permission(group_id, admin_user_id)
        member = (
            self.db.query(GroupMember)
            .filter(GroupMember.group_id == group_id, GroupMember.user_id == target_user_id)
            .first()
        )
        if member:
            self.db.delete(member)
            self.db.commit()

    def add_place(self, group_id: int, user_id: int, place_data: GroupPlaceCreate) -> GroupPlace:
        group_place = GroupPlace(
            group_id=group_id,
            place_id=place_data.place_id,
            added_by=user_id,
            note=place_data.note,
        )
        self.db.add(group_place)
        self.db.commit()
        self.db.refresh(group_place)
        return group_place

    def get_group_places(self, group_id: int):
        return self.db.query(GroupPlace).filter(GroupPlace.group_id == group_id).all()

    def _check_admin_permission(self, group_id: int, user_id: int):
        member = (
            self.db.query(GroupMember)
            .filter(
                GroupMember.group_id == group_id,
                GroupMember.user_id == user_id,
                GroupMember.role.in_(["owner", "admin"]),
            )
            .first()
        )
        if not member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos de administrador en este grupo",
            )
