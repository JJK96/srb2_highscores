"""Add images

Revision ID: d1a0a1316d53
Revises: f84aadf4e2d8
Create Date: 2020-06-20 19:09:55.209500

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1a0a1316d53'
down_revision = 'f84aadf4e2d8'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("update maps set image = 'Amber_Island_1.jpg' where id = 716")
    op.execute("update maps set image = 'Asteroid_City_1.jpg' where id = 719")
    op.execute("update maps set image = 'Bizarre_Barrel_1.jpg' where id = 714")
    op.execute("update maps set image = 'Black_Core_1.jpg' where id = 147")
    op.execute("update maps set image = 'Burning_Sands_1.jpg' where id = 858")
    op.execute("update maps set image = 'Corrupt_Shrine_1.jpg' where id = 866")
    op.execute("update maps set image = 'Crimson_Cave_1.jpg' where id = 426")
    op.execute("update maps set image = 'Crimson_Construct_1.jpg' where id = 712")
    op.execute("update maps set image = 'Cyan_Cave_1.jpg' where id = 429")
    op.execute("update maps set image = 'Dread_Valley_1.jpg' where id = 428")
    op.execute("update maps set image = 'Egg_Hall_1.jpg' where id = 425")
    op.execute("update maps set image = 'Emerald_Coast_1.jpg' where id = 860")
    op.execute("update maps set image = 'Endless_Woods_1.jpg' where id = 424")
    op.execute("update maps set image = 'Fertile_Canyon_1.jpg' where id = 857")
    op.execute("update maps set image = 'Frozen_Night_1.jpg' where id = 862")
    op.execute("update maps set image = 'Frozen_Night_alt_1.jpg' where id = 423")
    op.execute("update maps set image = 'Frozen_Slush_1.jpg' where id = 713")
    op.execute("update maps set image = 'Generic_Greens_1.jpg' where id = 930")
    op.execute("update maps set image = 'Gravity_Hill_1.jpg' where id = 720")
    op.execute("update maps set image = 'Heaven_Pass_1.jpg' where id = 864")
    op.execute("update maps set image = 'Ice_Cap_1.jpg' where id = 929")
    op.execute("update maps set image = 'Lemon_Circuit_1.jpg' where id = 892")
    op.execute("update maps set image = 'Lime_Isle_1.jpg' where id = 927")
    op.execute("update maps set image = 'Lost_Speedway_1.jpg' where id = 721")
    op.execute("update maps set image = 'Mecha_Hill_1.jpg' where id = 711")
    op.execute("update maps set image = 'Metallic_Hall_1.jpg' where id = 863")
    op.execute("update maps set image = 'Morning_Hill_1.jpg' where id = 928")
    op.execute("update maps set image = 'Mystic_Marsh_1.jpg' where id = 174")
    op.execute("update maps set image = 'Neo_Sonic_Circuit_1.jpg' where id = 759")
    op.execute("update maps set image = 'Nightmare_Circuit_1.jpg' where id = 894")
    op.execute("update maps set image = 'Quicksand_Ruins_1.jpg' where id = 855")
    op.execute("update maps set image = 'Race_Alley_1.jpg' where id = 859")
    op.execute("update maps set image = 'Rainbow_Dash_1.jpg' where id = 430")
    op.execute("update maps set image = 'Sandopolis_1.jpg' where id = 931")
    op.execute("update maps set image = 'Sluggish_Shrine_1.jpg' where id = 893")
    op.execute("update maps set image = 'Sonic_Circuit_1.jpg' where id = 867")
    op.execute("update maps set image = 'Speedy_Ruins_1.jpg' where id = 891")
    op.execute("update maps set image = 'Storm_Castle_1.jpg' where id = 718")
    op.execute("update maps set image = 'Tainted_Gorge_1.jpg' where id = 856")
    op.execute("update maps set image = 'Thunder_Factory_1.jpg' where id = 427")
    op.execute("update maps set image = 'Toxic_Citadel_1.jpg' where id = 861")
    op.execute("update maps set image = 'Warped_Woods_1.jpg' where id = 865")


def downgrade():
    pass
