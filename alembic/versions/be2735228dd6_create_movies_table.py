"""create movies table

Revision ID: be2735228dd6
Revises: fa63f93f1835
Create Date: 2024-06-06 07:00:25.003104

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'be2735228dd6'
down_revision: Union[str, None] = 'fa63f93f1835'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = ['fa63f93f1835']


def upgrade():
    op.create_table(
        'movies',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('description', sa.String, nullable=True),
        sa.Column('director', sa.String, nullable=True),
        sa.Column('year', sa.Integer, nullable=True),
        sa.Column('genre', sa.String, nullable=True),
        sa.Column('rating', sa.Float, nullable=True),
        sa.Column('is_public', sa.Boolean, default=False, nullable=False),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime, default=sa.func.current_timestamp(), nullable=False)
    )

def downgrade():
    op.drop_table('movies')
