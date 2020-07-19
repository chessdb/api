"""added_positions


Revision ID: 96115ea05082
Revises:
Create Date: 2020-07-19 18:36:43.829236

"""
import sys
import pathlib

# Make migrations importable by adding the project root folder to the path.
# 'migrations/versions/96115ea05082.py' == __file__
# 'migrations/versions/' == parents[0]
# 'migrations/' == parents[1]
# '.' == parents[2]
DIR_NAME = str(pathlib.Path(__file__).parents[2])
sys.path.append(DIR_NAME)

from alembic import op
from sqlalchemy import orm
from migrations import helper

# revision identifiers, used by Alembic.
revision = '96115ea05082'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    helper.execute(bind=op.get_bind(), filename="added_positions/upgrade.sql")


def downgrade():
    helper.execute(bind=op.get_bind(), filename="added_positions/downgrade.sql")
