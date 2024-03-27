"""applications

Revision ID: d1ae94e71ff4
Revises: 099295fe7868
Create Date: 2024-03-25 23:51:53.663256

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1ae94e71ff4'
down_revision: Union[str, None] = '099295fe7868'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('applications', sa.Column('description', sa.String(length=10000), nullable=True))
    op.add_column('applications', sa.Column('application_link', sa.String(length=1000), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('applications', 'application_link')
    op.drop_column('applications', 'description')
    # ### end Alembic commands ###
