"""empty message

Revision ID: 69b735aaab56
Revises: 5c00652743c3
Create Date: 2021-05-06 04:13:55.750667

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '69b735aaab56'
down_revision = '5c00652743c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venues', sa.Column('genres', sa.ARRAY(sa.String()), nullable=True))
    op.drop_column('venues', 'generes')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venues', sa.Column('generes', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=True))
    op.drop_column('venues', 'genres')
    # ### end Alembic commands ###
