"""remove customer from orders

Revision ID: 3d6ba42b4bce
Revises: 79be50c6a50e
Create Date: 2025-06-04 15:51:25.200206

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d6ba42b4bce'
down_revision: Union[str, None] = '79be50c6a50e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('user_id', sa.Integer(), nullable=False))
    op.drop_constraint('orders_customer_id_fkey', 'orders', type_='foreignkey')
    op.create_foreign_key(None, 'orders', 'users', ['user_id'], ['id'])
    op.drop_column('orders', 'customer_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('customer_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.create_foreign_key('orders_customer_id_fkey', 'orders', 'customers', ['customer_id'], ['id'])
    op.drop_column('orders', 'user_id')
    # ### end Alembic commands ###
