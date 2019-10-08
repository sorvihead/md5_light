"""empty message

Revision ID: 8841e2c7e358
Revises: 
Create Date: 2019-10-08 17:01:23.631609

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8841e2c7e358'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('url', sa.String(length=128), nullable=True),
    sa.Column('email', sa.String(length=128), nullable=True),
    sa.Column('md5', sa.String(length=128), nullable=True),
    sa.Column('complete', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_url'), 'task', ['url'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_task_url'), table_name='task')
    op.drop_table('task')
    # ### end Alembic commands ###
