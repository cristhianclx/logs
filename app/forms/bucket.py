# -*- coding: utf-8 -*-

from db.schemas import Base


class BucketForm(Base):
    name: str

    class Config:
        orm_mode = True
