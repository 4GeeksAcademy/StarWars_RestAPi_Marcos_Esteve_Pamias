"""empty message

Revision ID: f6be72f1e1d1
Revises: 366b729a1859
Create Date: 2024-09-21 15:32:00.961578

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6be72f1e1d1'
down_revision = '366b729a1859'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('userstarwars')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=120), nullable=False))
        batch_op.create_unique_constraint(None, ['name'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('name')

    op.create_table('userstarwars',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.Column('firstname', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.Column('lastname', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=40), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='userstarwars_pkey'),
    sa.UniqueConstraint('email', name='userstarwars_email_key')
    )
    # ### end Alembic commands ###
