from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.schemas.user import UserCreate, UserLogin, Token, GoogleToken
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post(
        "/register", 
        summary="Registrar un nuevo usuario",
        description="Registra un nuevo usuario en el sistema y devuelve un token de autenticación.",
        response_model=Token
)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.register(user_data)


@router.post(
        "/login",
        summary="Iniciar sesión",
        description="Inicia sesión con las credenciales del usuario y devuelve un token de autenticación.",
        response_model=Token
)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.login(credentials)


@router.post(
        "/google",
        summary="Iniciar sesión con Google",
        description="Autentica al usuario mediante un ID Token de Google. Si el usuario no existe, se crea automáticamente.",
        response_model=Token
)
def google_login(google_token: GoogleToken, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.google_login(google_token.token)


@router.post(
        "/refresh",
        summary="Actualizar token",
        description="Actualiza el token de autenticación utilizando un token de refresco.",
        response_model=Token
)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.refresh(refresh_token)
