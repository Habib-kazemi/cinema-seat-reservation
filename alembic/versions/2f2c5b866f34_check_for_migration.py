"""Check for migration

Revision ID: 2f2c5b866f34
Revises: 6a2090c5ddb5
Create Date: 2025-08-09 15:13:13.819606

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = '2f2c5b866f34'
down_revision: Union[str, Sequence[str], None] = '6a2090c5ddb5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Check if index ix_users_id exists before dropping
    inspector = sa.inspect(op.get_context().connection)
    indexes = [idx['name'] for idx in inspector.get_indexes('user')]
    if 'ix_users_id' in indexes:
        op.drop_index(op.f('ix_users_id'), table_name='user')


def downgrade():
    # Recreate index if it was dropped
    op.create_index(op.f('ix_users_id'), 'user', ['id'], unique=False)
