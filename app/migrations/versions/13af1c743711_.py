"""empty message

Revision ID: 13af1c743711
Revises: b9191d2d3789
Create Date: 2020-11-19 16:44:45.019829

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13af1c743711'
down_revision = 'b9191d2d3789'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('slug', sa.String(length=100), nullable=True),
    sa.Column('about', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('slug')
    )
    op.create_table('community_category',
    sa.Column('community_id', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['community_id'], ['community.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('community_category')
    op.drop_table('category')
    # ### end Alembic commands ###
