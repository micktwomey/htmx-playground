"""Adding an update_date column

Revision ID: 4aa780bf0c24
Revises: f7939df47871
Create Date: 2022-10-19 16:23:19.392453

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4aa780bf0c24"
down_revision = "f7939df47871"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "widgets",
        sa.Column(
            "update_date",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=True,
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("widgets", "update_date")
    # ### end Alembic commands ###