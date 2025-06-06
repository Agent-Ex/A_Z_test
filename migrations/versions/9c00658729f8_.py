"""empty message

Revision ID: 9c00658729f8
Revises: 
Create Date: 2024-12-12 15:25:23.866446

"""

# STDLIB
from typing import Sequence, Union

# THIRDPARTY
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '9c00658729f8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'territory',
        sa.Column('cadastral_number', sa.String(), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longtitude', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('cadastral_number'),
    )
    op.create_table(
        'result',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('cadastral_number', sa.String(), nullable=False),
        sa.Column('score', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(
            ['cadastral_number'],
            ['territory.cadastral_number'],
            ondelete='CASCADE',
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('result')
    op.drop_table('territory')
    # ### end Alembic commands ###
