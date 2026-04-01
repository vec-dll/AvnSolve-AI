import logging

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards.onboarding import language_keyboard, grade_keyboard, style_keyboard
from app.db.models.user import User
from app.db.repositories.user_repo import UserRepository
from app.services.onboarding_service import get_next_step
from app.utils.i18n import t

logger = logging.getLogger(__name__)
router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, db_user: User, user_repo: UserRepository) -> None:
    lang = db_user.ui_language or "ru"
    name = message.from_user.first_name or "there"

    await user_repo.update(db_user, onboarding_complete=False, onboarding_step=None)

    await message.answer(t("welcome", lang, name=name))
    await message.answer(t("choose_language", lang), reply_markup=language_keyboard())
    await user_repo.update(db_user, onboarding_step="language")


@router.message(Command("help"))
async def cmd_help(message: Message, db_user: User) -> None:
    lang = db_user.ui_language or "ru"
    await message.answer(t("help_text", lang))


@router.callback_query(F.data.startswith("lang:"))
async def on_language_chosen(
    callback: CallbackQuery,
    db_user: User,
    user_repo: UserRepository,
) -> None:
    lang_code = callback.data.split(":")[1]
    await user_repo.update(db_user, ui_language=lang_code)

    if not db_user.onboarding_complete:
        await user_repo.update(db_user, onboarding_step="grade")
        await callback.message.edit_text(
            t("choose_grade", lang_code),
            reply_markup=grade_keyboard(lang_code),
        )
    else:
        await callback.message.edit_text(t("setting_updated", lang_code))

    await callback.answer()


@router.callback_query(F.data.startswith("grade:"))
async def on_grade_chosen(
    callback: CallbackQuery,
    db_user: User,
    user_repo: UserRepository,
) -> None:
    grade = callback.data.split(":")[1]
    lang = db_user.ui_language
    await user_repo.update(db_user, grade_level=grade)

    if not db_user.onboarding_complete:
        await user_repo.update(db_user, onboarding_step="style")
        await callback.message.edit_text(
            t("choose_style", lang),
            reply_markup=style_keyboard(lang),
        )
    else:
        await callback.message.edit_text(t("setting_updated", lang))

    await callback.answer()


@router.callback_query(F.data.startswith("style:"))
async def on_style_chosen(
    callback: CallbackQuery,
    db_user: User,
    user_repo: UserRepository,
) -> None:
    style = callback.data.split(":")[1]
    lang = db_user.ui_language
    await user_repo.update(db_user, response_style=style)

    if not db_user.onboarding_complete:
        await user_repo.update(db_user, onboarding_complete=True, onboarding_step="done")
        await callback.message.edit_text(t("onboarding_done", lang))
    else:
        await callback.message.edit_text(t("setting_updated", lang))

    await callback.answer()
