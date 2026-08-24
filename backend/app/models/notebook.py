from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.domain.enums import PageMode

if TYPE_CHECKING:
    from app.models.page import Page
    from app.models.user import User


class Notebook(Base):
    __tablename__ = "notebooks"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    page_mode: Mapped[PageMode] = mapped_column(
        SAEnum(PageMode, native_enum=False, length=20),
        default=PageMode.CONTINUOUS,
        nullable=False,
    )
    line_color: Mapped[str] = mapped_column(String(20), default="#9db3c8", nullable=False)
    line_spacing: Mapped[int] = mapped_column(default=28, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    owner: Mapped["User"] = relationship(back_populates="notebooks")
    pages: Mapped[list["Page"]] = relationship(
        back_populates="notebook", cascade="all, delete-orphan", order_by="Page.position"
    )
