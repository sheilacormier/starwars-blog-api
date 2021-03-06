"""empty message

Revision ID: 4d60ade4f0f4
Revises: f42bc33a02bb
Create Date: 2021-04-24 16:17:33.075638

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d60ade4f0f4'
down_revision = 'f42bc33a02bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('planets', sa.Column('photo_url', sa.String(length=200), nullable=True))
    op.add_column('starships', sa.Column('photo_url', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('starships', 'photo_url')
    op.drop_column('planets', 'photo_url')
    # ### end Alembic commands ###
