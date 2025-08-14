"""Add Hall_position table

Revision ID: c5875efbb2db
Revises: 
Create Date: 2025-07-31 17:46:33.366516

"""

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = 'c5875efbb2db'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Check if hall_position table exists, and only add missing columns
    if not op.get_context().dialect.has_table(op.get_context().connection, 'hall_position'):
        op.create_table(
            'hall_position',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('hall_id', sa.Integer(), nullable=False),
            sa.Column('row_index', sa.Integer(), nullable=False),
            sa.Column('column_index', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(
                ['hall_id'], ['hall.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )
    else:
        # Add missing columns if table exists
        inspector = sa.inspect(op.get_context().connection)
        columns = [col['name']
                   for col in inspector.get_columns('hall_position')]
        if 'row_index' not in columns:
            op.add_column('hall_position', sa.Column(
                'row_index', sa.Integer(), nullable=False))
        if 'column_index' not in columns:
            op.add_column('hall_position', sa.Column(
                'column_index', sa.Integer(), nullable=False))


def downgrade():
    # Drop columns if they were added
    inspector = sa.inspect(op.get_context().connection)
    columns = [col['name'] for col in inspector.get_columns('hall_position')]
    if 'row_index' in columns:
        op.drop_column('hall_position', 'row_index')
    if 'column_index' in columns:
        op.drop_column('hall_position', 'column_index')
    # Only drop table if it was created in this migration
    if op.get_context().dialect.has_table(op.get_context().connection, 'hall_position'):
        op.drop_table('hall_position')
