from datetime import datetime

from sqlalchemy import BigInteger, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    role: Mapped[str] = mapped_column(String(20))  # user / assistant
    message_type: Mapped[str] = mapped_column(String(20))  # text / image / image_text
    text: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_file_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ai_provider: Mapped[str | None] = mapped_column(String(20), nullable=True)
    intent: Mapped[str | None] = mapped_column(String(50), nullable=True)
    language: Mapped[str | None] = mapped_column(String(10), nullable=True)
    response_time_ms: Mapped[int | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="messages")

    def __repr__(self) -> str:
        return f"<Message id={self.id} role={self.role}>"
