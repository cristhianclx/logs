# -*- coding: utf-8 -*-

from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from db.orm import ModelBase


class User(ModelBase):
    __tablename__: str = "users"

    email = Column(
        String,
        primary_key=True,
        index=True,
        nullable=False,
    )
    first_name = Column(
        String,
        index=True,
        nullable=True,
    )
    last_name = Column(
        String,
        index=True,
        nullable=True,
    )
    password = Column(
        String,
        nullable=False,
    )
    is_active = Column(
        Boolean,
        default=True,
    )

    buckets = relationship("Bucket", back_populates="user")
