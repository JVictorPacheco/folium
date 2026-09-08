from sqlalchemy import Column, ForeignKey, Table

from app.core.database import Base

notebook_tags = Table(
    "notebook_tags",
    Base.metadata,
    Column("notebook_id", ForeignKey("notebooks.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)
