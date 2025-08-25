"""create_commin_info_district

Revision ID: 8e8b10978110
Revises: 78c0dd9a0a85
Create Date: 2025-08-22 10:53:10.785143

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '8e8b10978110'
down_revision: Union[str, Sequence[str], None] = '78c0dd9a0a85'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('common_info_district',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('district_id', sa.Integer(), sa.ForeignKey('district_data.id'), unique=True),
                    sa.Column('total_companies', sa.Integer()),
                    sa.Column('companies_with_business_value', sa.Integer()),
                    sa.Column('profitable_companies', sa.Integer()),
                    sa.Column('debt_free_companies', sa.Integer()),
                    sa.Column('solvent_companies', sa.Integer()),
                    sa.Column('companies_with_asset_profitability', sa.Integer()),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('common_info_district')
