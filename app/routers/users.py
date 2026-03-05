from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.user import UserResponse, UserUpdate
from app.services.user_service import UserService
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Usuarios"])


@router.get(
        "/me",
        summary="Perfil del usuario",
        description="Devuelve la información del perfil del usuario autenticado.",
        response_model=UserResponse
)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.put(
        "/me",
        summary="Actualizar perfil del usuario",
        description="Actualiza la información del perfil del usuario autenticado.",
        response_model=UserResponse
)
def update_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = UserService(db)
    return service.update_user(current_user.id, user_data)


@router.get(
    "/",
    summary="Listar usuarios",
    description="Devuelve una lista paginada de todos los usuarios activos.",
    response_description="Lista de usuarios.",
)
async def list_users(limit: int = 10, offset: int = 0):
    service = UserService(get_db())
    return service.list_users(limit, offset)
