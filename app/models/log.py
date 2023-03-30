# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.decl_api import DeclarativeMeta

Base: DeclarativeMeta = declarative_base()


class Log(Base):
    __tablename__: str = "logs"
    __table_args__: dict = {
        "sqlite_autoincrement": True,
    }

    id = Column(
        Integer,
        primary_key=True,
        nullable=True,
        autoincrement=True,
    )
    source = Column(
        String,
        nullable=True,
    )
    data = Column(
        String,
        nullable=False,
    )
    bucket = Column(
        String,
        index=True,
        nullable=False,
    )
    email = Column(
        String,
        index=True,
        nullable=False,
    )
