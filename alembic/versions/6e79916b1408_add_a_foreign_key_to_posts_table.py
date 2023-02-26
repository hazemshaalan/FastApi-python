""" add a foreign key to posts table

Revision ID: 6e79916b1408
Revises: 47f07a794698
Create Date: 2023-02-19 11:25:06.017789

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e79916b1408'
down_revision = '47f07a794698'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('posts_users_fk',source_table="posts",referent_table='users',local_cols=["owner_id"],remote_cols=["id"]
    ,ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint("posts_users_fk",table_name="posts")#---> to remove only the forign key 
    op.drop_column("posts","owner_id")
    pass
