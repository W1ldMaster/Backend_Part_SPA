from app.core.auth import auth_backend, current_active_user, fastapi_users
from app.core.utility import handle_domain_exception
from app.dependencies import get_user_service
from app.models import User
from app.schemas import UserCreate, UserRead, UserUpdate
from app.services.user import UserService
from fastapi import APIRouter, Depends

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)


@router.delete('/users/me', status_code=204)
async def delete_user(
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(current_active_user)
):
    try:
        return await service.delete_user(current_user=current_user)
    except Exception as e:
        handle_domain_exception(e)

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
