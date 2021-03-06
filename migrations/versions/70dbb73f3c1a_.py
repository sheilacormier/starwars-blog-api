"""empty message

Revision ID: 70dbb73f3c1a
Revises: b77bbf8609d7
Create Date: 2021-04-21 15:46:10.681409

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '70dbb73f3c1a'
down_revision = 'b77bbf8609d7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('people', sa.Column('homeworld', sa.Integer(), nullable=True))
    op.drop_constraint('people_ibfk_1', 'people', type_='foreignkey')
    op.create_foreign_key(None, 'people', 'planets', ['homeworld'], ['id'])
    op.drop_column('people', 'homeworld_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('people', sa.Column('homeworld_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'people', type_='foreignkey')
    op.create_foreign_key('people_ibfk_1', 'people', 'planets', ['homeworld_id'], ['id'])
    op.drop_column('people', 'homeworld')
    # ### end Alembic commands ###
