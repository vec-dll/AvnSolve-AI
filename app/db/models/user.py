from datetime import datetime

from sqlalchemy import BigInteger, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    first_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ui_language: Mapped[str] = mapped_column(String(10), default="ru")
    grade_level: Mapped[str | None] = mapped_column(String(20), nullable=True)
    response_style: Mapped[str] = mapped_column(String(20), default="normal")
    last_message_language: Mapped[str | None] = mapped_column(String(10), nullable=True)
    onboarding_complete: Mapped[bool] = mapped_column(default=False)
    onboarding_step: Mapped[str | None] = mapped_column(String(50), nullable=True)
    is_blocked: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    messages: Mapped[list["Message"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User telegram_id={self.telegram_id}>"
