"""Multiple times for same map,username,skin

Revision ID: f84aadf4e2d8
Revises: f6e9c6582972
Create Date: 2020-06-20 17:38:10.074480

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f84aadf4e2d8'
down_revision = 'f6e9c6582972'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("alter table highscores drop constraint primary key")
    op.execute("alter table highscores add column score_id int NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST")
    op.alter_column('highscores', 'map_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('highscores', 'skin',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=20),
               nullable=True)
    op.alter_column('highscores', 'username',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=30),
               nullable=True)
    op.alter_column('maps', 'votes',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)


def downgrade():
    op.alter_column('maps', 'votes',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('highscores', 'username',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=30),
               nullable=False)
    op.alter_column('highscores', 'skin',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=20),
               nullable=False)
    op.alter_column('highscores', 'map_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.drop_column('highscores', 'score_id')
