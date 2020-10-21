"""empty message

Revision ID: 813c2f0cbc27
Revises: cf098aa85365
Create Date: 2020-09-01 14:07:33.640958

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '813c2f0cbc27'
down_revision = 'cf098aa85365'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('site', schema=None) as batch_op:
        batch_op.add_column(sa.Column('enddate', sa.Date(), nullable=True))
        batch_op.add_column(sa.Column('startdate', sa.Date(), nullable=True))
        batch_op.drop_column('end_date')
        batch_op.drop_column('start_date')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('site', schema=None) as batch_op:
        batch_op.add_column(sa.Column('start_date', sa.DATE(), nullable=True))
        batch_op.add_column(sa.Column('end_date', sa.DATE(), nullable=True))
        batch_op.drop_column('startdate')
        batch_op.drop_column('enddate')

    # ### end Alembic commands ###
