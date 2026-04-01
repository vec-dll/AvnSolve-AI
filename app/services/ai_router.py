import logging

from app.core.constants import AIProvider, Intent
from app.schemas.user import AIRequest
from app.services import gemini_service, groq_service
from app.services.prompt_service import build_system_prompt, build_context_messages

logger = logging.getLogger(__name__)


def choose_provider(request: AIRequest) -> AIProvider:
    if request.image_path:
        return AIProvider.GEMINI
    return AIProvider.GROQ


async def get_ai_response(request: AIRequest) -> tuple[str, AIProvider, int]:
    provider = choose_provider(request)

    system_prompt = build_system_prompt(
        response_language=request.detected_language or request.user_profile.ui_language,
        grade_level=request.user_profile.grade_level,
        response_style=request.user_profile.response_style,
        intent=request.intent or Intent.GENERAL_QUESTION,
    )

    user_text = request.text or request.image_caption or ""

    context = list(request.context_messages)
    if user_text:
        context.append({"role": "user", "content": user_text})

    messages = build_context_messages(context, system_prompt)

    if provider == AIProvider.GEMINI:
        try:
            if request.image_path:
                text, ms = await gemini_service.generate_with_image(messages, request.image_path)
            else:
                text, ms = await gemini_service.generate_text(messages)
            return text, AIProvider.GEMINI, ms
        except Exception:
            logger.warning("Gemini failed, trying Groq fallback")
            if request.image_path:
                raise
            try:
                text, ms = await groq_service.generate_text(messages)
                return text, AIProvider.GROQ, ms
            except Exception:
                raise
    else:
        try:
            text, ms = await groq_service.generate_text(messages)
            return text, AIProvider.GROQ, ms
        except Exception:
            logger.warning("Groq failed, trying Gemini fallback")
            try:
                text, ms = await gemini_service.generate_text(messages)
                return text, AIProvider.GEMINI, ms
            except Exception:
                raise
