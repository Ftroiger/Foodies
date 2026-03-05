from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.dependencies.database import get_db
from app.schemas.place import PlaceResponse, PlaceListResponse
from app.services.place_service import PlaceService
from app.utils.pagination import PaginationParams

router = APIRouter(prefix="/places", tags=["Lugares"])


@router.get(
        "/", 
        summary="Listar lugares",
        description="Devuelve una lista de lugares, opcionalmente filtrados por ciudad, categoría o búsqueda.",
        response_model=list[PlaceListResponse]
)
def list_places(
    city: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
):
    service = PlaceService(db)
    return service.get_places(
        city=city, category=category, search=search, pagination=pagination
    )


@router.get(
        "/{place_id}",
        summary="Obtener lugar",
        description="Devuelve los detalles de un lugar específico.",
        response_model=PlaceResponse
)
def get_place(place_id: int, db: Session = Depends(get_db)):
    service = PlaceService(db)
    return service.get_place(place_id)
