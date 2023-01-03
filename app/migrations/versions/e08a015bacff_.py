"""empty message

Revision ID: e08a015bacff
Revises: 7aeb53aa4a76
Create Date: 2020-11-24 18:16:48.830520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e08a015bacff'
down_revision = '7aeb53aa4a76'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_community',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('community_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['community_id'], ['community.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.add_column('community', sa.Column('creator_id', sa.Integer(), nullable=True))
    op.add_column('report', sa.Column('rType', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('report', 'rType')
    op.drop_column('community', 'creator_id')
    op.drop_table('user_community')
    # ### end Alembic commands ###
