"""add broadcast to movies table

Revision ID: aac7617d63bd
Revises: be2735228dd6
Create Date: 2024-06-06 08:06:06.219357

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aac7617d63bd'
down_revision: Union[str, None] = 'be2735228dd6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = ['be2735228dd6']


def upgrade():
    # Add new columns
    op.add_column('movies', sa.Column('broadcast', sa.String, nullable=True))
    op.add_column('movies', sa.Column('area_location', sa.String, nullable=True))
    op.add_column('movies', sa.Column('localtime', sa.String, nullable=True))
    op.add_column('movies', sa.Column('utc_datetime', sa.String, nullable=True))
    op.add_column('movies', sa.Column('utc_offset', sa.String, nullable=True))

def downgrade():
    # Drop the columns in the reverse order
    op.drop_column('movies', 'utc_offset')
    op.drop_column('movies', 'utc_datetime')
    op.drop_column('movies', 'localtime')
    op.drop_column('movies', 'area_location')
    op.drop_column('movies', 'broadcast')
