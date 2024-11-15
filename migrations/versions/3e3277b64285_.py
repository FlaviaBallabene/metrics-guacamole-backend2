"""empty message

Revision ID: 3e3277b64285
Revises: abd13bae28e7
Create Date: 2024-11-11 23:44:07.738431

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e3277b64285'
down_revision = 'abd13bae28e7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('weekly_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('start_date', sa.Date(), nullable=False))
        batch_op.add_column(sa.Column('end_date', sa.Date(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('weekly_data', schema=None) as batch_op:
        batch_op.drop_column('end_date')
        batch_op.drop_column('start_date')

    # ### end Alembic commands ###
