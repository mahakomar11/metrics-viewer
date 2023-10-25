"""init

Revision ID: 3761df14a877
Revises: 
Create Date: 2023-10-22 11:27:49.438277

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3761df14a877"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "impression",
        sa.Column("uuid", sa.UUID(), nullable=False),
        sa.Column("impressions_count", sa.Integer(), nullable=False),
        sa.Column("reg_time", sa.DateTime(), nullable=False),
        sa.Column("mm_dma", sa.Integer(), nullable=False),
        sa.Column("site_id", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("uuid"),
    )
    op.create_table(
        "event",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("impression_uuid", sa.UUID(), nullable=False),
        sa.Column("tag", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.execute(
        """
        COPY impression (reg_time, uuid, mm_dma, site_id, impressions_count) 
        FROM '/raw_data/impressions.csv' WITH DELIMITER ',' CSV HEADER;
        """
    )
    op.execute(
        """
        COPY event (id, impression_uuid, tag)
        FROM '/raw_data/events.csv' WITH DELIMITER ',' CSV HEADER;
        """
    )


def downgrade() -> None:
    op.drop_table("event")
    op.drop_table("impression")
