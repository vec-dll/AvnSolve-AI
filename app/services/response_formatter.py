import logging

from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest

logger = logging.getLogger(__name__)


def truncate_for_telegram(text: str, max_length: int = 4096) -> str:
    if len(text) <= max_length:
        return text
    return text[: max_length - 20] + "\n\n... (truncated)"


def format_response(text: str) -> str:
    text = text.strip()
    text = truncate_for_telegram(text)
    return text


async def safe_send(message: Message, text: str) -> Message:
    """Send message trying Markdown first, falling back to plain text."""
    formatted = format_response(text)
    try:
        return await message.answer(formatted, parse_mode="Markdown")
    except TelegramBadRequest:
        logger.debug("Markdown parse failed, sending as plain text")
        return await message.answer(formatted, parse_mode=None)
