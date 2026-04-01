from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.repositories.message_repo import MessageRepository


class HistoryService:
    def __init__(self, session: AsyncSession):
        self.repo = MessageRepository(session)

    async def save_user_message(
        self,
        user_id: int,
        text: str | None,
        message_type: str,
        image_file_id: str | None = None,
        language: str | None = None,
        intent: str | None = None,
    ) -> None:
        await self.repo.add(
            user_id=user_id,
            role="user",
            message_type=message_type,
            text=text,
            image_file_id=image_file_id,
            language=language,
            intent=intent,
        )

    async def save_assistant_message(
        self,
        user_id: int,
        text: str,
        ai_provider: str | None = None,
        response_time_ms: int | None = None,
    ) -> None:
        await self.repo.add(
            user_id=user_id,
            role="assistant",
            message_type="text",
            text=text,
            ai_provider=ai_provider,
            response_time_ms=response_time_ms,
        )

    async def get_context(self, user_id: int) -> list[dict]:
        messages = await self.repo.get_recent(
            user_id, limit=settings.max_context_messages
        )
        context = []
        for msg in messages:
            if msg.text:
                context.append({"role": msg.role, "content": msg.text})
        return context

    async def clear(self, user_id: int) -> int:
        return await self.repo.clear_history(user_id)
