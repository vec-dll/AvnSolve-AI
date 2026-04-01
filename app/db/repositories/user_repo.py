from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(
        self,
        telegram_id: int,
        username: str | None = None,
        first_name: str | None = None,
        ui_language: str = "ru",
    ) -> User:
        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            ui_language=ui_language,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, user: User, **kwargs) -> User:
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_or_create(
        self,
        telegram_id: int,
        username: str | None = None,
        first_name: str | None = None,
        ui_language: str = "ru",
    ) -> tuple[User, bool]:
        user = await self.get_by_telegram_id(telegram_id)
        if user:
            return user, False
        user = await self.create(telegram_id, username, first_name, ui_language)
        return user, True
