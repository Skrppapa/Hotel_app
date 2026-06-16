"""Add users

Revision ID: af48b6607f2c
Revises: ce1da5dc189a
Create Date: 2026-03-28 20:10:42.701038

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "af48b6607f2c"
down_revision: Union[str, Sequence[str], None] = "ce1da5dc189a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")