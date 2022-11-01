"""empty message

Revision ID: dc55ad526bdb
Revises: 
Create Date: 2022-10-22 17:18:07.432990

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc55ad526bdb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('completed',sa.Boolean(), nullable = True))
    op.execute('UPDATE todos SET completed = False WHERE completed IS NULL;')
    op.alter_column('todos','completed', nullable =False)
    # ### end Alembic commands ###
    


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todos', 'completed')
    # ### end Alembic commands ###
