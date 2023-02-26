""" create posts table 

Revision ID: d87d84fd6965
Revises: 
Create Date: 2023-02-17 19:46:53.874956

"""
from alembic import op

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd87d84fd6965'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts",sa.Column("id",sa.Integer(),nullable=False,primary_key=True)
   ,sa.Column("title",sa.String(),nullable=False) )
    pass


def downgrade():
    op.drop_table("posts")
    pass
