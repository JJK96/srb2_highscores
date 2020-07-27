"""Magma Mine map setup

Revision ID: e6baa6897cd7
Revises: 2c270d6d437e
Create Date: 2020-07-27 18:43:38.212560

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e6baa6897cd7'
down_revision = '2c270d6d437e'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("update maps set image = 'magma_mine.jpg' where id = 932")
    op.execute("update maps set votes = 0 where id = 932")
    op.alter_column('maps', 'votes',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)


def downgrade():
    pass
