# -*- coding: utf-8 -*-

from typing import Any

from fastapi import HTTPException
from grpc._channel import _InactiveRpcError
from immudb import ImmudbClient
from immudb.constants import PERMISSION_R, PERMISSION_RW
from immudb.datatypesv2 import PrimaryKeyIntValue

from forms.constants import USER_TYPE_READ, USER_TYPE_READ_WRITE
from settings import IMMUDB_CERT, IMMUDB_URL

DATABASE = "bbdd"
DATABASE_ADMIN_USER = "immudb"
DATABASE_ADMIN_PASSWORD = "immudb"
DATABASE_PASSWORD = "P4ssw=rd"


class ImmuDB:
    def __init__(
        self,
        email: str = "",
        bucket: str = "",
        _type: str = "",
    ) -> None:
        self.connection = ImmudbClient(IMMUDB_URL, publicKeyFile=IMMUDB_CERT)
        self.email = email
        self.bucket = bucket
        self._type = _type
        self.database = DATABASE

    def _login(self) -> None:
        if self._type == USER_TYPE_READ:
            self.connection.login(f"{self.database}_read", DATABASE_PASSWORD, DATABASE)
        elif self._type == USER_TYPE_READ_WRITE:
            self.connection.login(f"{self.database}_read_write", DATABASE_PASSWORD, DATABASE)
        self.connection.useDatabase(DATABASE.encode("utf8"))

    def _users_get(self, name: str) -> bool:
        raw = self.connection.listUsers()
        for raw_item in raw.userlist.users:
            if name == raw_item.user.decode():
                return True
        return False

    def users_create(self) -> None:
        self.connection.login(username=DATABASE_ADMIN_USER, password=DATABASE_ADMIN_PASSWORD)
        if not self._users_get(f"{self.database}_read"):
            self.connection.createUser(f"{self.database}_read", DATABASE_PASSWORD, PERMISSION_R, self.database)
        if not self._users_get(f"{self.database}_read_write"):
            self.connection.createUser(f"{self.database}_read_write", DATABASE_PASSWORD, PERMISSION_RW, self.database)
        self.connection.logout()

    def _logout(self) -> None:
        self.connection.logout()

    def execute(self, sql: str) -> Any:
        self._login()
        try:
            raw = self.connection.sqlExec(sql)
        except _InactiveRpcError as err:  # maybe it's a user with only read permissions
            raise HTTPException(status_code=403, detail=str(err)) from err
        self._logout()
        return raw

    def query(self, sql: str) -> Any:
        self._login()
        raw = self.connection.sqlQuery(sql)
        self._logout()
        return raw

    # https://github.com/codenotary/immudb-py/blob/6af811b354b640615b75d933eaede712660aebf8/tests/immu/test_sql_verify.py#L38
    def verify(self, table: str, _id: int) -> Any:
        self._login()
        raw = self.connection.verifiableSQLGet(
            table=table,
            primaryKeys=[PrimaryKeyIntValue(_id)],
        )
        self._logout()
        return raw
