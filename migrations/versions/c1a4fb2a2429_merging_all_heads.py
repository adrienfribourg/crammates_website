"""Merging all heads

Revision ID: c1a4fb2a2429
Revises: d7f8e2c9a3b4, b6546207be3a, 4b71cbf1fb31
Create Date: 2024-09-11 23:51:13.968065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1a4fb2a2429'
down_revision = ('d7f8e2c9a3b4', 'b6546207be3a', '4b71cbf1fb31')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
