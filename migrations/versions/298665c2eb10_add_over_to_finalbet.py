"""Add over to finalbet

Revision ID: 298665c2eb10
Revises: cfeade2a86a6
Create Date: 2024-11-07 12:54:31.545295

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '298665c2eb10'
down_revision = 'cfeade2a86a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('final_bet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('over', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('final_bet', schema=None) as batch_op:
        batch_op.drop_column('over')

    # ### end Alembic commands ###
