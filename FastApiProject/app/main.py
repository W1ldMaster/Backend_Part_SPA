from fastapi import FastAPI
from fastapi_pagination import add_pagination
from app.routers import posts_django
from app.routers.auth_users import router as auth_users_router


async def lifespan(app: FastAPI):
    yield

app = FastAPI(title="SSA_fastAPI", lifespan=lifespan)
app.include_router(auth_users_router)
app.include_router(posts_django.router)
add_pagination(app)
