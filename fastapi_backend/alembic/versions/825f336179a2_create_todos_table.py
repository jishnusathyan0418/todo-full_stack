"""create todos table

Revision ID: 825f336179a2
Revises: 
Create Date: 2025-10-04 16:42:23.549699

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '825f336179a2'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute(
        """
        create table todos(
            id bigserial primary key,
            name text,
            completed boolean not null default false
        )
        """
    )



def downgrade():
    op.execute(
        "drop the table todos;"
    )
