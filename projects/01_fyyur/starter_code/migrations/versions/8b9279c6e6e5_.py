"""empty message

Revision ID: 8b9279c6e6e5
Revises: f511c0e56d69
Create Date: 2021-05-07 17:31:18.627838

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b9279c6e6e5'
down_revision = 'f511c0e56d69'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venues', sa.Column('website_link', sa.String(), nullable=True))
    op.drop_column('venues', 'website')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venues', sa.Column('website', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('venues', 'website_link')
    # ### end Alembic commands ###
