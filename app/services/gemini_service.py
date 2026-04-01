import logging
import time
from pathlib import Path

from google import genai
from google.genai import types

from app.core.config import settings

logger = logging.getLogger(__name__)

_client = genai.Client(api_key=settings.gemini_api_key)

MODEL = "gemini-2.0-flash"


async def generate_text(
    messages: list[dict],
    temperature: float = 0.4,
) -> tuple[str, int]:
    start = time.monotonic()
    try:
        system_text = ""
        contents = []
        for msg in messages:
            if msg["role"] == "system":
                system_text = msg["content"]
            else:
                role = "user" if msg["role"] == "user" else "model"
                contents.append(types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=msg["content"])],
                ))

        config = types.GenerateContentConfig(
            system_instruction=system_text if system_text else None,
            temperature=temperature,
            max_output_tokens=4096,
        )

        response = await _client.aio.models.generate_content(
            model=MODEL,
            contents=contents,
            config=config,
        )

        elapsed_ms = int((time.monotonic() - start) * 1000)
        text = response.text or ""
        logger.info("Gemini response in %dms, %d chars", elapsed_ms, len(text))
        return text, elapsed_ms

    except Exception as exc:
        elapsed_ms = int((time.monotonic() - start) * 1000)
        logger.exception("Gemini text generation failed after %dms", elapsed_ms)
        raise exc


async def generate_with_image(
    messages: list[dict],
    image_path: str,
    temperature: float = 0.4,
) -> tuple[str, int]:
    start = time.monotonic()
    try:
        system_text = ""
        contents = []
        for msg in messages:
            if msg["role"] == "system":
                system_text = msg["content"]
            elif msg["role"] == "user":
                contents.append(types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=msg["content"])],
                ))
            else:
                contents.append(types.Content(
                    role="model",
                    parts=[types.Part.from_text(text=msg["content"])],
                ))

        image_bytes = Path(image_path).read_bytes()
        suffix = Path(image_path).suffix.lower()
        mime_map = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp", ".gif": "image/gif"}
        mime = mime_map.get(suffix, "image/jpeg")

        last_user_text = ""
        if contents and contents[-1].role == "user":
            last_content = contents.pop()
            last_user_text = last_content.parts[0].text if last_content.parts else ""

        contents.append(types.Content(
            role="user",
            parts=[
                types.Part.from_bytes(data=image_bytes, mime_type=mime),
                types.Part.from_text(text=last_user_text or "Analyze this image and solve the task shown."),
            ],
        ))

        config = types.GenerateContentConfig(
            system_instruction=system_text if system_text else None,
            temperature=temperature,
            max_output_tokens=4096,
        )

        response = await _client.aio.models.generate_content(
            model=MODEL,
            contents=contents,
            config=config,
        )

        elapsed_ms = int((time.monotonic() - start) * 1000)
        text = response.text or ""
        logger.info("Gemini image response in %dms, %d chars", elapsed_ms, len(text))
        return text, elapsed_ms

    except Exception as exc:
        elapsed_ms = int((time.monotonic() - start) * 1000)
        logger.exception("Gemini image generation failed after %dms", elapsed_ms)
        raise exc


IMAGE_MODEL = "gemini-2.0-flash-exp-image-generation"


async def generate_image(prompt: str) -> tuple[bytes | None, str | None, int]:
    """Generate an image using Gemini. Returns (image_bytes, text_response, elapsed_ms)."""
    start = time.monotonic()
    try:
        response = await _client.aio.models.generate_content(
            model=IMAGE_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
            ),
        )

        elapsed_ms = int((time.monotonic() - start) * 1000)

        image_bytes = None
        text_response = None

        if response.candidates:
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    image_bytes = part.inline_data.data
                elif part.text:
                    text_response = part.text

        logger.info("Gemini image gen in %dms, got_image=%s", elapsed_ms, image_bytes is not None)
        return image_bytes, text_response, elapsed_ms

    except Exception as exc:
        elapsed_ms = int((time.monotonic() - start) * 1000)
        logger.exception("Gemini image gen failed after %dms", elapsed_ms)
        raise exc
