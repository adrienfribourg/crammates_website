"""Add course column to study_session

Revision ID: 01b6cceba8a0
Revises: e6c1284e5fe3
Create Date: 2024-09-13 17:10:33.336121

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01b6cceba8a0'
down_revision = 'e6c1284e5fe3'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('study_session') as batch_op:
        batch_op.add_column(sa.Column('course', sa.String(length=128), nullable=False))


def downgrade():
    with op.batch_alter_table('study_session') as batch_op:
        batch_op.drop_column('course')
