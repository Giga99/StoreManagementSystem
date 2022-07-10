"""Changes of tables

Revision ID: c142202735ff
Revises: e3c76dd20009
Create Date: 2022-07-10 14:11:20.028802

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c142202735ff'
down_revision = 'e3c76dd20009'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('numberOfSoldProducts', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('userEmail', sa.String(length=256), nullable=False),
    sa.Column('statusId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['statusId'], ['orderstatus.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('productcategory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('productId', sa.Integer(), nullable=False),
    sa.Column('categoryId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['categoryId'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['productId'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('productorder',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('productId', sa.Integer(), nullable=False),
    sa.Column('orderId', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('received', sa.Integer(), nullable=False),
    sa.Column('requested', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['orderId'], ['orders.id'], ),
    sa.ForeignKeyConstraint(['productId'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('productorder')
    op.drop_table('productcategory')
    op.drop_table('orders')
    op.drop_table('products')
    op.drop_table('categories')
    # ### end Alembic commands ###
