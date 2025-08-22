"""company_data_orm

Revision ID: a1a4392d7cc0
Revises: 
Create Date: 2025-08-20 08:09:46.726125

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'a1a4392d7cc0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'company_data',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('okved', sa.String(length=10), nullable=False),
        sa.Column('okved_decoding', sa.String(length=255), nullable=False),
        sa.Column('industry', sa.String(length=512), nullable=False),
        sa.Column('region', sa.String(length=255), nullable=False),
        sa.Column('district', sa.String(length=255), nullable=False),
        sa.Column('business_value', sa.Float(), nullable=True),
        sa.Column('liquidation_value', sa.Float(), nullable=True),
        sa.Column('creditors_return', sa.Float(), nullable=True),
        sa.Column('working_capital_needs', sa.Float(), nullable=True),
        sa.Column('profit_before_tax', sa.Float(), nullable=True),
        sa.Column('tax_debt', sa.Float(), nullable=True),
        sa.Column('enforcement_proceedings', sa.Float(), nullable=True),
        sa.Column('guarantee_limit', sa.String(length=255), nullable=True),
        sa.Column('solvency_rank', sa.Float(), nullable=True),
        sa.Column('company_age', sa.Float(), nullable=True),
        sa.Column('bankruptcy_data', sa.JSON(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('company_data')
