from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.message import Message


class MessageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, **kwargs) -> Message:
        msg = Message(**kwargs)
        self.session.add(msg)
        await self.session.commit()
        return msg

    async def get_recent(self, user_id: int, limit: int = 12) -> list[Message]:
        stmt = (
            select(Message)
            .where(Message.user_id == user_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        messages = list(result.scalars().all())
        messages.reverse()
        return messages

    async def clear_history(self, user_id: int) -> int:
        stmt = delete(Message).where(Message.user_id == user_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount
