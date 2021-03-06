"""create all table

Revision ID: 32a9518ad88e
Revises:
Create Date: 2014-12-11 17:38:17.222570

"""

# revision identifiers, used by Alembic.
revision = '32a9518ad88e'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('list_tweet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('list_user_id', sa.Integer(), nullable=True),
    sa.Column('id_str', sa.String(length=30), nullable=True),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('create_at', sa.DateTime(), nullable=True),
    sa.Column('update_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_list_tweet_id_str'), 'list_tweet', ['id_str'], unique=False)
    op.create_index(op.f('ix_list_tweet_list_user_id'), 'list_tweet', ['list_user_id'], unique=False)
    op.create_table('list_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('screen_name', sa.String(length=120), nullable=True),
    sa.Column('profile_image_url', sa.String(length=180), nullable=True),
    sa.Column('create_at', sa.DateTime(), nullable=True),
    sa.Column('update_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('list_media',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('list_user_id', sa.Integer(), nullable=True),
    sa.Column('list_tweet_id', sa.Integer(), nullable=True),
    sa.Column('id_str', sa.String(length=30), nullable=True),
    sa.Column('media_url', sa.String(length=180), nullable=True),
    sa.Column('type', sa.String(length=20), nullable=True),
    sa.Column('status', sa.String(length=10), nullable=True),
    sa.Column('hash_id', sa.String(length=64), nullable=True),
    sa.Column('create_at', sa.DateTime(), nullable=True),
    sa.Column('update_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_list_media_list_tweet_id'), 'list_media', ['list_tweet_id'], unique=False)
    op.create_index(op.f('ix_list_media_list_user_id'), 'list_media', ['list_user_id'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_list_media_list_user_id'), table_name='list_media')
    op.drop_index(op.f('ix_list_media_list_tweet_id'), table_name='list_media')
    op.drop_table('list_media')
    op.drop_table('list_user')
    op.drop_index(op.f('ix_list_tweet_list_user_id'), table_name='list_tweet')
    op.drop_index(op.f('ix_list_tweet_id_str'), table_name='list_tweet')
    op.drop_table('list_tweet')
    ### end Alembic commands ###
