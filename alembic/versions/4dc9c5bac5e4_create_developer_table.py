"""create developer table

Revision ID: 4dc9c5bac5e4
Revises: 1b04db1c24fd
Create Date: 2014-12-13 15:06:21.214938

"""

# revision identifiers, used by Alembic.
revision = '4dc9c5bac5e4'
down_revision = '1b04db1c24fd'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('developer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=True),
    sa.Column('api_key', sa.String(length=120), nullable=True),
    sa.Column('create_at', sa.DateTime(), nullable=True),
    sa.Column('update_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_developer_account_id'), 'developer', ['account_id'], unique=False)
    op.create_index(op.f('ix_developer_api_key'), 'developer', ['api_key'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_developer_api_key'), table_name='developer')
    op.drop_index(op.f('ix_developer_account_id'), table_name='developer')
    op.drop_table('developer')
    ### end Alembic commands ###