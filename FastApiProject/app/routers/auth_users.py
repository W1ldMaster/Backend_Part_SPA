from fastapi import APIRouter

from app.core.auth import fastapi_users, auth_backend
from app.schemas import UserRead, UserCreate, UserUpdate

router = APIRouter()

# ==================== 1. АУТЕНТИФИКАЦИЯ ====================
# /auth/jwt/login, /auth/jwt/logout
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

# ==================== 2. РЕГИСТРАЦИЯ ====================
# /auth/register
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

# ==================== 3. СБРОС ПАРОЛЯ ====================
# /auth/forgot-password, /auth/reset-password
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

# ==================== 4. УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ ====================
# /users/me, /users/{id}  ← один раз, с UserUpdate (не UserCreate!)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)