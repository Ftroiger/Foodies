from sqlalchemy.orm import Session
from app.models.city import City


class CityService:
    def __init__(self, db: Session):
        self.db = db

    def get_cities(self, search: str | None = None, country: str | None = None):
        query = self.db.query(City)

        if search:
            query = query.filter(City.name.ilike(f"%{search}%"))
        if country:
            query = query.filter(City.country == country)

        return query.order_by(City.name).all()
