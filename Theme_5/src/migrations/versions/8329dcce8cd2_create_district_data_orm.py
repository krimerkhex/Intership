"""create_district_data_orm

Revision ID: 8329dcce8cd2
Revises: 24c6bb2103ba
Create Date: 2025-08-22 07:32:23.085476

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '8329dcce8cd2'
down_revision: Union[str, Sequence[str], None] = '24c6bb2103ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('district_data',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('county', sa.String(), nullable=False, unique=True),
                    sa.Column('avg_business_value', sa.Float(), nullable=True),
                    sa.Column('avg_liquidation_value', sa.Float(), nullable=True),
                    sa.Column('avg_creditors_return', sa.Float(), nullable=True),
                    sa.Column('avg_working_capital_needs', sa.Float(), nullable=True),
                    sa.Column('avg_profit_before_tax', sa.Float(), nullable=True)
                    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("district_data")
