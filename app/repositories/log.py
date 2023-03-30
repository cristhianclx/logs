# -*- coding: utf-8 -*-

from json import dumps as json_dumps, loads as json_loads
from typing import List, Optional

from sqlalchemy import dialects, func, insert, select

from forms.log import LogCreateForm, LogForm
from models.log import Log
from utils.immudb import ImmuDB


class LogRepository:
    def __init__(
        self,
        email: str = "",
        bucket: str = "",
        _type: str = "",
    ) -> None:
        self.model = Log
        self.form = LogForm
        self.email = email
        self.bucket = bucket
        self.type = _type
        self.database = ImmuDB(
            email=self.email,
            bucket=self.bucket,
            _type=self.type,
        )

    def create(self, item: LogCreateForm) -> LogForm:
        values = item.dict()
        values.update(
            email=self.email,
            bucket=self.bucket,
        )
        values["data"] = json_dumps(values["data"])
        sql = str(
            insert(Log)
            .values(values)
            .inline()
            .compile(dialect=dialects.postgresql.dialect(), compile_kwargs={"literal_binds": True})
        )
        raw = self.database.execute(sql)
        _id = raw.txs[0].lastInsertedPKs["logs"].n
        sql = str(
            select(Log)
            .where(Log.id == _id)
            .compile(dialect=dialects.postgresql.dialect(), compile_kwargs={"literal_binds": True})
        )
        raw = self.database.query(sql)
        item = dict(zip(self.model.__table__._columns.keys(), raw[0]))  # pylint:disable=protected-access
        item["data"] = json_loads(item["data"])
        item["verified"] = self.database.verify(self.model.__table__.name, item["id"]).verified
        return self.form(**item)

    def create_batch(self, items: List[LogCreateForm]) -> List[LogForm]:
        values = []
        for item in items:
            value = item.dict()
            value.update(
                email=self.email,
                bucket=self.bucket,
            )
            value["data"] = json_dumps(value["data"])
            values.append(value)
        sql = str(
            insert(Log)
            .values(values)
            .inline()
            .compile(dialect=dialects.postgresql.dialect(), compile_kwargs={"literal_binds": True})
        )
        raw = self.database.execute(sql)
        ids = list(range(raw.txs[0].firstInsertedPKs["logs"].n, raw.txs[0].lastInsertedPKs["logs"].n + 1))
        sql = str(
            select(Log)
            .where(Log.id.in_(ids))
            .compile(dialect=dialects.postgresql.dialect(), compile_kwargs={"literal_binds": True})
        )
        raw = self.database.query(sql)
        items = [dict(zip(self.model.__table__._columns.keys(), r)) for r in raw]  # pylint:disable=protected-access
        for item in items:
            item["data"] = json_loads(item["data"])
            item["verified"] = self.database.verify(self.model.__table__.name, item["id"]).verified
        return [self.form(**item) for item in items]

    def list(self, source: str = None, page_size: int = None, page: int = None, order_by: str = "asc") -> List[LogForm]:
        query = select(Log).where(self.model.email == self.email)
        if self.bucket and self.bucket != "":
            query = query.where(
                self.model.bucket == self.bucket,
            )
        if source:
            query = query.where(
                self.model.source == source,
            )
        if page and page_size:
            query = query.offset((page - 1) * page_size)
        if page_size:
            query = query.limit(page_size)
        if order_by == "asc":
            query = query.order_by(self.model.id.asc())
        if order_by == "desc":
            query = query.order_by(self.model.id.desc())
        sql = str(query.compile(dialect=dialects.postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        raw = self.database.query(sql)
        items = [dict(zip(self.model.__table__._columns.keys(), r)) for r in raw]  # pylint:disable=protected-access
        for item in items:
            item["data"] = json_loads(item["data"])
            item["verified"] = self.database.verify(self.model.__table__.name, item["id"]).verified
        return [self.form(**item) for item in items]

    def get(self, _id: int) -> Optional[LogForm]:
        sql = str(
            select(Log)
            .where(
                self.model.email == self.email,
                self.model.bucket == self.bucket,
                self.model.id == _id,
            )
            .compile(dialect=dialects.postgresql.dialect(), compile_kwargs={"literal_binds": True})
        )
        raw = self.database.query(sql)
        if len(raw) == 0:
            return None
        item = dict(zip(self.model.__table__._columns.keys(), raw[0]))  # pylint:disable=protected-access
        item["data"] = json_loads(item["data"])
        item["verified"] = self.database.verify(self.model.__table__.name, item["id"]).verified
        return self.form(**item)

    def stats(self, source: str = None) -> dict:
        query = (  # pylint:disable-next=not-callable
            select(func.count())
            .select_from(Log)
            .where(
                self.model.email == self.email,
            )
        )
        if self.bucket and self.bucket != "":
            query = query.where(
                self.model.bucket == self.bucket,
            )
        if source:
            query = query.where(
                self.model.source == source,
            )
        sql = str(query.compile(dialect=dialects.postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        raw = self.database.query(sql)
        return {
            "n": raw[0][0],
        }
