from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.utils.i18n import t


def settings_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t("settings_language", lang), callback_data="set:language")],
        [InlineKeyboardButton(text=t("settings_grade", lang), callback_data="set:grade")],
        [InlineKeyboardButton(text=t("settings_style", lang), callback_data="set:style")],
        [InlineKeyboardButton(text=t("settings_clear_history", lang), callback_data="set:clear_history")],
    ])
