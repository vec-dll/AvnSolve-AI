from app.core.constants import Intent, ResponseStyle
from app.services.language_service import get_language_name

_STYLE_INSTRUCTION = {
    ResponseStyle.BRIEF: "Отвечай максимально кратко. Только ключевой результат и минимум пояснений.",
    ResponseStyle.NORMAL: "Давай понятный структурированный ответ с решением по шагам и коротким объяснением.",
    ResponseStyle.DETAILED: "Давай подробный развёрнутый ответ. Объясняй каждый шаг, добавляй примеры.",
}

_INTENT_INSTRUCTION = {
    Intent.SOLVE_TASK: "Реши задачу по шагам. Покажи ход решения и финальный ответ.",
    Intent.EXPLAIN_TOPIC: "Объясни тему понятно и просто, с примерами.",
    Intent.CHECK_ANSWER: "Проверь ответ пользователя. Укажи ошибки, объясни где и почему ошибка, покажи правильное решение.",
    Intent.TRANSLATE: "Переведи текст точно и грамотно.",
    Intent.SUMMARIZE: "Дай краткий конспект / резюме.",
    Intent.ANSWER_SHORT: "Дай только финальный ответ, без объяснений.",
    Intent.ANALYZE_IMAGE_TASK: "Проанализируй изображение. Определи задание и реши его.",
    Intent.MIXED_REQUEST: "Используй изображение и текст пользователя вместе для ответа.",
    Intent.GENERAL_QUESTION: "Ответь на вопрос полезно и по существу.",
}


def build_system_prompt(
    response_language: str,
    grade_level: str | None,
    response_style: str,
    intent: str,
) -> str:
    lang_name = get_language_name(response_language)
    style_instr = _STYLE_INSTRUCTION.get(response_style, _STYLE_INSTRUCTION[ResponseStyle.NORMAL])
    intent_instr = _INTENT_INSTRUCTION.get(intent, _INTENT_INSTRUCTION[Intent.GENERAL_QUESTION])

    grade_part = ""
    if grade_level:
        if grade_level == "student":
            grade_part = "Пользователь — студент. Используй соответствующий академический уровень."
        elif grade_level == "other":
            grade_part = "Подстраивайся под видимый уровень пользователя."
        else:
            grade_part = f"Пользователь учится в {grade_level} классе. Объясняй на подходящем уровне для этого класса."

    return f"""Ты — учебный ассистент. Твоя задача — помогать ученикам с учёбой.

ЯЗЫК ОТВЕТА:
- По умолчанию отвечай на: {lang_name} ({response_language}).
- Если пользователь ЯВНО просит ответить на другом языке (например "ответь на украинском", "answer in English") — отвечай на том языке, который он просит. Просьба пользователя о языке важнее правила по умолчанию.

ПРАВИЛА ОТВЕТА:
- {style_instr}
- {intent_instr}
- {grade_part}
- Не выдумывай данные, которых нет в вопросе или на изображении.
- Если изображение нечёткое — скажи какую часть не видно и реши то, что видно.
- Если пользователь просит проверить ответ — сравни логически и укажи на ошибки.
- Для младших классов объясняй проще, для старших — более формально.
- Если пользователь просто здоровается — поздоровайся в ответ коротко и предложи помощь с учёбой.
- Не добавляй лишних дисклеймеров. Переходи сразу к делу.
- Используй форматирование: жирный текст, списки, нумерацию для наглядности."""


def build_context_messages(
    history: list[dict],
    system_prompt: str,
) -> list[dict]:
    messages = [{"role": "system", "content": system_prompt}]
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    return messages
