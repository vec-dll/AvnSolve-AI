from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.core.constants import SUPPORTED_LANGUAGES, GRADE_LABELS, STYLE_LABELS


def language_keyboard() -> InlineKeyboardMarkup:
    buttons = []
    for code, name in SUPPORTED_LANGUAGES.items():
        buttons.append([InlineKeyboardButton(text=name, callback_data=f"lang:{code}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def grade_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    labels = GRADE_LABELS.get(lang, GRADE_LABELS["ru"])
    buttons = []
    row = []
    for value, label in labels.items():
        row.append(InlineKeyboardButton(text=label, callback_data=f"grade:{value}"))
        if len(row) == 4:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def style_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    labels = STYLE_LABELS.get(lang, STYLE_LABELS["ru"])
    buttons = []
    for value, label in labels.items():
        buttons.append([InlineKeyboardButton(text=label, callback_data=f"style:{value}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
