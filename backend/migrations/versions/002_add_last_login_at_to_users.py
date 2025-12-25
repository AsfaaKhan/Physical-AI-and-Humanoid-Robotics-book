"""Add last_login_at column to users table

Revision ID: 002
Revises: 001
Create Date: 2025-12-22 22:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add last_login_at column to users table
    op.add_column('users', sa.Column('last_login_at', sa.DateTime(timezone=True), server_default=sa.text('now()')))


def downgrade() -> None:
    # Remove last_login_at column from users table
    op.drop_column('users', 'last_login_at')