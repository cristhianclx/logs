# -*- coding: utf-8 -*-

from string import ascii_lowercase

from faker import Factory
from fastapi.testclient import TestClient
from immudb.datatypesv2 import DatabaseSettingsV2
from pytest import MonkeyPatch, fixture as pytest__fixture
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.orm import Base
from utils.immudb import DATABASE_ADMIN_PASSWORD, DATABASE_ADMIN_USER, ImmuDB

DATABASE_URL = "sqlite:///./tests.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def override__get__database() -> sessionmaker:
    try:
        database = TestingSessionLocal()  # pylint:disable=redefined-outer-name
        yield database
    finally:
        database.close()


Base.metadata.create_all(bind=engine)


from models.log import Base as LogBase  # noqa:E402 pylint:disable=wrong-import-position

DATABASE_NAME = Factory.create().bothify(text="????", letters=ascii_lowercase)  # pylint:disable=no-member

database = ImmuDB()
database.connection.login(username=DATABASE_ADMIN_USER, password=DATABASE_ADMIN_PASSWORD)
database.connection.createDatabaseV2(DATABASE_NAME, settings=DatabaseSettingsV2(), ifNotExists=True)
database.connection.useDatabase(DATABASE_NAME.encode("utf8"))
for table in LogBase.metadata.tables.values():
    SQL: str = str(sa.schema.CreateTable(table).compile(dialect=sa.dialects.sqlite.dialect()))
    SQL = SQL.replace("PRIMARY KEY AUTOINCREMENT", "AUTO_INCREMENT").replace(")", ", PRIMARY KEY(id))")
    database.connection.sqlExec(SQL)
database.connection.logout()
database.database = DATABASE_NAME
database.users_create()


@pytest__fixture
def _client(monkeypatch: MonkeyPatch) -> TestClient:
    from utils import database  # pylint:disable=import-outside-toplevel,redefined-outer-name

    monkeypatch.setattr(database, "get__database", override__get__database)

    from settings import active  # pylint:disable=import-outside-toplevel

    monkeypatch.setattr(
        active,
        "STATIC_DIR",
        "/code/app/static",
    )
    monkeypatch.setattr(
        active,
        "TEMPLATES_DIR",
        "/code/app/templates",
    )
    monkeypatch.setattr(
        active,
        "RATE_THROTTLING_PER_SECOND",
        1000,
    )
    monkeypatch.setattr(
        active,
        "RATE_THROTTLING_PER_MINUTE",
        10000,
    )

    from utils import immudb  # pylint:disable=import-outside-toplevel

    monkeypatch.setattr(
        immudb,
        "DATABASE",
        DATABASE_NAME,
    )

    from main import app  # pylint:disable=import-outside-toplevel

    return TestClient(app)


@pytest__fixture
def session() -> sessionmaker:
    try:
        database = TestingSessionLocal()  # pylint:disable=redefined-outer-name
        yield database
    finally:
        database.close()
