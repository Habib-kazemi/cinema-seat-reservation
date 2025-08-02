"""Change seat_number to position_id in reservation

Revision ID: 2f76c3d8c6cf
Revises: c5875efbb2db
Create Date: 2025-07-31 18:30:17.986633

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = '2f76c3d8c6cf'
down_revision = 'c5875efbb2db'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('reservation', sa.Column('position_id', sa.Integer, sa.ForeignKey(
        'hall_position.id'), nullable=False))
    op.drop_column('reservation', 'seat_number')


def downgrade():
    op.add_column('reservation', sa.Column(
        'seat_number', sa.String(10), nullable=False))
    op.drop_column('reservation', 'position_id')
