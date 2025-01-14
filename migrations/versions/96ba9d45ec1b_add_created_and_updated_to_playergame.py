"""Add created and updated to PlayerGame

Revision ID: 96ba9d45ec1b
Revises: e3317a63dbec
Create Date: 2024-10-22 22:05:20.069935

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96ba9d45ec1b'
down_revision = 'e3317a63dbec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('player_game', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('player_game', schema=None) as batch_op:
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')

    # ### end Alembic commands ###
