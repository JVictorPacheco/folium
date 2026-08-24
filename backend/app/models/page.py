from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, JSONType

if TYPE_CHECKING:
    from app.models.notebook import Notebook


class Page(Base):
    __tablename__ = "pages"

    id: Mapped[int] = mapped_column(primary_key=True)
    notebook_id: Mapped[int] = mapped_column(
        ForeignKey("notebooks.id", ondelete="CASCADE"), index=True, nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), default="Sem título", nullable=False)
    position: Mapped[int] = mapped_column(default=0, nullable=False)
    content_json: Mapped[dict] = mapped_column(JSONType, default=dict, nullable=False)
    revision: Mapped[int] = mapped_column(default=1, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    notebook: Mapped["Notebook"] = relationship(back_populates="pages")
