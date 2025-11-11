"""add payment table

Revision ID: 001
Revises:
Create Date: 2025-11-11 12:46:00.000000

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
    """Create the payments table."""
    op.create_table(
        'payments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('stripe_customer_id', sa.String(length=255), nullable=True),
        sa.Column('stripe_checkout_session_id', sa.String(length=255), nullable=True),
        sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('currency', sa.String(length=3), nullable=False, server_default='usd'),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='pending'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_payments_id'), 'payments', ['id'], unique=False)
    op.create_index(op.f('ix_payments_stripe_customer_id'), 'payments', ['stripe_customer_id'], unique=False)
    op.create_index(op.f('ix_payments_stripe_checkout_session_id'), 'payments', ['stripe_checkout_session_id'], unique=True)


def downgrade() -> None:
    """Drop the payments table."""
    op.drop_index(op.f('ix_payments_stripe_checkout_session_id'), table_name='payments')
    op.drop_index(op.f('ix_payments_stripe_customer_id'), table_name='payments')
    op.drop_index(op.f('ix_payments_id'), table_name='payments')
    op.drop_table('payments')
