from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'new_revision_id'  # Replace with a unique revision ID, like 'b6546207be3a'
down_revision = 'previous_revision_id'  # Replace with the ID of the last migration, like 'e6c1284e5fe3'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('study_session', schema=None) as batch_op:
        batch_op.add_column(sa.Column('course', sa.String(length=128), nullable=False))

def downgrade():
    with op.batch_alter_table('study_session', schema=None) as batch_op:
        batch_op.drop_column('course')
