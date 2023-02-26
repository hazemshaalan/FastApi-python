""" add content to posts table 

Revision ID: a508a7e6fb0e
Revises: d87d84fd6965 ---> the previous version 
Create Date: 2023-02-19 10:41:57.181494

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a508a7e6fb0e'
down_revision = 'd87d84fd6965'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
     #---> every time you upgrade you need to downgrade 
     op.drop_column('posts','content')
     pass
