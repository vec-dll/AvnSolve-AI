import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards.onboarding import language_keyboard, grade_keyboard, style_keyboard
from app.bot.keyboards.settings import settings_keyboard
from app.db.models.user import User
from app.db.repositories.user_repo import UserRepository
from app.services.history_service import HistoryService
from app.utils.i18n import t

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("settings"))
async def cmd_settings(message: Message, db_user: User) -> None:
    lang = db_user.ui_language or "ru"
    await message.answer(t("settings_title", lang), reply_markup=settings_keyboard(lang))


@router.message(Command("clear"))
async def cmd_clear(message: Message, db_user: User, db_session: AsyncSession) -> None:
    lang = db_user.ui_language or "ru"
    history_svc = HistoryService(db_session)
    await history_svc.clear(db_user.id)
    await message.answer(t("history_cleared", lang))


@router.callback_query(F.data == "set:language")
async def settings_language(callback: CallbackQuery, db_user: User) -> None:
    lang = db_user.ui_language or "ru"
    await callback.message.edit_text(
        t("choose_language", lang), reply_markup=language_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "set:grade")
async def settings_grade(callback: CallbackQuery, db_user: User) -> None:
    lang = db_user.ui_language or "ru"
    await callback.message.edit_text(
        t("choose_grade", lang), reply_markup=grade_keyboard(lang)
    )
    await callback.answer()


@router.callback_query(F.data == "set:style")
async def settings_style(callback: CallbackQuery, db_user: User) -> None:
    lang = db_user.ui_language or "ru"
    await callback.message.edit_text(
        t("choose_style", lang), reply_markup=style_keyboard(lang)
    )
    await callback.answer()


@router.callback_query(F.data == "set:clear_history")
async def settings_clear_history(
    callback: CallbackQuery,
    db_user: User,
    db_session: AsyncSession,
) -> None:
    lang = db_user.ui_language or "ru"
    history_svc = HistoryService(db_session)
    await history_svc.clear(db_user.id)
    await callback.message.edit_text(t("history_cleared", lang))
    await callback.answer()
