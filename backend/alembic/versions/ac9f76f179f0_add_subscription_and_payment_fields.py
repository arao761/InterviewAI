"""add_subscription_and_payment_fields

Revision ID: ac9f76f179f0
Revises: c427876904a9
Create Date: 2025-12-24 14:10:43.292129

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ac9f76f179f0'
down_revision: Union[str, Sequence[str], None] = 'c427876904a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - add subscription and payment fields."""
    # Add subscription fields to users table
    op.add_column('users', sa.Column('subscription_plan', sa.String(length=50), nullable=True))
    op.add_column('users', sa.Column('subscription_status', sa.String(length=50), nullable=True))
    op.add_column('users', sa.Column('stripe_customer_id', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('stripe_subscription_id', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('subscription_start_date', sa.DateTime(timezone=True), nullable=True))
    op.add_column('users', sa.Column('subscription_end_date', sa.DateTime(timezone=True), nullable=True))
    op.add_column('users', sa.Column('trial_end_date', sa.DateTime(timezone=True), nullable=True))
    
    # Create indexes for Stripe IDs
    op.create_index(op.f('ix_users_stripe_customer_id'), 'users', ['stripe_customer_id'], unique=True)
    op.create_index(op.f('ix_users_stripe_subscription_id'), 'users', ['stripe_subscription_id'], unique=True)
    
    # Create payments table
    op.create_table('payments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('stripe_payment_intent_id', sa.String(length=255), nullable=True),
        sa.Column('stripe_charge_id', sa.String(length=255), nullable=True),
        sa.Column('stripe_invoice_id', sa.String(length=255), nullable=True),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('currency', sa.String(length=10), nullable=False, server_default='usd'),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('payment_method', sa.String(length=50), nullable=True),
        sa.Column('subscription_plan', sa.String(length=50), nullable=True),
        sa.Column('billing_period_start', sa.DateTime(timezone=True), nullable=True),
        sa.Column('billing_period_end', sa.DateTime(timezone=True), nullable=True),
        sa.Column('payment_metadata', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_payments_id'), 'payments', ['id'], unique=False)
    op.create_index(op.f('ix_payments_user_id'), 'payments', ['user_id'], unique=False)
    op.create_index(op.f('ix_payments_stripe_payment_intent_id'), 'payments', ['stripe_payment_intent_id'], unique=True)
    op.create_index(op.f('ix_payments_stripe_charge_id'), 'payments', ['stripe_charge_id'], unique=True)
    op.create_index(op.f('ix_payments_stripe_invoice_id'), 'payments', ['stripe_invoice_id'], unique=True)


def downgrade() -> None:
    """Downgrade schema - remove subscription and payment fields."""
    # Drop payments table
    op.drop_index(op.f('ix_payments_stripe_invoice_id'), table_name='payments')
    op.drop_index(op.f('ix_payments_stripe_charge_id'), table_name='payments')
    op.drop_index(op.f('ix_payments_stripe_payment_intent_id'), table_name='payments')
    op.drop_index(op.f('ix_payments_user_id'), table_name='payments')
    op.drop_index(op.f('ix_payments_id'), table_name='payments')
    op.drop_table('payments')
    
    # Remove indexes
    op.drop_index(op.f('ix_users_stripe_subscription_id'), table_name='users')
    op.drop_index(op.f('ix_users_stripe_customer_id'), table_name='users')
    
    # Remove subscription fields from users table
    op.drop_column('users', 'trial_end_date')
    op.drop_column('users', 'subscription_end_date')
    op.drop_column('users', 'subscription_start_date')
    op.drop_column('users', 'stripe_subscription_id')
    op.drop_column('users', 'stripe_customer_id')
    op.drop_column('users', 'subscription_status')
    op.drop_column('users', 'subscription_plan')
