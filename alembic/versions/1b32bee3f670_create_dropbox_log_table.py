"""create_dropbox_log_table

Revision ID: 1b32bee3f670
Revises: 5511a2d0efea
Create Date: 2015-07-03 16:21:25.118523

"""

# revision identifiers, used by Alembic.
revision = '1b32bee3f670'
down_revision = '5511a2d0efea'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dropbox_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('list_user_id', sa.Integer(), nullable=True),
    sa.Column('list_media_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.Enum('success', 'failed', name='status_type'), nullable=False),
    sa.Column('create_at', sa.DateTime(), nullable=True),
    sa.Column('update_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dropbox_log_list_media_id'), 'dropbox_log', ['list_media_id'], unique=False)
    op.create_index(op.f('ix_dropbox_log_list_user_id'), 'dropbox_log', ['list_user_id'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_dropbox_log_list_user_id'), table_name='dropbox_log')
    op.drop_index(op.f('ix_dropbox_log_list_media_id'), table_name='dropbox_log')
    op.drop_table('dropbox_log')
    ENUM(name="status_type").drop(op.get_bind(), checkfirst=False)
    ### end Alembic commands ###
