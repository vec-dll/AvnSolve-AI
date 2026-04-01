import time
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message


class ThrottleMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = 1.0):
        self._rate_limit = rate_limit
        self._last_request: dict[int, float] = {}

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        if not isinstance(event, Message) or not event.from_user:
            return await handler(event, data)

        user_id = event.from_user.id
        now = time.monotonic()
        last = self._last_request.get(user_id, 0)

        if now - last < self._rate_limit:
            return None

        self._last_request[user_id] = now
        return await handler(event, data)
