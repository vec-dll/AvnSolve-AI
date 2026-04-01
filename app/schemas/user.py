from pydantic import BaseModel

from app.core.constants import ResponseStyle


class UserProfile(BaseModel):
    telegram_id: int
    username: str | None = None
    first_name: str | None = None
    ui_language: str = "ru"
    grade_level: str | None = None
    response_style: str = ResponseStyle.NORMAL
    last_message_language: str | None = None
    onboarding_complete: bool = False


class AIRequest(BaseModel):
    user_profile: UserProfile
    text: str | None = None
    image_path: str | None = None
    image_caption: str | None = None
    intent: str | None = None
    detected_language: str | None = None
    context_messages: list[dict] = []
