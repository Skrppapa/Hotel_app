"""user email add Unique

Revision ID: 0391ce95d1ec
Revises: af48b6607f2c
Create Date: 2026-03-28 21:39:12.060380

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0391ce95d1ec"
down_revision: Union[str, Sequence[str], None] = "af48b6607f2c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "users", type_="unique")
