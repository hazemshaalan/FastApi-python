""" add last few columns to posts table 

Revision ID: f71bba577e5d
Revises: 6e79916b1408
Create Date: 2023-02-19 11:36:14.796583

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f71bba577e5d'
down_revision = '6e79916b1408'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('published',sa.Boolean(),nullable=False,server_default="TRUE"),
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text("now()"))))
    pass


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')

    pass
