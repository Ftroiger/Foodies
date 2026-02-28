from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.favorite import FavoriteCreate, FavoriteResponse
from app.services.favorite_service import FavoriteService
from app.models.user import User

router = APIRouter(prefix="/favorites", tags=["Favoritos"])


@router.post("/", response_model=FavoriteResponse)
def add_favorite(
    favorite_data: FavoriteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = FavoriteService(db)
    return service.add_favorite(current_user.id, favorite_data)


@router.get("/", response_model=list[FavoriteResponse])
def list_favorites(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = FavoriteService(db)
    return service.get_user_favorites(current_user.id)


@router.delete("/{place_id}")
def remove_favorite(
    place_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = FavoriteService(db)
    service.remove_favorite(current_user.id, place_id)
    return {"message": "Favorito eliminado"}
