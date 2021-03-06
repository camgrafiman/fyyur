"""empty message

Revision ID: f511c0e56d69
Revises: 69b735aaab56
Create Date: 2021-05-06 04:34:39.077781

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f511c0e56d69'
down_revision = '69b735aaab56'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venues', 'genres',
                    existing_type=postgresql.ARRAY(sa.VARCHAR()),
                    nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venues', 'genres',
                    existing_type=postgresql.ARRAY(sa.VARCHAR()),
                    nullable=True)
    # ### end Alembic commands ###
