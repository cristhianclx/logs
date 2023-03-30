# mypy: ignore-errors

"""added logs

Revision ID: 14a111e37223
Revises: a328a6546f03
Create Date: 2023-03-28 04:04:08.393286

"""

# pylint: skip-file

import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "14a111e37223"
down_revision = "b05e7019d1fb"
branch_labels = None
depends_on = None


def replace(sql):
    sql = sql.replace("SERIAL", "INTEGER AUTO_INCREMENT")
    return sql


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    from immudb.datatypesv2 import DatabaseSettingsV2

    from utils.immudb import DATABASE, DATABASE_ADMIN_PASSWORD, DATABASE_ADMIN_USER, ImmuDB

    database = ImmuDB()
    database.connection.login(username=DATABASE_ADMIN_USER, password=DATABASE_ADMIN_PASSWORD)
    database.connection.createDatabaseV2(DATABASE, settings=DatabaseSettingsV2(), ifNotExists=True)
    database.connection.useDatabase(DATABASE.encode("utf8"))
    from models.log import Base

    for table in Base.metadata.tables.values():
        sql = str(sa.schema.CreateTable(table).compile(dialect=sa.dialects.postgresql.dialect()))
        sql = replace(sql)
        import ipdb; ipdb.set_trace()
        database.connection.sqlExec(sql)
    database.connection.logout()
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    from immudb.datatypesv2 import DatabaseSettingsV2

    from utils.immudb import DATABASE, DATABASE_ADMIN_PASSWORD, DATABASE_ADMIN_USER, ImmuDB

    database = ImmuDB()
    database.connection.login(username=DATABASE_ADMIN_USER, password=DATABASE_ADMIN_PASSWORD)
    database.connection.createDatabaseV2(DATABASE, settings=DatabaseSettingsV2(), ifNotExists=True)
    database.connection.useDatabase(DATABASE.encode("utf8"))
    from models.log import Base

    for table in Base.metadata.tables.values():
        sql = str(sa.schema.DropTable(table).compile(dialect=sa.dialects.postgresql.dialect()))
        sql = replace(sql)
        database.connection.sqlExec(sql)
    database.connection.logout()
    # ### end Alembic commands ###
