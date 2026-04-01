import logging
import time

from groq import AsyncGroq

from app.core.config import settings

logger = logging.getLogger(__name__)

_client = AsyncGroq(api_key=settings.groq_api_key)

MODEL = "llama-3.3-70b-versatile"


async def generate_text(
    messages: list[dict],
    temperature: float = 0.4,
) -> tuple[str, int]:
    start = time.monotonic()
    try:
        response = await _client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=4096,
        )

        elapsed_ms = int((time.monotonic() - start) * 1000)
        text = response.choices[0].message.content or ""
        logger.info("Groq response in %dms, %d chars", elapsed_ms, len(text))
        return text, elapsed_ms

    except Exception as exc:
        elapsed_ms = int((time.monotonic() - start) * 1000)
        logger.exception("Groq text generation failed after %dms", elapsed_ms)
        raise exc
