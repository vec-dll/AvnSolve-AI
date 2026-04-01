from pathlib import Path

from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


def _ensure_sqlite_directory_exists(database_url: str) -> None:
    if not database_url.startswith("sqlite+aiosqlite:///"):
        return

    db_path = make_url(database_url).database
    if not db_path or db_path == ":memory:":
        return

    db_file = Path(db_path)
    if not db_file.is_absolute():
        db_file = Path.cwd() / db_file

    db_file.parent.mkdir(parents=True, exist_ok=True)


_ensure_sqlite_directory_exists(settings.database_url)
engine = create_async_engine(settings.database_url, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
