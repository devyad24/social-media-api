"""add foreign-key to post table

Revision ID: 00f08f0b2fff
Revises: 371734da485b
Create Date: 2022-11-14 14:14:02.919549

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00f08f0b2fff'
down_revision = '371734da485b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name="posts")
    op.drop_column('posts','owner_id')
    pass
