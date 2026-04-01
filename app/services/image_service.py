import logging
import os
import uuid
from pathlib import Path

from aiogram import Bot

from app.core.config import settings

logger = logging.getLogger(__name__)

TEMP_DIR = Path("temp")
ALLOWED_MIME = {"image/jpeg", "image/png", "image/webp", "image/gif"}
MAX_SIZE_BYTES = settings.max_image_size_mb * 1024 * 1024


async def download_photo(bot: Bot, file_id: str) -> str | None:
    try:
        file = await bot.get_file(file_id)
        if not file.file_path:
            logger.error("Empty file_path for file_id=%s", file_id)
            return None

        if file.file_size and file.file_size > MAX_SIZE_BYTES:
            logger.warning("File too large: %d bytes", file.file_size)
            return None

        ext = Path(file.file_path).suffix or ".jpg"
        local_path = TEMP_DIR / f"{uuid.uuid4().hex}{ext}"
        TEMP_DIR.mkdir(exist_ok=True)

        await bot.download_file(file.file_path, destination=str(local_path))
        logger.info("Downloaded photo to %s (%d bytes)", local_path, local_path.stat().st_size)
        return str(local_path)

    except Exception:
        logger.exception("Failed to download photo file_id=%s", file_id)
        return None


def cleanup_temp_file(path: str | None) -> None:
    if path and os.path.exists(path):
        try:
            os.remove(path)
            logger.debug("Removed temp file %s", path)
        except OSError:
            logger.warning("Could not remove temp file %s", path)
