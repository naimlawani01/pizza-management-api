"""Initial migration

Revision ID: 556303a7ecbe
Revises: 2adae4a3a4a6
Create Date: 2025-06-03 18:30:10.264098

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '556303a7ecbe'
down_revision: Union[str, None] = '2adae4a3a4a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pizzas', 'ingredients')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pizzas', sa.Column('ingredients', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
