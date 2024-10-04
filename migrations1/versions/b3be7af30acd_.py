"""empty message

Revision ID: b3be7af30acd
Revises: 51b59bace9fd
Create Date: 2024-09-22 17:26:24.999217

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3be7af30acd'
down_revision = '51b59bace9fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('lastname', sa.String(length=120), nullable=False))
        batch_op.alter_column('user_name',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('user_name',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
        batch_op.drop_column('lastname')

    # ### end Alembic commands ###
