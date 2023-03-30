# -*- coding: utf-8 -*-

from typing import Generator

from db.engine import SessionLocal


def get__database() -> Generator:
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()
