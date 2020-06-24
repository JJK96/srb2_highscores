"""In rotation

Revision ID: 2c270d6d437e
Revises: 1719107d71a6
Create Date: 2020-06-24 16:51:16.838087

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c270d6d437e'
down_revision = '1719107d71a6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('maps', sa.Column('in_rotation', sa.Integer(), nullable=False, default=1))
    op.execute("update maps set in_rotation = 1")
    op.execute("update maps set in_rotation = 0 where id = 715 or id = 717 or id = 868") 

def downgrade():
    op.drop_column('maps', 'in_rotation')
