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
        sa.Column('company_name', sa.String(length=50), nullable=False),
        sa.Column('inn', sa.String(length=255), nullable=True),
        sa.Column('bankruptcy_data', sa.JSON, nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('company_data')
