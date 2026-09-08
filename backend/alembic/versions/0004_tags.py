"""tags e associacao com cadernos

Revision ID: 0004
Revises: 0003
Create Date: 2026-09-08

"""
import sqlalchemy as sa
from alembic import op

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tags",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.UniqueConstraint("user_id", "name", name="uq_tags_user_id_name"),
    )
    op.create_index("ix_tags_user_id", "tags", ["user_id"])

    op.create_table(
        "notebook_tags",
        sa.Column(
            "notebook_id", sa.Integer(), sa.ForeignKey("notebooks.id", ondelete="CASCADE"), primary_key=True
        ),
        sa.Column("tag_id", sa.Integer(), sa.ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
    )


def downgrade() -> None:
    op.drop_table("notebook_tags")
    op.drop_index("ix_tags_user_id", table_name="tags")
    op.drop_table("tags")
