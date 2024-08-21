"""ADD tarots table

Revision ID: d81ed4a40859
Revises: 
Create Date: 2024-08-21 00:29:20.655315

"""
from datetime import datetime, timedelta, timezone
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd81ed4a40859'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'tarots',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(31), nullable=False),
        sa.Column('description', sa.String(2047), nullable=False),
        sa.Column('good_words', sa.String(255), nullable=False),
        sa.Column('bad_words', sa.String(255), nullable=False),
        sa.Column('tarot_id', sa.Integer, nullable=False, unique=True),
        sa.Column('img_url', sa.String(1023), nullable=False),
        sa.Column('created_dt', sa.DateTime, default=lambda: datetime.now(timezone(timedelta(hours=9)))),
        sa.Column('updated_dt', sa.DateTime, default=lambda: datetime.now(timezone(timedelta(hours=9))), onupdate=lambda: datetime.now(timezone(timedelta(hours=9)))),
    )


def downgrade() -> None:
    op.drop_table('tarots')
