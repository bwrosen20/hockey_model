"""Change total corsi to even

Revision ID: e3317a63dbec
Revises: 50182e3180b4
Create Date: 2024-10-20 11:38:05.211531

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3317a63dbec'
down_revision = '50182e3180b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.add_column(sa.Column('home_even_corsi', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('away_even_corsi', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('home_even_hits', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('away_even_hits', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('home_even_blocks', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('away_even_blocks', sa.Integer(), nullable=True))
        batch_op.drop_column('away_total_corsi')
        batch_op.drop_column('home_total_hits')
        batch_op.drop_column('home_total_blocks')
        batch_op.drop_column('away_total_hits')
        batch_op.drop_column('home_total_corsi')
        batch_op.drop_column('away_total_blocks')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.add_column(sa.Column('away_total_blocks', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('home_total_corsi', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('away_total_hits', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('home_total_blocks', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('home_total_hits', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('away_total_corsi', sa.INTEGER(), nullable=True))
        batch_op.drop_column('away_even_blocks')
        batch_op.drop_column('home_even_blocks')
        batch_op.drop_column('away_even_hits')
        batch_op.drop_column('home_even_hits')
        batch_op.drop_column('away_even_corsi')
        batch_op.drop_column('home_even_corsi')

    # ### end Alembic commands ###
