from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

from app.core.config import settings
from app.db.repositories.user_repo import UserRepository
from app.db.session import async_session


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if not isinstance(event, Update):
            return await handler(event, data)

        tg_user = None
        if event.message and event.message.from_user:
            tg_user = event.message.from_user
        elif event.callback_query and event.callback_query.from_user:
            tg_user = event.callback_query.from_user

        if tg_user is None:
            return await handler(event, data)

        async with async_session() as session:
            repo = UserRepository(session)
            user, created = await repo.get_or_create(
                telegram_id=tg_user.id,
                username=tg_user.username,
                first_name=tg_user.first_name,
                ui_language=tg_user.language_code or settings.default_ui_language,
            )
            if not created and (
                user.username != tg_user.username
                or user.first_name != tg_user.first_name
            ):
                await repo.update(
                    user,
                    username=tg_user.username,
                    first_name=tg_user.first_name,
                )

            data["db_session"] = session
            data["db_user"] = user
            data["user_repo"] = repo

            return await handler(event, data)
