"""add confirmed columns to User table

Revision ID: 58e7c3c4598e
Revises: 
Create Date: 2016-03-10 23:57:53.373977

"""

# revision identifiers, used by Alembic.
revision = '58e7c3c4598e'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column("user", sa.Column("confirmed", sa.Boolean, default=False, nullable=False))
    op.add_column("user", sa.Column("confirmed_on", sa.DateTime(timezone=True)))


def downgrade():
    op.drop_column("user", 'confirmed')
    op.drop_column("user", 'confirmed_on')
