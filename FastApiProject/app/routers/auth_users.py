from fastapi import APIRouter
from app.core.auth import fastapi_users, auth_backend
from app.models import User
from app.schemas import UserRead, UserCreate, UserUpdate
router = APIRouter()


router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),   # ✅
    prefix="/users",
    tags=["users"]
)

# Регистрация
router.include_router(
    # fastapi_users.get_register_router(User, User),  # /auth/register
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"]
)

# Сброс пароля
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"]
)

# Управление пользователями
router.include_router(
    fastapi_users.get_users_router(UserRead, UserCreate),  # /users/me, /users/{id}
    prefix="/users",
    tags=["users"]
)