"""Add university and courses to user model

Revision ID: e6c1284e5fe3
Revises: bb860d5038d3
Create Date: 2024-09-01 16:43:42.225744

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector


# revision identifiers, used by Alembic.
revision = 'e6c1284e5fe3'
down_revision = 'bb860d5038d3'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)

    # Check if 'university' column exists before adding it
    if 'university' not in [col['name'] for col in inspector.get_columns('user')]:
        with op.batch_alter_table('user', schema=None) as batch_op:
            batch_op.add_column(sa.Column('university', sa.String(length=150), nullable=True))

    # Check if 'courses' column exists before adding it
    if 'courses' not in [col['name'] for col in inspector.get_columns('user')]:
        with op.batch_alter_table('user', schema=None) as batch_op:
            batch_op.add_column(sa.Column('courses', sa.String(length=300), nullable=True))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
               existing_type=sa.VARCHAR(length=150),
               type_=sa.String(length=256),
               existing_nullable=False)
        batch_op.drop_column('course')


def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('course', sa.VARCHAR(length=100), nullable=False))
        batch_op.alter_column('password_hash',
               existing_type=sa.String(length=256),
               type_=sa.VARCHAR(length=150),
               existing_nullable=False)
        batch_op.drop_column('courses')
        batch_op.drop_column('university')
