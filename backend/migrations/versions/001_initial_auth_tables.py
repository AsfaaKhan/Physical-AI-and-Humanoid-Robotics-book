"""Initial auth tables

Revision ID: 001
Revises:
Create Date: 2025-12-16 22:45:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('user_id', sa.String(255), primary_key=True, index=True),
        sa.Column('email', sa.String(255), unique=True, index=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), onupdate=sa.text('now()'), nullable=False),
        sa.Column('is_verified', sa.Boolean, default=False)
    )

    # Create user_profiles table
    op.create_table('user_profiles',
        sa.Column('user_id', sa.String(255), primary_key=True, index=True),
        sa.Column('software_experience', sa.String(20), nullable=False),
        sa.Column('programming_background', sa.String(20), nullable=False),
        sa.Column('hardware_knowledge', sa.String(20), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), onupdate=sa.text('now()'), nullable=False),
        sa.Column('profile_completed', sa.Boolean, default=False),
        sa.CheckConstraint("software_experience IN ('beginner', 'intermediate', 'expert')", name='check_software_experience'),
        sa.CheckConstraint("programming_background IN ('none', 'basic', 'intermediate', 'advanced')", name='check_programming_background'),
        sa.CheckConstraint("hardware_knowledge IN ('none', 'basic', 'intermediate', 'advanced')", name='check_hardware_knowledge')
    )

    # Create user_sessions table
    op.create_table('user_sessions',
        sa.Column('session_id', sa.String(255), primary_key=True, index=True),
        sa.Column('user_id', sa.String(255), index=True, nullable=False),
        sa.Column('token_hash', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('last_accessed', sa.DateTime(timezone=True), server_default=sa.text('now()'), onupdate=sa.text('now()'), nullable=False),
        sa.Column('user_agent', sa.Text),
        sa.Column('ip_address', sa.String(45))
    )

    # Add foreign key constraint for user_profiles
    op.create_foreign_key('fk_user_profiles_user_id', 'user_profiles', 'users', ['user_id'], ['user_id'])

    # Create indexes for better performance
    op.create_index('idx_user_sessions_user_id', 'user_sessions', ['user_id'])
    op.create_index('idx_user_sessions_expires_at', 'user_sessions', ['expires_at'])


def downgrade() -> None:
    # Drop foreign key constraint first
    op.drop_constraint('fk_user_profiles_user_id', 'user_profiles', type_='foreignkey')

    # Drop indexes
    op.drop_index('idx_user_sessions_user_id', table_name='user_sessions')
    op.drop_index('idx_user_sessions_expires_at', table_name='user_sessions')

    # Drop tables in reverse order
    op.drop_table('user_sessions')
    op.drop_table('user_profiles')
    op.drop_table('users')