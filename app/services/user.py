# -*- coding: utf-8 -*-

from sqlalchemy.orm import Session

from forms.user import UserForm
from models.user import User
from repositories.user import UserRepository


class UserService:
    def __init__(self) -> None:
        self.repository = UserRepository

    def create(
        self,
        session: Session,
        item: UserForm,
    ) -> User:
        repo = self.repository(session)
        return repo.create(item=item)

    def get(
        self,
        session: Session,
        email: str,
    ) -> User:
        repo = self.repository(session)
        return repo.get(reference=email)
