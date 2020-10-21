"""empty message

Revision ID: 1d77e324f10b
Revises: 7138aeefb36c
Create Date: 2020-09-18 12:55:24.463840

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d77e324f10b'
down_revision = '7138aeefb36c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('site_in',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('area', sa.String(length=10), nullable=False),
    sa.Column('point', sa.String(length=10), nullable=False),
    sa.Column('pointea', sa.Integer(), nullable=True),
    sa.Column('remark', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('remark', sa.String(length=10), nullable=True))

    with op.batch_alter_table('point', schema=None) as batch_op:
        batch_op.add_column(sa.Column('memo', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('point', schema=None) as batch_op:
        batch_op.drop_column('memo')

    with op.batch_alter_table('data', schema=None) as batch_op:
        batch_op.drop_column('remark')

    op.drop_table('site_in')
    # ### end Alembic commands ###
