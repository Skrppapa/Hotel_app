from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "adcf61a0c60f"
down_revision: Union[str, Sequence[str], None] = "0391ce95d1ec"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass



def downgrade() -> None:
    """Downgrade schema."""
    pass

