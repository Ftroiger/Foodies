from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.favorite import Favorite
from app.schemas.favorite import FavoriteCreate


class FavoriteService:
    def __init__(self, db: Session):
        self.db = db

    def add_favorite(self, user_id: int, favorite_data: FavoriteCreate) -> Favorite:
        existing = (
            self.db.query(Favorite)
            .filter(Favorite.user_id == user_id, Favorite.place_id == favorite_data.place_id)
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este lugar ya está en tus favoritos",
            )

        favorite = Favorite(user_id=user_id, place_id=favorite_data.place_id)
        self.db.add(favorite)
        self.db.commit()
        self.db.refresh(favorite)
        return favorite

    def get_user_favorites(self, user_id: int):
        return self.db.query(Favorite).filter(Favorite.user_id == user_id).all()

    def remove_favorite(self, user_id: int, place_id: int):
        favorite = (
            self.db.query(Favorite)
            .filter(Favorite.user_id == user_id, Favorite.place_id == place_id)
            .first()
        )
        if not favorite:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Favorito no encontrado",
            )
        self.db.delete(favorite)
        self.db.commit()
