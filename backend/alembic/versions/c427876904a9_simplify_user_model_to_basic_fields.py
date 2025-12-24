"""simplify_user_model_to_basic_fields

Revision ID: c427876904a9
Revises: 1c5ce72115a7
Create Date: 2025-12-23 23:53:09.491088

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c427876904a9'
down_revision: Union[str, Sequence[str], None] = '1c5ce72115a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - remove extra user profile fields, keep only name, email, password."""
    # Drop extra columns that were added in previous migration
    op.drop_column('users', 'last_login')
    op.drop_column('users', 'last_session_date')
    op.drop_column('users', 'average_score')
    op.drop_column('users', 'total_questions_answered')
    op.drop_column('users', 'total_sessions')
    op.drop_column('users', 'interview_preferences')
    op.drop_column('users', 'preferred_interview_types')
    op.drop_column('users', 'skills')
    op.drop_column('users', 'location')
    op.drop_column('users', 'current_position')
    op.drop_column('users', 'experience_level')
    op.drop_column('users', 'target_company')
    op.drop_column('users', 'target_role')
    op.drop_column('users', 'profile_picture_url')
    op.drop_column('users', 'portfolio_url')
    op.drop_column('users', 'github_url')
    op.drop_column('users', 'linkedin_url')
    op.drop_column('users', 'bio')
    op.drop_column('users', 'phone')


def downgrade() -> None:
    """Downgrade schema - restore extra user profile fields."""
    # Re-add the columns (simplified - you may need to adjust types)
    op.add_column('users', sa.Column('phone', sa.String(length=20), nullable=True))
    op.add_column('users', sa.Column('bio', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('linkedin_url', sa.String(length=500), nullable=True))
    op.add_column('users', sa.Column('github_url', sa.String(length=500), nullable=True))
    op.add_column('users', sa.Column('portfolio_url', sa.String(length=500), nullable=True))
    op.add_column('users', sa.Column('profile_picture_url', sa.String(length=500), nullable=True))
    op.add_column('users', sa.Column('target_role', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('target_company', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('experience_level', sa.String(length=50), nullable=True))
    op.add_column('users', sa.Column('current_position', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('location', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('skills', sa.JSON(), nullable=True))
    op.add_column('users', sa.Column('preferred_interview_types', sa.JSON(), nullable=True))
    op.add_column('users', sa.Column('interview_preferences', sa.JSON(), nullable=True))
    op.add_column('users', sa.Column('total_sessions', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('users', sa.Column('total_questions_answered', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('users', sa.Column('average_score', sa.Float(), nullable=True))
    op.add_column('users', sa.Column('last_session_date', sa.DateTime(timezone=True), nullable=True))
    op.add_column('users', sa.Column('last_login', sa.DateTime(timezone=True), nullable=True))
