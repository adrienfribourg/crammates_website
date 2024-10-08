"""Add end_date column to study_session

Revision ID: ca856c738ec3
Revises: ec4c8abb7f94
Create Date: 2024-09-13 19:53:11.728594

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca856c738ec3'
down_revision = 'ec4c8abb7f94'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('study_session', schema=None) as batch_op:
        batch_op.add_column(sa.Column('end_date', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('study_session', schema=None) as batch_op:
        batch_op.drop_column('end_date')

    # ### end Alembic commands ###
