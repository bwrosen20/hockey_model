"""Add result and daily index to finalbet

Revision ID: 3cc0158ab16a
Revises: 5851cc150188
Create Date: 2024-10-30 18:02:25.570141

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3cc0158ab16a'
down_revision = '5851cc150188'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('final_bet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('daily_index', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('result', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('final_bet', schema=None) as batch_op:
        batch_op.drop_column('result')
        batch_op.drop_column('daily_index')

    # ### end Alembic commands ###
