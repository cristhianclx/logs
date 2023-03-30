# -*- coding: utf-8 -*-

from typing import List, Optional

from sqlalchemy.orm import Session

from forms.bucket import BucketForm
from models.bucket import Bucket
from models.user import User


class BucketRepository:
    def __init__(self, session: Session):
        self.model = Bucket
        self.session = session

    def create(self, item: BucketForm, user: User) -> User:
        values = item.dict()
        item = self.model(**values)
        item.user = user
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def get(self, reference: str, user: User) -> Optional[Bucket]:  # pylint:disable=arguments-differ
        return (
            self.session.query(self.model)
            .filter(
                self.model.name == reference,
                self.model.user == user,
            )
            .first()
        )

    def get_or_create(self, reference: str, user: User) -> Bucket:
        item = self.get(reference=reference, user=user)
        if item:
            return item
        return self.create(item=BucketForm(name=reference), user=user)

    def list(self, user: User) -> List[Bucket]:
        return (
            self.session.query(self.model)
            .filter(
                self.model.user == user,
            )
            .all()
        )
