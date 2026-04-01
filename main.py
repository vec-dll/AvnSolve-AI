import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from app.core.config import settings
from app.core.logging import setup_logging
from app.bot.handlers import setup_routers
from app.bot.middlewares.user import UserMiddleware
from app.bot.middlewares.throttle import ThrottleMiddleware
from app.db.session import engine, Base

logger = logging.getLogger(__name__)


async def on_startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created / verified")


async def main() -> None:
    setup_logging()
    logger.info("Starting Study Bot (env=%s)", settings.app_env)

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(),
    )
    dp = Dispatcher()

    dp.update.middleware(UserMiddleware())
    dp.message.middleware(ThrottleMiddleware(rate_limit=0.5))

    dp.include_router(setup_routers())

    dp.startup.register(on_startup)

    logger.info("Bot is starting polling...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
