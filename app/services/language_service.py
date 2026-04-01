import logging

from langdetect import detect, detect_langs, LangDetectException

logger = logging.getLogger(__name__)

_LANG_NAMES = {
    "ru": "Russian",
    "uk": "Ukrainian",
    "en": "English",
    "kk": "Kazakh",
    "uz": "Uzbek",
    "de": "German",
    "fr": "French",
    "es": "Spanish",
    "tr": "Turkish",
    "ar": "Arabic",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "pl": "Polish",
    "pt": "Portuguese",
    "it": "Italian",
}

_LANG_MAP = {
    "zh-cn": "zh",
    "zh-tw": "zh",
}

# Languages that langdetect confuses with each other on short texts
# mk (Macedonian), bg (Bulgarian) are often confused with ru/uk
_CYRILLIC_FALLBACK = {"mk", "bg", "sr"}

# Minimum word count for reliable detection
_MIN_WORDS_FOR_DETECTION = 3


def detect_language(text: str, ui_language: str | None = None) -> str | None:
    if not text or len(text.strip()) < 2:
        return None

    words = text.strip().split()

    try:
        raw = detect(text)
        lang = _LANG_MAP.get(raw, raw)

        # Short messages: langdetect unreliable for Cyrillic scripts
        # "привет" -> mk, "как дела" -> bg, etc.
        if len(words) < _MIN_WORDS_FOR_DETECTION and lang in _CYRILLIC_FALLBACK:
            if ui_language and ui_language in ("ru", "uk"):
                logger.debug(
                    "Short text '%s' detected as %s, using ui_language=%s instead",
                    text[:30], lang, ui_language,
                )
                return ui_language
            return "ru"

        return lang

    except LangDetectException:
        logger.debug("Could not detect language for text: %s...", text[:50])
        return None


def get_response_language(
    detected: str | None,
    last_message_language: str | None,
    ui_language: str,
) -> str:
    if detected:
        return detected
    if last_message_language:
        return last_message_language
    return ui_language


def get_language_name(code: str) -> str:
    return _LANG_NAMES.get(code, code)
