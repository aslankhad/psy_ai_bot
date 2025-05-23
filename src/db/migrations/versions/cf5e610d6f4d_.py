"""empty message

Revision ID: cf5e610d6f4d
Revises: 3e64b5b51d95
Create Date: 2025-03-26 16:49:53.348393

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cf5e610d6f4d'
down_revision: Union[str, None] = '3e64b5b51d95'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('day_hints',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('hint', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('day_hints')
    # ### end Alembic commands ###
