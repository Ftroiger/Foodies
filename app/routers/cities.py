from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.dependencies.database import get_db
from app.schemas.city import CityResponse
from app.services.city_service import CityService

router = APIRouter(prefix="/cities", tags=["Ciudades"])


@router.get("/", 
            summary="Listar ciudades",
            description="Devuelve una lista de ciudades, opcionalmente filtradas por nombre o país.",
            response_model=list[CityResponse])
def list_cities(
    search: Optional[str] = None,
    country: Optional[str] = None,
    db: Session = Depends(get_db),
):
    service = CityService(db)
    return service.get_cities(search=search, country=country)
