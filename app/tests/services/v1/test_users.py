# -*- coding: utf-8 -*-

# mypy: disable-error-code=attr-defined
# pylint:disable=no-member

from typing import Callable

from faker import Factory
from fastapi.testclient import TestClient
from pytest import fixture as pytest__fixture
from sqlalchemy.orm import Session

from models.user import User
from tests.base import _client  # noqa:F401 pylint:disable=unused-import
from tests.base import session  # noqa:F401 pylint:disable=unused-import

from . import URL_API_V1

URL_API_V1_USERS: str = f"{URL_API_V1}/users"

faker = Factory.create()


@pytest__fixture
def _user(session: Session) -> Callable[[], User]:  # pylint:disable=redefined-outer-name
    def __user() -> User:
        item = User(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            email=faker.email(),
            password="$2b$12$JvNZ89p2f5E9wL6EBl80Re0boCSb1oPDmMZ60hx5KhN/1zEy6TCrm",
            is_active=True,
        )
        session.add(item)
        session.commit()
        session.refresh(item)
        return item

    return __user


@pytest__fixture
def _user_inactive(session: Session) -> Callable[[], User]:  # pylint:disable=redefined-outer-name
    def __user_inactive() -> User:
        item = User(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            email=faker.email(),
            password="$2b$12$JvNZ89p2f5E9wL6EBl80Re0boCSb1oPDmMZ60hx5KhN/1zEy6TCrm",
            is_active=False,
        )
        session.add(item)
        session.commit()
        session.refresh(item)
        return item

    return __user_inactive


class TestUserService:
    def test_create_empty(self, _client: TestClient) -> None:
        response = _client.post(
            f"{URL_API_V1_USERS}/",
            json={},
        )
        assert response.status_code == 422

    def test_create_error(self, _client: TestClient) -> None:
        response = _client.post(
            f"{URL_API_V1_USERS}/",
            json={
                "first_name": faker.first_name(),
                "last_name": faker.last_name(),
                "email": faker.email(),
            },
        )
        assert response.status_code == 422
        data = response.json()
        assert data["detail"][0]["type"] == "value_error.missing"
        response = _client.post(
            f"{URL_API_V1_USERS}/",
            json={
                "first_name": faker.first_name(),
                "last_name": faker.last_name(),
                "password": faker.email(),
            },
        )
        assert response.status_code == 422
        data = response.json()
        assert data["detail"][0]["type"] == "value_error.missing"
        response = _client.post(
            f"{URL_API_V1_USERS}/",
            json={
                "first_name": faker.first_name(),
                "last_name": faker.last_name(),
                "email": faker.email(),
                "password": "12345",
            },
        )
        assert response.status_code == 422
        data = response.json()
        assert data["detail"][0]["type"] == "value_error"

    def test_create(self, _client: TestClient) -> None:
        response = _client.post(
            f"{URL_API_V1_USERS}/",
            json={
                "first_name": faker.first_name(),
                "last_name": faker.last_name(),
                "email": faker.email(),
                "password": "123456",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert "login" in data
        assert "token" in data["login"]

    def test_create_with_same_email(self, _client: TestClient) -> None:
        email = faker.email()
        response = _client.post(
            f"{URL_API_V1_USERS}/",
            json={
                "first_name": faker.first_name(),
                "last_name": faker.last_name(),
                "email": email,
                "password": "123456",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert "login" in data
        response = _client.post(
            f"{URL_API_V1_USERS}",
            json={
                "first_name": faker.first_name(),
                "last_name": faker.last_name(),
                "email": email,
                "password": "123456",
            },
        )
        assert response.status_code == 400

    def test_login_error(self, _client: TestClient) -> None:
        response = _client.post(
            f"{URL_API_V1_USERS}/login/",
            json={
                "email": faker.email(),
                "password": "54321",
            },
        )
        assert response.status_code == 422

    def test_login_with_not_existing_user(self, _client: TestClient) -> None:
        response = _client.post(
            f"{URL_API_V1_USERS}/login/",
            json={
                "email": faker.email(),
                "password": "123456",
                "type": "read",
            },
        )
        assert response.status_code == 400

    def test_login_with_inactive_user(self, _client: TestClient, _user_inactive: User) -> None:
        response = _client.post(
            f"{URL_API_V1_USERS}/login/",
            json={
                "email": _user_inactive().email,
                "password": "123456",
                "type": "read",
            },
        )
        assert response.status_code == 400

    def test_login_with_invalid_password(self, _client: TestClient, _user: User) -> None:
        response = _client.post(
            f"{URL_API_V1_USERS}/login/",
            json={
                "email": _user().email,
                "password": "654321",
                "type": "read",
            },
        )
        assert response.status_code == 401

    def test_login(self, _client: TestClient, _user: User) -> None:
        response = _client.post(
            f"{URL_API_V1_USERS}/login/",
            json={
                "email": _user().email,
                "password": "123456",
                "type": "read",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "login" in data
        assert "token" in data["login"]
