import io
import logging

from aiogram import Router, F
from aiogram.types import Message, BufferedInputFile
from aiogram.exceptions import TelegramBadRequest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import MessageType, Intent
from app.db.models.user import User
from app.db.repositories.user_repo import UserRepository
from app.schemas.user import AIRequest, UserProfile
from app.services.ai_router import get_ai_response
from app.services import gemini_service
from app.services.history_service import HistoryService
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


async def _handle_image_generation(
    message: Message,
    text: str,
    db_user: User,
    db_session: AsyncSession,
    thinking_msg: Message,
) -> None:
    """Handle image generation requests via Gemini."""
    try:
        image_bytes, text_response, elapsed_ms = await gemini_service.generate_image(text)

        history_svc = HistoryService(db_session)
        await history_svc.save_user_message(
            user_id=db_user.id,
            text=text,
            message_type=MessageType.TEXT,
            intent=Intent.GENERATE_IMAGE,
        )

        await _delete_msg(thinking_msg)

        if image_bytes:
            photo_file = BufferedInputFile(image_bytes, filename="generated.png")
            await message.answer_photo(photo=photo_file, caption=text_response or "")
            await history_svc.save_assistant_message(
                user_id=db_user.id,
                text=text_response or "[image generated]",
                ai_provider="gemini",
                response_time_ms=elapsed_ms,
            )
        elif text_response:
            await safe_send(message, text_response)
            await history_svc.save_assistant_message(
                user_id=db_user.id,
                text=text_response,
                ai_provider="gemini",
                response_time_ms=elapsed_ms,
            )
        else:
            await message.answer(t("error_generic", db_user.ui_language))

        logger.info("user=%d image_gen time=%dms", db_user.telegram_id, elapsed_ms)

    except Exception:
        logger.exception("Image generation failed for user=%d", db_user.telegram_id)
        await _delete_msg(thinking_msg)
        await message.answer(t("error_image_gen", db_user.ui_language))


@router.message(F.text)
async def handle_text_message(
    message: Message,
    db_user: User,
    db_session: AsyncSession,
    user_repo: UserRepository,
) -> None:
    if not db_user.onboarding_complete:
        lang = db_user.ui_language or "ru"
        await message.answer(t("help_text", lang))
        return

    text = message.text.strip()
    if not text:
        await message.answer(t("error_empty_message", db_user.ui_language))
        return

    thinking_msg = await message.answer(t("thinking", db_user.ui_language))

    try:
        detected_lang = detect_language(text, ui_language=db_user.ui_language)
        response_lang = get_response_language(
            detected_lang, db_user.last_message_language, db_user.ui_language
        )
        intent = classify_intent(text, has_image=False)

        await user_repo.update(db_user, last_message_language=response_lang)

        # Image generation — route to Gemini directly
        if intent == Intent.GENERATE_IMAGE:
            await _handle_image_generation(
                message, text, db_user, db_session, thinking_msg
            )
            return

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
            text=text,
            intent=intent,
            detected_language=response_lang,
            context_messages=context,
        )

        ai_text, provider, elapsed_ms = await get_ai_response(request)

        await history_svc.save_user_message(
            user_id=db_user.id,
            text=text,
            message_type=MessageType.TEXT,
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
            "user=%d provider=%s intent=%s lang=%s time=%dms",
            db_user.telegram_id, provider, intent, response_lang, elapsed_ms,
        )

    except Exception:
        logger.exception("Error handling text message from user=%d", db_user.telegram_id)
        await _delete_msg(thinking_msg)
        await message.answer(t("error_generic", db_user.ui_language))
