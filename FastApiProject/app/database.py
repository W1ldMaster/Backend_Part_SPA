from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

# Абсолютный путь к БД рядом с папкой app/
BASE_DIR = Path(__file__).resolve().parent.parent   # ...\Backend\FastApiProject
DB_PATH = BASE_DIR / "db.sqlite3"

SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH.as_posix()}"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False,
    connect_args={"timeout": 5},   # вместо вечного зависания — "database is locked"
)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with async_session_maker() as session:
        yield session