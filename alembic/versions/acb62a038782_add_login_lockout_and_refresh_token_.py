"""Add login lockout and refresh token fields to users

Revision ID: acb62a038782
Revises: 3b7ec8540645
Create Date: 2026-08-15 17:14:23.939860

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'acb62a038782'
down_revision: Union[str, Sequence[str], None] = '3b7ec8540645'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
