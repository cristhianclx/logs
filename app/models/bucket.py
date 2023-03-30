# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from db.orm import ModelBase


class Bucket(ModelBase):
    __tablename__: str = "buckets"

    name = Column(
        String,
        primary_key=True,
        index=True,
        nullable=False,
    )
    user_email = Column(
        String,
        ForeignKey("users.email"),
    )

    user = relationship("User", back_populates="buckets")
