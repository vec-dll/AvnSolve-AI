import logging

from aiogram import Router, F
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import MessageType
from app.db.models.user import User
from app.db.repositories.user_repo import UserRepository
from app.schemas.user import AIRequest, UserProfile
from app.services.ai_router import get_ai_response
from app.services.history_service import HistoryService
from app.services.image_service import download_photo, cleanup_temp_file
from app.services.intent_service import classify_intent
from app.services.language_service import detect_language, get_response_language
from app.services.response_formatter import safe_send
from app.utils.i18n import t

logger = logging.getLogger(__name__)
router = Router()


async def _delete_msg(msg: Message) -> None:
    try:
        await msg.delete()
    except TelegramBadRequest:
        pass


@router.message(F.photo)
async def handle_photo_message(
    message: Message,
    db_user: User,
    db_session: AsyncSession,
    user_repo: UserRepository,
) -> None:
    if not db_user.onboarding_complete:
        lang = db_user.ui_language or "ru"
        await message.answer(t("help_text", lang))
        return

    thinking_msg = await message.answer(t("thinking", db_user.ui_language))
    image_path: str | None = None

    try:
        photo = message.photo[-1]
        image_path = await download_photo(message.bot, photo.file_id)

        if image_path is None:
            await _delete_msg(thinking_msg)
            await message.answer(
                t("error_image_too_large", db_user.ui_language, max_mb=10)
            )
            return

        caption = message.caption or ""
        has_caption = bool(caption.strip())

        detected_lang = detect_language(caption, ui_language=db_user.ui_language) if has_caption else None
        response_lang = get_response_language(
            detected_lang, db_user.last_message_language, db_user.ui_language
        )
        intent = classify_intent(caption, has_image=True, has_caption=has_caption)

        if has_caption:
            msg_type = MessageType.IMAGE_TEXT
        else:
            msg_type = MessageType.IMAGE

        await user_repo.update(db_user, last_message_language=response_lang)

        history_svc = HistoryService(db_session)
        context = await history_svc.get_context(db_user.id)

        profile = UserProfile(
            telegram_id=db_user.telegram_id,
            ui_language=db_user.ui_language,
            grade_level=db_user.grade_level,
            response_style=db_user.response_style,
            last_message_language=response_lang,
            onboarding_complete=db_user.onboarding_complete,
        )

        request = AIRequest(
            user_profile=profile,
            text=caption if has_caption else None,
            image_path=image_path,
            image_caption=caption if has_caption else None,
            intent=intent,
            detected_language=response_lang,
            context_messages=context,
        )

        ai_text, provider, elapsed_ms = await get_ai_response(request)

        await history_svc.save_user_message(
            user_id=db_user.id,
            text=caption or "[image]",
            message_type=msg_type,
            image_file_id=photo.file_id,
            language=response_lang,
            intent=intent,
        )
        await history_svc.save_assistant_message(
            user_id=db_user.id,
            text=ai_text,
            ai_provider=provider,
            response_time_ms=elapsed_ms,
        )

        await _delete_msg(thinking_msg)
        await safe_send(message, ai_text)

        logger.info(
            "user=%d photo provider=%s intent=%s lang=%s time=%dms",
            db_user.telegram_id, provider, intent, response_lang, elapsed_ms,
        )

    except Exception as exc:
        logger.exception("Error handling photo from user=%d", db_user.telegram_id)
        await _delete_msg(thinking_msg)
        err_key = "error_image_unavailable" if "gemini" in str(exc).lower() else "error_generic"
        await message.answer(t(err_key, db_user.ui_language))

    finally:
        cleanup_temp_file(image_path)
