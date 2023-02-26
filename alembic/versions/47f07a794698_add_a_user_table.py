""" add a user table 

Revision ID: 47f07a794698
Revises: a508a7e6fb0e
Create Date: 2023-02-19 10:57:27.986295

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47f07a794698'
down_revision = 'a508a7e6fb0e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users'
    ,sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
    sa.Column('email',sa.String(),nullable=False),
    sa.Column('password',sa.String(),nullable=False),sa.Column('created_at',sa.TIMESTAMP(timezone=True) ,server_default=sa.text('now()'),nullable=False)
    ,sa.UniqueConstraint('email'))
    pass


def downgrade():
    op.drop_table('users')
    pass
