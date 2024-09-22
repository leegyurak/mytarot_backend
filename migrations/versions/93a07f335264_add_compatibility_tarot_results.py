"""add_compatibility_tarot_results

Revision ID: 93a07f335264
Revises: d81ed4a40859
Create Date: 2024-09-23 04:16:55.530514

"""
from datetime import datetime, timezone, timedelta
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '93a07f335264'
down_revision: Union[str, None] = 'd81ed4a40859'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'compatibility_tarot_results',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('first_tarot_id', sa.Integer, nullable=False),
        sa.Column('second_tarot_id', sa.Integer, nullable=False),
        sa.Column('commentary', sa.String(length=4095), nullable=False),
        sa.UniqueConstraint('first_tarot_id', 'second_tarot_id', name='uq_first_second_tarot'),
        sa.Column('created_dt', sa.DateTime, default=lambda: datetime.now(timezone(timedelta(hours=9)))),
        sa.Column('updated_dt', sa.DateTime, default=lambda: datetime.now(timezone(timedelta(hours=9))), onupdate=lambda: datetime.now(timezone(timedelta(hours=9)))),
    )


def downgrade() -> None:
    op.drop_table('compatibility_tarot_results')
