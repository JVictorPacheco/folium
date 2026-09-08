from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.domain.enums import SharePermission

if TYPE_CHECKING:
    from app.models.notebook import Notebook
    from app.models.user import User


class NotebookShare(Base):
    __tablename__ = "notebook_shares"
    __table_args__ = (
        UniqueConstraint("notebook_id", "shared_with_user_id", name="uq_notebook_shares_notebook_user"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    notebook_id: Mapped[int] = mapped_column(
        ForeignKey("notebooks.id", ondelete="CASCADE"), index=True, nullable=False
    )
    shared_with_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    permission: Mapped[SharePermission] = mapped_column(
        SAEnum(SharePermission, native_enum=False, length=20), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    notebook: Mapped["Notebook"] = relationship()
    shared_with: Mapped["User"] = relationship()
