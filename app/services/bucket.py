# -*- coding: utf-8 -*-

from typing import List, Optional

from sqlalchemy.orm import Session

from forms.bucket import BucketForm
from models.bucket import Bucket
from models.user import User
from repositories.bucket import BucketRepository


class BucketService:
    def __init__(self) -> None:
        self.repository = BucketRepository

    def create(
        self,
        session: Session,
        item: BucketForm,
        user: User,
    ) -> Bucket:
        repo = self.repository(session)
        return repo.create(item=item, user=user)

    def get(
        self,
        session: Session,
        name: str,
        user: User,
    ) -> Optional[Bucket]:
        repo = self.repository(session)
        return repo.get(reference=name, user=user)

    def get_or_create(
        self,
        session: Session,
        name: str,
        user: User,
    ) -> Bucket:
        item = self.get(session=session, name=name, user=user)
        if item:
            return item
        return self.create(session=session, item=BucketForm(name=name), user=user)

    def list(
        self,
        session: Session,
        user: User,
    ) -> List[Bucket]:
        repo = self.repository(session)
        return repo.list(user=user)
