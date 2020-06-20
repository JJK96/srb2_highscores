"""Image as string

Revision ID: 1719107d71a6
Revises: d1a0a1316d53
Create Date: 2020-06-20 19:35:32.272896

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1719107d71a6'
down_revision = 'd1a0a1316d53'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("alter table maps modify image TEXT")


def downgrade():
    pass
