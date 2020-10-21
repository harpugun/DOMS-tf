"""empty message

Revision ID: 7138aeefb36c
Revises: b771fc82aeb1
Create Date: 2020-09-17 15:55:41.934127

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7138aeefb36c'
down_revision = 'b771fc82aeb1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('data15', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('data', schema=None) as batch_op:
        batch_op.drop_column('data15')

    # ### end Alembic commands ###