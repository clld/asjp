"""fix polymorphic_type

Revision ID: 295e0533cccf
Revises: 
Create Date: 2014-11-26 13:47:54.018000

"""

# revision identifiers, used by Alembic.
revision = '295e0533cccf'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    update_pmtype(['parameter', 'value', 'valueset', 'language'], 'base', 'custom')


def downgrade():
    update_pmtype(['parameter', 'value', 'valueset', 'language'], 'custom', 'base')


def update_pmtype(tablenames, before, after):
    for table in tablenames:
        op.execute(sa.text('UPDATE %s SET polymorphic_type = :after '
            'WHERE polymorphic_type = :before' % table
            ).bindparams(before=before, after=after))
