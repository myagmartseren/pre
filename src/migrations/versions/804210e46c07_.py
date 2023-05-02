"""empty message

Revision ID: 804210e46c07
Revises: 56db3cc1c79b
Create Date: 2023-05-02 17:31:55.168374

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '804210e46c07'
down_revision = '56db3cc1c79b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('file_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('action', sa.String(length=256), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['file_id'], ['files.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('files', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type', sa.String(length=50), nullable=False))
        batch_op.add_column(sa.Column('path', sa.String(length=256), nullable=False))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
        batch_op.add_column(sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))

    with op.batch_alter_table('shares', schema=None) as batch_op:
        batch_op.add_column(sa.Column('delegator_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('delegatee_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('re_key', sa.String(length=256), nullable=False))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
        batch_op.add_column(sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
        batch_op.create_foreign_key(None, 'users', ['delegator_id'], ['id'])
        batch_op.create_foreign_key(None, 'users', ['delegatee_id'], ['id'])
        batch_op.drop_column('recipient_id')
        batch_op.drop_column('prf_key')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
        batch_op.add_column(sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
        batch_op.drop_constraint('users_private_key_key', type_='unique')
        batch_op.drop_constraint('users_public_key_key', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_unique_constraint('users_public_key_key', ['public_key'])
        batch_op.create_unique_constraint('users_private_key_key', ['private_key'])
        batch_op.drop_column('deleted_at')
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')

    with op.batch_alter_table('shares', schema=None) as batch_op:
        batch_op.add_column(sa.Column('prf_key', sa.VARCHAR(length=256), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('recipient_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('deleted_at')
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')
        batch_op.drop_column('re_key')
        batch_op.drop_column('delegatee_id')
        batch_op.drop_column('delegator_id')

    with op.batch_alter_table('files', schema=None) as batch_op:
        batch_op.drop_column('deleted_at')
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')
        batch_op.drop_column('path')
        batch_op.drop_column('type')

    op.drop_table('logs')
    # ### end Alembic commands ###