# -*- coding: utf-8 -*-

from typing import Optional

from db.schemas import Base


class LogCreateForm(Base):
    source: Optional[str] = ""
    data: dict


class LogForm(Base):
    id: int
    source: str
    data: dict
    bucket: str
    email: str
    verified: bool = False
