"""add role to users

Revision ID: add_role_to_users
Revises: 14a0ca4be776
Create Date: 2026-03-08 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_role_to_users'
down_revision: Union[str, Sequence[str], None] = '14a0ca4be776'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add role column to users table."""
    # Add role column with default value 'user'
    op.add_column('users', sa.Column('role', sa.String(), nullable=False, server_default='user'))


def downgrade() -> None:
    """Remove role column from users table."""
    op.drop_column('users', 'role')
