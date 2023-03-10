"""empty message

Revision ID: 4fdb3ea8fdfe
Revises: ee97c856d43a
Create Date: 2020-11-20 16:38:00.153585

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4fdb3ea8fdfe'
down_revision = 'ee97c856d43a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('creator_id', sa.Integer(), nullable=True))
    op.add_column('report', sa.Column('creator_id', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('blocked', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'blocked')
    op.drop_column('report', 'creator_id')
    op.drop_column('comment', 'creator_id')
    # ### end Alembic commands ###
