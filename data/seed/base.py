# -*- coding: utf-8 -*-

from typing import Any, List

from db.engine import SessionLocal as Session
from db.orm import Base


def load__data(Model: Base, ModelReference: Any, data: List, reference: Any) -> None:  # pylint: disable=invalid-name
    session = Session()
    IDs = [d[reference] for d in data]  # pylint: disable=invalid-name
    items_in = session.query(Model).filter(ModelReference.in_(IDs)).all()
    items_in_IDs = [i.__dict__[reference] for i in items_in]  # pylint: disable=invalid-name
    items = [Model(**d) for d in data if d[reference] not in items_in_IDs]
    session.add_all(items)
    session.commit()
