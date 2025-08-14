"""Change seat_number to position_id in reservation

Revision ID: 2f76c3d8c6cf
Revises: c5875efbb2db
Create Date: 2025-07-31 18:30:17.986633

"""

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = '2f76c3d8c6cf'
down_revision = 'c5875efbb2db'
branch_labels = None
depends_on = None


def upgrade():
    # Check if position_id already exists
    inspector = sa.inspect(op.get_context().connection)
    columns = [col['name'] for col in inspector.get_columns('reservation')]

    # If seat_number exists, rename or drop it
    if 'seat_number' in columns:
        if 'position_id' not in columns:
            op.alter_column('reservation', 'seat_number',
                            new_column_name='position_id')
        else:
            op.drop_column('reservation', 'seat_number')

    # Ensure position_id exists with correct definition
    if 'position_id' not in columns:
        op.add_column('reservation',
                      sa.Column('position_id', sa.Integer(), sa.ForeignKey(
                          'hall_position.id'), nullable=False)
                      )

    # Ensure foreign key constraint exists
    if not any(fk['constrained_columns'] == ['position_id'] for fk in inspector.get_foreign_keys('reservation')):
        op.create_foreign_key(
            'reservation_position_id_fkey',
            'reservation',
            'hall_position',
            ['position_id'],
            ['id'],
            ondelete='CASCADE'
        )


def downgrade():
    inspector = sa.inspect(op.get_context().connection)
    columns = [col['name'] for col in inspector.get_columns('reservation')]

    # Drop position_id if it was added
    if 'position_id' in columns:
        op.drop_column('reservation', 'position_id')

    # Recreate seat_number if it was dropped
    if 'seat_number' not in columns:
        op.add_column('reservation', sa.Column(
            'seat_number', sa.Integer(), nullable=False))
