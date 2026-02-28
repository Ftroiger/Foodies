import httpx
from app.config import get_settings


class GoogleMapsService:
    """Servicio para integración con Google Places API."""

    BASE_URL = "https://maps.googleapis.com/maps/api/place"

    def __init__(self):
        self.settings = get_settings()
        self.api_key = self.settings.GOOGLE_MAPS_API_KEY

    async def search_places(self, query: str, location: str | None = None):
        """Buscar lugares en Google Places API."""
        params = {
            "query": query,
            "key": self.api_key,
        }
        if location:
            params["location"] = location

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/textsearch/json", params=params)
            return response.json()

    async def get_place_details(self, place_id: str):
        """Obtener detalles de un lugar por su place_id de Google."""
        params = {
            "place_id": place_id,
            "key": self.api_key,
            "fields": "name,formatted_address,geometry,formatted_phone_number,website,url,rating,user_ratings_total,price_level,opening_hours,photos",
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/details/json", params=params)
            return response.json()
