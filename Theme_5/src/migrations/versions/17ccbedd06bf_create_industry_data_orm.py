"""create_industry_data_orm

Revision ID: 17ccbedd06bf
Revises: 8329dcce8cd2
Create Date: 2025-08-22 10:52:40.823001

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '17ccbedd06bf'
down_revision: Union[str, Sequence[str], None] = '8329dcce8cd2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('industry_data',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('industry', sa.String(), nullable=False, unique=True),
                    sa.Column('avg_business_value', sa.Float(), nullable=True),
                    sa.Column('avg_liquidation_value', sa.Float(), nullable=True),
                    sa.Column('avg_creditors_return', sa.Float(), nullable=True),
                    sa.Column('avg_working_capital_needs', sa.Float(), nullable=True),
                    sa.Column('avg_profit_before_tax', sa.Float(), nullable=True)
                    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("industry_data")
