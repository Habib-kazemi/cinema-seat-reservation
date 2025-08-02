"""Add Hall_position table

Revision ID: c5875efbb2db
Revises: 
Create Date: 2025-07-31 17:46:33.366516

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5875efbb2db'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'hall_position',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('hall_id', sa.Integer, sa.ForeignKey(
            'hall.id', ondelete='CASCADE'), nullable=False),
        sa.Column('row_index', sa.Integer, nullable=False),
        sa.Column('column_index', sa.Integer, nullable=False),
    )


def downgrade():
    op.drop_table('hall_position')
