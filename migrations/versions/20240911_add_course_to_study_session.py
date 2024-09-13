from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = 'd7f8e2c9a3b4'
down_revision = 'e6c1284e5fe3'
branch_labels = None
depends_on = None

def upgrade():
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)

    # Check if 'course' column exists before adding it
    if 'course' not in [col['name'] for col in inspector.get_columns('study_session')]:
        with op.batch_alter_table('study_session', schema=None) as batch_op:
            batch_op.add_column(sa.Column('course', sa.String(length=128), nullable=False))

def downgrade():
    with op.batch_alter_table('study_session', schema=None) as batch_op:
        batch_op.drop_column('course')
