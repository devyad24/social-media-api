"""add content column to posts table

Revision ID: 286bc3b0741b
Revises: 2b106266e0a3
Create Date: 2022-11-14 13:52:31.005557

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '286bc3b0741b'
down_revision = '2b106266e0a3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
