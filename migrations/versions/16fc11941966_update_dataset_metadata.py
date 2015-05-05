"""update dataset metadata

Revision ID: 16fc11941966
Revises: 295e0533cccf
Create Date: 2015-05-05 09:58:27.005876

"""

# revision identifiers, used by Alembic.
revision = '16fc11941966'
down_revision = '295e0533cccf'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


CHANGES = {
    'name': ('ASJP', 'The ASJP Database'),
    'contact': ('wichmann@eva.mpg.de', 'wichmannsoeren@gmail.com'),
}


def upgrade():
    for name, (_from, _to) in CHANGES.items():
        op.execute("update dataset set %s = '%s'" % (name, _to))


def downgrade():
    for name, (_from, _to) in CHANGES.items():
        op.execute("update dataset set %s = '%s'" % (name, _from))
