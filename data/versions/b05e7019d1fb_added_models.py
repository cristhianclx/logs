# mypy: ignore-errors

"""added models

Revision ID: b05e7019d1fb
Revises:
Create Date: 2023-03-28 05:37:18.648455

"""

# pylint: skip-file

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "b05e7019d1fb"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("email"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=False)
    op.create_index(op.f("ix_users_first_name"), "users", ["first_name"], unique=False)
    op.create_index(op.f("ix_users_last_name"), "users", ["last_name"], unique=False)
    op.create_table(
        "buckets",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("user_email", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_email"],
            ["users.email"],
        ),
        sa.PrimaryKeyConstraint("name"),
    )
    op.create_index(op.f("ix_buckets_name"), "buckets", ["name"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_buckets_name"), table_name="buckets")
    op.drop_table("buckets")
    op.drop_index(op.f("ix_users_last_name"), table_name="users")
    op.drop_index(op.f("ix_users_first_name"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###
