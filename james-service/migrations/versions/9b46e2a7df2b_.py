"""empty message

Revision ID: 9b46e2a7df2b
Revises:
Create Date: 2017-06-13 08:24:39.867605

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b46e2a7df2b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('projects',
        sa.Column('id', sa.Integer(), nullable= False),
        sa.Column('title', sa.String(length= 128), nullable= False),
        sa.Column('description', sa.String(length= 512), nullable= True),
        sa.Column('copyright', sa.String(length= 128), nullable= True),
        sa.Column('dedication', sa.String(length= 128), nullable= True),
        sa.Column('status', sa.String(), nullable= False),
        sa.Column('author', sa.String(length= 257), nullable= False),
        sa.Column('user_id', sa.Integer(), nullable= False),
        sa.Column('page_settings_id', sa.Integer(), nullable= False),
        sa.Column('created_at', sa.DateTime(), nullable= False),
        sa.Column('updated_at', sa.DateTime(), nullable= False),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table('projects_settings',
        sa.Column('id', sa.Integer(), nullable= False),
        sa.Column('orientaion', sa.String(), nullable= False),
        sa.Column('margin_top', sa.Float(), nullable= False),
        sa.Column('margin_right', sa.Float(), nullable= False),
        sa.Column('margin_bottom', sa.Float(), nullable= False),
        sa.Column('margin_left', sa.Float(), nullable= False),
        sa.PrimaryKeyConstraint('id'),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('projects_settings')
    op.drop_table('projects')
    # ### end Alembic commands ###
