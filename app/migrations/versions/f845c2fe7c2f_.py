"""empty message

Revision ID: f845c2fe7c2f
Revises: d2f69bd2b548
Create Date: 2020-11-13 20:30:26.790133

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f845c2fe7c2f'
down_revision = 'd2f69bd2b548'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('community', sa.Column('com_members', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('community', 'com_members')
    # ### end Alembic commands ###
