# -*- coding: utf-8 -*-

# mypy: disable-error-code=attr-defined
# pylint:disable=no-member

from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from pytest import MonkeyPatch

from models.bucket import Bucket
from models.user import User
from tests.base import _client  # noqa:F401 pylint:disable=unused-import
from tests.base import session  # noqa:F401 pylint:disable=unused-import
from utils import auth

from . import URL_API_V1
from .test_buckets import _bucket  # noqa:F401 pylint:disable=unused-import
from .test_users import URL_API_V1_USERS
from .test_users import _user  # noqa:F401 pylint:disable=unused-import

URL_API_V1_LOGS: str = f"{URL_API_V1}/logs"


class TestLogService:
    def test_create_without_permissions(
        self,
        _client: TestClient,
        _user: User,
        _bucket: Bucket,
        monkeypatch: MonkeyPatch,
    ) -> None:
        user = _user()
        bucket = _bucket(user)
        monkeypatch.setattr(auth, "get_user", MagicMock(return_value=user))
        response = _client.post(
            f"{URL_API_V1_USERS}/login/",
            json={
                "email": user.email,
                "password": "123456",
                "type": "read",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "login" in data
        assert "token" in data["login"]
        token = data["login"]["token"]
        response = _client.post(
            f"{URL_API_V1_LOGS}/{bucket.name}",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json=[
                {
                    "source": "web",
                    "data": {
                        "a": 1,
                        "b": 2,
                        "c": 3,
                    },
                },
                {
                    "source": "web",
                    "data": {
                        "a": 4,
                        "b": 5,
                        "c": 6,
                    },
                },
            ],
        )
        assert response.status_code == 403

    def test_create(
        self,
        _client: TestClient,
        _user: User,
        _bucket: Bucket,
        monkeypatch: MonkeyPatch,
    ) -> None:
        user = _user()
        bucket = _bucket(user)
        monkeypatch.setattr(auth, "get_user", MagicMock(return_value=user))
        response = _client.post(
            f"{URL_API_V1_USERS}/login/",
            json={
                "email": user.email,
                "password": "123456",
                "type": "read-write",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "login" in data
        assert "token" in data["login"]
        token = data["login"]["token"]
        response = _client.post(
            f"{URL_API_V1_LOGS}/{bucket.name}",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json=[
                {
                    "source": "web",
                    "data": {
                        "a": 1,
                        "b": 2,
                        "c": 3,
                    },
                },
                {
                    "source": "web",
                    "data": {
                        "a": 4,
                        "b": 5,
                        "c": 6,
                    },
                },
            ],
        )
        assert response.status_code == 201
        data = response.json()
        assert len(data) == 2
        assert "id" in data[0]
        assert "source" in data[0]
        assert "data" in data[0]
        assert "bucket" in data[0]
        assert "email" in data[0]
        assert "verified" in data[0]
        assert data[0]["verified"] is True

    def test_list(
        self,
        _client: TestClient,
        _user: User,
        _bucket: Bucket,
        monkeypatch: MonkeyPatch,
    ) -> None:
        user = _user()
        bucket = _bucket(user)
        monkeypatch.setattr(auth, "get_user", MagicMock(return_value=user))
        response = _client.post(
            f"{URL_API_V1_USERS}/login/",
            json={
                "email": user.email,
                "password": "123456",
                "type": "read-write",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "login" in data
        assert "token" in data["login"]
        token = data["login"]["token"]
        response = _client.post(
            f"{URL_API_V1_LOGS}/{bucket.name}/",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json=[
                {
                    "source": "cellphone",
                    "data": {
                        "a": 1,
                        "b": 2,
                        "c": 3,
                    },
                },
                {
                    "source": "cellphone",
                    "data": {
                        "a": 4,
                        "b": 5,
                        "c": 6,
                    },
                },
                {
                    "source": "app",
                    "data": {
                        "a": 7,
                        "b": 8,
                        "c": 9,
                    },
                },
            ],
        )
        assert response.status_code == 201
        response = _client.get(
            f"{URL_API_V1_LOGS}/",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert "id" in data[0]
        assert "source" in data[0]
        assert "data" in data[0]
        assert "bucket" in data[0]
        assert "email" in data[0]
        assert "verified" in data[0]
        assert data[0]["verified"] is True

    def test_list_in_bucket(
        self,
        _client: TestClient,
        _user: User,
        _bucket: Bucket,
        monkeypatch: MonkeyPatch,
    ) -> None:
        user = _user()
        bucket = _bucket(user)
        monkeypatch.setattr(auth, "get_user", MagicMock(return_value=user))
        response = _client.post(
            f"{URL_API_V1_USERS}/login/",
            json={
                "email": user.email,
                "password": "123456",
                "type": "read-write",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "login" in data
        assert "token" in data["login"]
        token = data["login"]["token"]
        response = _client.post(
            f"{URL_API_V1_LOGS}/{bucket.name}/",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json=[
                {
                    "source": "cellphone",
                    "data": {
                        "a": 1,
                        "b": 2,
                        "c": 3,
                    },
                },
                {
                    "source": "cellphone",
                    "data": {
                        "a": 4,
                        "b": 5,
                        "c": 6,
                    },
                },
            ],
        )
        assert response.status_code == 201
        response = _client.get(
            f"{URL_API_V1_LOGS}/{bucket.name}/",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert "id" in data[0]
        assert "source" in data[0]
        assert "data" in data[0]
        assert "bucket" in data[0]
        assert "email" in data[0]
        assert "verified" in data[0]
        assert data[0]["verified"] is True

    def test_list_in_bucket_last_x(
        self,
        _client: TestClient,
        _user: User,
        _bucket: Bucket,
        monkeypatch: MonkeyPatch,
    ) -> None:
        user = _user()
        bucket = _bucket(user)
        monkeypatch.setattr(auth, "get_user", MagicMock(return_value=user))
        response = _client.post(
            f"{URL_API_V1_USERS}/login/",
            json={
                "email": user.email,
                "password": "123456",
                "type": "read-write",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "login" in data
        assert "token" in data["login"]
        token = data["login"]["token"]
        response = _client.post(
            f"{URL_API_V1_LOGS}/{bucket.name}/",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json=[
                {"source": "cellphone-1", "data": {}},
                {"source": "cellphone-2", "data": {}},
                {"source": "cellphone-3", "data": {}},
                {"source": "cellphone-4", "data": {}},
                {"source": "cellphone-5", "data": {}},
            ],
        )
        assert response.status_code == 201
        response = _client.get(
            f"{URL_API_V1_LOGS}/{bucket.name}/",
            headers={
                "Authorization": f"Bearer {token}",
            },
            params={
                "page_size": 2,
                "order_by": "desc",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert "id" in data[0]
        assert "source" in data[0]
        assert "data" in data[0]
        assert "bucket" in data[0]
        assert "email" in data[0]
        assert "verified" in data[0]
        assert data[0]["verified"] is True
        assert data[0]["source"] == "cellphone-5"
        assert data[1]["source"] == "cellphone-4"

    def test_list_in_stats(
        self,
        _client: TestClient,
        _user: User,
        _bucket: Bucket,
        monkeypatch: MonkeyPatch,
    ) -> None:
        user = _user()
        bucket = _bucket(user)
        monkeypatch.setattr(auth, "get_user", MagicMock(return_value=user))
        response = _client.post(
            f"{URL_API_V1_USERS}/login/",
            json={
                "email": user.email,
                "password": "123456",
                "type": "read-write",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "login" in data
        assert "token" in data["login"]
        token = data["login"]["token"]
        response = _client.post(
            f"{URL_API_V1_LOGS}/{bucket.name}/",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json=[
                {"source": "cellphone-1", "data": {}},
                {"source": "cellphone-2", "data": {}},
                {"source": "cellphone-3", "data": {}},
                {"source": "cellphone-4", "data": {}},
                {"source": "cellphone-5", "data": {}},
            ],
        )
        assert response.status_code == 201
        response = _client.get(
            f"{URL_API_V1_LOGS}/{bucket.name}/stats/",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "n" in data
        assert data["n"] == 5
        response = _client.get(
            f"{URL_API_V1_LOGS}/stats/",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "n" in data
        assert data["n"] == 5

    def test_list_in_bucket_stats(
        self,
        _client: TestClient,
        _user: User,
        _bucket: Bucket,
        monkeypatch: MonkeyPatch,
    ) -> None:
        user = _user()
        bucket = _bucket(user)
        monkeypatch.setattr(auth, "get_user", MagicMock(return_value=user))
        response = _client.post(
            f"{URL_API_V1_USERS}/login/",
            json={
                "email": user.email,
                "password": "123456",
                "type": "read-write",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "login" in data
        assert "token" in data["login"]
        token = data["login"]["token"]
        response = _client.post(
            f"{URL_API_V1_LOGS}/{bucket.name}/",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json=[
                {"source": "cellphone-1", "data": {}},
                {"source": "cellphone-2", "data": {}},
                {"source": "cellphone-3", "data": {}},
                {"source": "cellphone-4", "data": {}},
                {"source": "cellphone-5", "data": {}},
            ],
        )
        assert response.status_code == 201
        response = _client.get(
            f"{URL_API_V1_LOGS}/{bucket.name}/stats/",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "n" in data
        assert data["n"] == 5
        response = _client.get(
            f"{URL_API_V1_LOGS}/{bucket.name}/stats/",
            headers={
                "Authorization": f"Bearer {token}",
            },
            params={
                "source": "cellphone-1",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "n" in data
        assert data["n"] == 1

    def test_get(
        self,
        _client: TestClient,
        _user: User,
        _bucket: Bucket,
        monkeypatch: MonkeyPatch,
    ) -> None:
        user = _user()
        bucket = _bucket(user)
        monkeypatch.setattr(auth, "get_user", MagicMock(return_value=user))
        response = _client.post(
            f"{URL_API_V1_USERS}/login/",
            json={
                "email": user.email,
                "password": "123456",
                "type": "read-write",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "login" in data
        assert "token" in data["login"]
        token = data["login"]["token"]
        response = _client.post(
            f"{URL_API_V1_LOGS}/{bucket.name}/",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json=[
                {
                    "source": "cellphone",
                    "data": {
                        "a": 1,
                        "b": 2,
                        "c": 3,
                    },
                },
            ],
        )
        assert response.status_code == 201
        data = response.json()
        _id = data[0]["id"]
        response = _client.get(
            f"{URL_API_V1_LOGS}/{bucket.name}/{_id}/",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )
        print(response.url)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "source" in data
        assert "data" in data
        assert "bucket" in data
        assert "email" in data
        assert "verified" in data
        assert data["verified"] is True
