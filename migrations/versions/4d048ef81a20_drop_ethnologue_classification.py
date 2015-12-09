"""drop ethnologue classification

Revision ID: 4d048ef81a20
Revises: 16fc11941966
Create Date: 2015-12-09 10:21:39.132016

"""

# revision identifiers, used by Alembic.
revision = '4d048ef81a20'
down_revision = '16fc11941966'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute(
        "update doculect set classification_ethnologue = '', number_of_speakers = 0")


def downgrade():
    pass
