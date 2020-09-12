"""Add images for new maps

Revision ID: 8ee85df7e412
Revises: e6baa6897cd7
Create Date: 2020-09-12 11:34:43.888863

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8ee85df7e412'
down_revision = 'e6baa6897cd7'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("update maps set image = 'Greenflower_Canyon_1.jpg' where id = 605")
    op.execute("update maps set image = 'Greenflower_circuit_1.jpg' where id = 315")
    op.execute("update maps set image = 'Haptic_Caverns_1.jpg' where id = 604")
    op.execute("update maps set image = 'Hydrowing_1.jpg' where id = 603")

def downgrade():
    pass
