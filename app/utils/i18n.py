_TEXTS: dict[str, dict[str, str]] = {
    "welcome": {
        "ru": "Привет, {name}! Я твой учебный помощник. Давай настроим меня для тебя.",
        "en": "Hi, {name}! I'm your study assistant. Let me set things up for you.",
        "uk": "Привіт, {name}! Я твій навчальний помічник. Давай налаштуємо мене для тебе.",
    },
    "choose_language": {
        "ru": "Выбери язык интерфейса:",
        "en": "Choose interface language:",
        "uk": "Обери мову інтерфейсу:",
    },
    "choose_grade": {
        "ru": "Выбери свой класс или уровень обучения:",
        "en": "Choose your grade or education level:",
        "uk": "Обери свій клас або рівень навчання:",
    },
    "choose_style": {
        "ru": "Как тебе удобнее получать ответы?",
        "en": "How would you like to receive answers?",
        "uk": "Як тобі зручніше отримувати відповіді?",
    },
    "onboarding_done": {
        "ru": "Отлично! Всё настроено. Просто отправь мне текст или фото задания, и я помогу!",
        "en": "All set! Just send me text or a photo of your task, and I'll help!",
        "uk": "Чудово! Все налаштовано. Просто надішли мені текст або фото завдання, і я допоможу!",
    },
    "error_generic": {
        "ru": "Произошла ошибка. Попробуй ещё раз через несколько секунд.",
        "en": "An error occurred. Please try again in a few seconds.",
        "uk": "Сталася помилка. Спробуй ще раз через кілька секунд.",
    },
    "error_image_unavailable": {
        "ru": "Анализ изображений временно недоступен. Попробуй отправить текст задания.",
        "en": "Image analysis is temporarily unavailable. Try sending the task as text.",
        "uk": "Аналіз зображень тимчасово недоступний. Спробуй надіслати текст завдання.",
    },
    "error_image_too_large": {
        "ru": "Изображение слишком большое. Максимум — {max_mb} МБ.",
        "en": "Image is too large. Maximum — {max_mb} MB.",
        "uk": "Зображення завелике. Максимум — {max_mb} МБ.",
    },
    "error_empty_message": {
        "ru": "Отправь мне текст или фото, и я помогу с заданием.",
        "en": "Send me text or a photo, and I'll help with your task.",
        "uk": "Надішли мені текст або фото, і я допоможу із завданням.",
    },
    "settings_title": {
        "ru": "Настройки:",
        "en": "Settings:",
        "uk": "Налаштування:",
    },
    "settings_language": {
        "ru": "Язык интерфейса",
        "en": "Interface language",
        "uk": "Мова інтерфейсу",
    },
    "settings_grade": {
        "ru": "Класс / уровень",
        "en": "Grade / level",
        "uk": "Клас / рівень",
    },
    "settings_style": {
        "ru": "Стиль ответа",
        "en": "Response style",
        "uk": "Стиль відповіді",
    },
    "settings_clear_history": {
        "ru": "Очистить историю",
        "en": "Clear history",
        "uk": "Очистити історію",
    },
    "history_cleared": {
        "ru": "История диалога очищена.",
        "en": "Conversation history cleared.",
        "uk": "Історію діалогу очищено.",
    },
    "setting_updated": {
        "ru": "Настройка обновлена!",
        "en": "Setting updated!",
        "uk": "Налаштування оновлено!",
    },
    "thinking": {
        "ru": "Думаю...",
        "en": "Thinking...",
        "uk": "Думаю...",
    },
    "error_image_gen": {
        "ru": "Не удалось сгенерировать изображение. Попробуй позже или измени запрос.",
        "en": "Could not generate the image. Try again later or change your request.",
        "uk": "Не вдалося згенерувати зображення. Спробуй пізніше або зміни запит.",
    },
    "help_text": {
        "ru": "Просто отправь мне:\n• Текст задания\n• Фото задания\n• Фото + подпись\n\nКоманды:\n/settings — настройки\n/clear — очистить историю\n/help — помощь",
        "en": "Just send me:\n• Task text\n• Task photo\n• Photo + caption\n\nCommands:\n/settings — settings\n/clear — clear history\n/help — help",
        "uk": "Просто надішли мені:\n• Текст завдання\n• Фото завдання\n• Фото + підпис\n\nКоманди:\n/settings — налаштування\n/clear — очистити історію\n/help — допомога",
    },
}


def t(key: str, lang: str = "ru", **kwargs) -> str:
    texts = _TEXTS.get(key, {})
    text = texts.get(lang) or texts.get("en") or texts.get("ru", key)
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError):
            pass
    return text
