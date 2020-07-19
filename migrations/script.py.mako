"""${message}


Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
import sys
import pathlib

# Make migrations importable by adding the project root folder to the path.
# 'migrations/versions/${up_revision}.py' == __file__
# 'migrations/versions/' == parents[0]
# 'migrations/' == parents[1]
# '.' == parents[2]
DIR_NAME = str(pathlib.Path(__file__).parents[2])
sys.path.append(DIR_NAME)

from alembic import op
from sqlalchemy import orm
from migrations import helper
${imports if imports else ""}
# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
    helper.execute(bind=op.get_bind(), filename="${message}/upgrade.sql")

def downgrade():
    helper.execute(bind=op.get_bind(), filename="${message}/downgrade.sql")
