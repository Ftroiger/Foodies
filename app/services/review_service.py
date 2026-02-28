from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate


class ReviewService:
    def __init__(self, db: Session):
        self.db = db

    def create_review(self, user_id: int, review_data: ReviewCreate) -> Review:
        review = Review(
            user_id=user_id,
            place_id=review_data.place_id,
            rating=review_data.rating,
            comment=review_data.comment,
        )
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)
        return review

    def update_review(self, review_id: int, user_id: int, review_data: ReviewUpdate) -> Review:
        review = self._get_own_review(review_id, user_id)
        update_data = review_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(review, field, value)
        self.db.commit()
        self.db.refresh(review)
        return review

    def delete_review(self, review_id: int, user_id: int):
        review = self._get_own_review(review_id, user_id)
        self.db.delete(review)
        self.db.commit()

    def _get_own_review(self, review_id: int, user_id: int) -> Review:
        review = self.db.query(Review).filter(Review.id == review_id).first()
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reseña no encontrada",
            )
        if review.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para modificar esta reseña",
            )
        return review
