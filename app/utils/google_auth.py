from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi import HTTPException, status
from app.config import get_settings


def verify_google_token(token: str) -> dict:
    """Verifica un ID Token de Google y retorna la información del usuario."""
    settings = get_settings()

    if not settings.GOOGLE_CLIENT_ID:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="GOOGLE_CLIENT_ID no está configurado",
        )

    try:
        id_info = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            settings.GOOGLE_CLIENT_ID,
        )

        if id_info["iss"] not in ("accounts.google.com", "https://accounts.google.com"):
            raise ValueError("Emisor del token inválido")

        if not id_info.get("email_verified", False):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email de Google no está verificado",
            )

        return {
            "email": id_info["email"],
            "name": id_info.get("name"),
            "picture": id_info.get("picture"),
        }

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de Google inválido",
        )
