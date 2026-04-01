from aiogram import Router

from app.bot.handlers.start import router as start_router
from app.bot.handlers.settings import router as settings_router
from app.bot.handlers.messages import router as messages_router
from app.bot.handlers.images import router as images_router


def setup_routers() -> Router:
    root = Router()
    root.include_router(start_router)
    root.include_router(settings_router)
    root.include_router(images_router)
    root.include_router(messages_router)
    return root
