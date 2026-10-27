"""add index for latest service order lookup

Revision ID: a9c2e8f7d4b1
Revises: 26378592b45b
Create Date: 2026-10-26

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "a9c2e8f7d4b1"
down_revision: Union[str, Sequence[str], None] = "26378592b45b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        "ix_service_orders_employee_created_at_id",
        "service_orders",
        ["employee_id", "created_at", "id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_service_orders_employee_created_at_id",
        table_name="service_orders",
    )
