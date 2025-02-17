"""Add to finalBet

Revision ID: 5fbe42e25933
Revises: 298665c2eb10
Create Date: 2024-11-12 14:43:22.382268

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5fbe42e25933'
down_revision = '298665c2eb10'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('final_bet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('arrays', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('low_stdev', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('final_bet', schema=None) as batch_op:
        batch_op.drop_column('low_stdev')
        batch_op.drop_column('arrays')

    # ### end Alembic commands ###
