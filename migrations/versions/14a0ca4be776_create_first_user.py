"""create first user

Revision ID: 14a0ca4be776
Revises: e58ddd96285e
Create Date: 2026-03-07 18:36:08.154868

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session  
from app.api.modules.tables import User
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = '14a0ca4be776'
down_revision: Union[str, Sequence[str], None] = 'e58ddd96285e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    admin = User(
        username="admin",
        email="admin@example.com",
        password="hashed_passworSuperSecure123d",
        registration_date=datetime.utcnow()
    )

    session.add(admin)
    session.commit()

def downgrade():
    pass