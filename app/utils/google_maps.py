def parse_place_details(google_response: dict) -> dict:
    """Parsear la respuesta de Google Place Details a un dict plano."""
    result = google_response.get("result", {})

    geometry = result.get("geometry", {}).get("location", {})

    opening_hours = result.get("opening_hours", {})
    photos = result.get("photos", [])
    photo_urls = [
        f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photoreference={p.get('photo_reference')}"
        for p in photos
        if p.get("photo_reference")
    ]

    return {
        "name": result.get("name"),
        "address": result.get("formatted_address"),
        "latitude": geometry.get("lat"),
        "longitude": geometry.get("lng"),
        "phone": result.get("formatted_phone_number"),
        "website": result.get("website"),
        "google_maps_url": result.get("url"),
        "google_rating": result.get("rating"),
        "google_ratings_total": result.get("user_ratings_total"),
        "price_level": str(result.get("price_level", "")),
        "opening_hours": opening_hours.get("weekday_text", []),
        "photos_urls": photo_urls,
    }
