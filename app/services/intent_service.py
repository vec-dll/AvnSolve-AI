import re

from app.core.constants import Intent

_IMAGE_GEN_PATTERN = re.compile(
    r"нарисуй|нарисовать|сгенерируй|сгенерировать|создай\s+(картинк|изображен|рисунок)"
    r"|generate\s+(image|picture|drawing)"
    r"|draw\s+(me|a|an|the)\b"
    r"|намалюй|створи\s+(зображення|картинк)",
    re.I,
)

_PATTERNS: list[tuple[re.Pattern, Intent]] = [
    (re.compile(r"провер[ьи]|check\s+(my|the)\s+answer|перевір", re.I), Intent.CHECK_ANSWER),
    (re.compile(r"перевед|translat|переклад", re.I), Intent.TRANSLATE),
    (re.compile(r"кратко|коротко|конспект|summarize|summary|brief", re.I), Intent.SUMMARIZE),
    (re.compile(r"только\s+ответ|just\s+answer|без\s+объяснен|no\s+explain", re.I), Intent.ANSWER_SHORT),
    (re.compile(r"объясн[ии]|explain|поясн[ии]|розкаж|what\s+is|что\s+тако", re.I), Intent.EXPLAIN_TOPIC),
    (re.compile(r"реш[ии]|solve|вирішити|найд[ии]|calculat|вычисл|посчитай", re.I), Intent.SOLVE_TASK),
]


def classify_intent(
    text: str | None,
    has_image: bool = False,
    has_caption: bool = False,
) -> Intent:
    if has_image and not text and not has_caption:
        return Intent.ANALYZE_IMAGE_TASK

    if has_image and (text or has_caption):
        return Intent.MIXED_REQUEST

    if not text:
        return Intent.GENERAL_QUESTION

    if _IMAGE_GEN_PATTERN.search(text):
        return Intent.GENERATE_IMAGE

    for pattern, intent in _PATTERNS:
        if pattern.search(text):
            return intent

    return Intent.SOLVE_TASK
