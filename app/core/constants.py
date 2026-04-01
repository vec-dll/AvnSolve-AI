from enum import StrEnum


class GradeLevel(StrEnum):
    GRADE_1 = "1"
    GRADE_2 = "2"
    GRADE_3 = "3"
    GRADE_4 = "4"
    GRADE_5 = "5"
    GRADE_6 = "6"
    GRADE_7 = "7"
    GRADE_8 = "8"
    GRADE_9 = "9"
    GRADE_10 = "10"
    GRADE_11 = "11"
    STUDENT = "student"
    OTHER = "other"


class ResponseStyle(StrEnum):
    BRIEF = "brief"
    NORMAL = "normal"
    DETAILED = "detailed"


class Intent(StrEnum):
    SOLVE_TASK = "solve_task"
    EXPLAIN_TOPIC = "explain_topic"
    CHECK_ANSWER = "check_answer"
    TRANSLATE = "translate"
    SUMMARIZE = "summarize"
    ANSWER_SHORT = "answer_short"
    ANALYZE_IMAGE_TASK = "analyze_image_task"
    MIXED_REQUEST = "mixed_request"
    GENERAL_QUESTION = "general_question"
    GENERATE_IMAGE = "generate_image"


class AIProvider(StrEnum):
    GEMINI = "gemini"
    GROQ = "groq"


class MessageType(StrEnum):
    TEXT = "text"
    IMAGE = "image"
    IMAGE_TEXT = "image_text"


SUPPORTED_LANGUAGES = {
    "ru": "Русский",
    "uk": "Українська",
    "en": "English",
    "kk": "Қазақша",
    "uz": "O'zbekcha",
    "de": "Deutsch",
    "fr": "Français",
    "es": "Español",
}

GRADE_LABELS = {
    "ru": {
        "1": "1 класс", "2": "2 класс", "3": "3 класс", "4": "4 класс",
        "5": "5 класс", "6": "6 класс", "7": "7 класс", "8": "8 класс",
        "9": "9 класс", "10": "10 класс", "11": "11 класс",
        "student": "Студент", "other": "Другое",
    },
    "en": {
        "1": "Grade 1", "2": "Grade 2", "3": "Grade 3", "4": "Grade 4",
        "5": "Grade 5", "6": "Grade 6", "7": "Grade 7", "8": "Grade 8",
        "9": "Grade 9", "10": "Grade 10", "11": "Grade 11",
        "student": "Student", "other": "Other",
    },
    "uk": {
        "1": "1 клас", "2": "2 клас", "3": "3 клас", "4": "4 клас",
        "5": "5 клас", "6": "6 клас", "7": "7 клас", "8": "8 клас",
        "9": "9 клас", "10": "10 клас", "11": "11 клас",
        "student": "Студент", "other": "Інше",
    },
}

STYLE_LABELS = {
    "ru": {"brief": "Кратко", "normal": "Обычно", "detailed": "Подробно"},
    "en": {"brief": "Brief", "normal": "Normal", "detailed": "Detailed"},
    "uk": {"brief": "Коротко", "normal": "Звичайно", "detailed": "Детально"},
}
