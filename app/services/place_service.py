from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.place import Place
from app.utils.pagination import PaginationParams


class PlaceService:
    def __init__(self, db: Session):
        self.db = db

    def get_places(
        self,
        city: str | None = None,
        category: str | None = None,
        search: str | None = None,
        pagination: PaginationParams = None,
    ):
        query = self.db.query(Place)

        if city:
            query = query.filter(Place.city == city)
        if category:
            query = query.filter(Place.category == category)
        if search:
            query = query.filter(Place.name.ilike(f"%{search}%"))

        if pagination:
            query = query.offset(pagination.offset).limit(pagination.limit)

        return query.all()

    def get_place(self, place_id: int) -> Place:
        place = self.db.query(Place).filter(Place.id == place_id).first()
        if not place:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lugar no encontrado",
            )
        return place
