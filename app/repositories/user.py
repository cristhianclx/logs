# -*- coding: utf-8 -*-

from sqlalchemy.orm import Session

from forms.user import UserForm
from models.user import User

from .bucket import BucketRepository


class UserRepository:
    def __init__(self, session: Session):
        self.model = User
        self.session = session

    def create(self, item: UserForm) -> User:
        values = item.dict()
        item = self.model(**values)
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        repo = BucketRepository(session=self.session)
        repo.get_or_create(
            reference=str(item.email),
            user=item,
        )
        return item

    def get(self, reference: str) -> User:
        return (
            self.session.query(self.model)
            .filter(
                self.model.email == reference,
            )
            .first()
        )
