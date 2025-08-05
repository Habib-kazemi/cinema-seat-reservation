"""rename users table to user

Revision ID: 6a2090c5ddb5
Revises: 2f76c3d8c6cf
Create Date: 2025-08-05 20:01:25.961826

"""

from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = '6a2090c5ddb5'
down_revision: Union[str, Sequence[str], None] = '2f76c3d8c6cf'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('users', 'user')
    op.drop_constraint('reservation_user_id_fkey',
                       'reservation', type_='foreignkey')
    op.create_foreign_key(
        'reservation_user_id_fkey',
        'reservation',
        'user',
        ['user_id'],
        ['id'],
        ondelete='CASCADE'
    )


def downgrade():
    op.drop_constraint('reservation_user_id_fkey',
                       'reservation', type_='foreignkey')
    op.create_foreign_key(
        'reservation_user_id_fkey',
        'reservation',
        'users',
        ['user_id'],
        ['id'],
        ondelete='CASCADE'
    )
    op.rename_table('user', 'users')
