"""compartilhamento de cadernos

Revision ID: 0005
Revises: 0004
Create Date: 2026-09-08

"""
import sqlalchemy as sa
from alembic import op

revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "notebook_shares",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "notebook_id", sa.Integer(), sa.ForeignKey("notebooks.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column(
            "shared_with_user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column("permission", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.UniqueConstraint("notebook_id", "shared_with_user_id", name="uq_notebook_shares_notebook_user"),
    )
    op.create_index("ix_notebook_shares_notebook_id", "notebook_shares", ["notebook_id"])
    op.create_index("ix_notebook_shares_shared_with_user_id", "notebook_shares", ["shared_with_user_id"])


def downgrade() -> None:
    op.drop_index("ix_notebook_shares_shared_with_user_id", table_name="notebook_shares")
    op.drop_index("ix_notebook_shares_notebook_id", table_name="notebook_shares")
    op.drop_table("notebook_shares")
