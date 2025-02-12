"""empty message

Revision ID: 366b729a1859
Revises: a5cffa318ac2
Create Date: 2024-09-21 14:57:07.068954

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '366b729a1859'
down_revision = 'a5cffa318ac2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('characters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('especies', sa.String(length=250), nullable=False),
    sa.Column('height', sa.String(length=250), nullable=False),
    sa.Column('gender', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('orbital_period', sa.String(length=250), nullable=False),
    sa.Column('climate', sa.String(length=40), nullable=False),
    sa.Column('population', sa.String(length=40), nullable=False),
    sa.Column('gravity', sa.String(length=40), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('population')
    )
    op.create_table('userstarwars',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=250), nullable=False),
    sa.Column('firstname', sa.String(length=250), nullable=False),
    sa.Column('lastname', sa.String(length=250), nullable=False),
    sa.Column('email', sa.String(length=250), nullable=False),
    sa.Column('password', sa.String(length=40), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('userstarwars')
    op.drop_table('planets')
    op.drop_table('characters')
    # ### end Alembic commands ###
