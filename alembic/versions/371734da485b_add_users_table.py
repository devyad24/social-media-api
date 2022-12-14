"""add users table

Revision ID: 371734da485b
Revises: 286bc3b0741b
Create Date: 2022-11-14 14:01:46.040513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '371734da485b'
down_revision = '286bc3b0741b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                                server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    pass
