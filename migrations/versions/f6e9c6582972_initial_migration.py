"""Initial migration.

Revision ID: f6e9c6582972
Revises: 
Create Date: 2020-06-17 20:17:27.108433

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6e9c6582972'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'voted',
        sa.Column('ip', sa.String(length=15), nullable=False),
        sa.Column('map', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('ip', 'map')
    )
    op.drop_constraint('highscores_ibfk_1', 'highscores', type_='foreignkey')
    op.add_column('maps', sa.Column('image', sa.LargeBinary(), nullable=True))
    op.add_column('maps', sa.Column('votes', sa.Integer(), nullable=False, default=0))


def downgrade():
    op.drop_column('maps', 'votes')
    op.drop_column('maps', 'image')
    op.create_foreign_key('highscores_ibfk_1', 'highscores', 'maps', ['map_id'], ['id'])
    op.drop_table('voted')
