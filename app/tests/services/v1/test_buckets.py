# -*- coding: utf-8 -*-

# mypy: disable-error-code=attr-defined
# pylint:disable=no-member

from datetime import timedelta
from string import ascii_lowercase
from typing import Callable
from unittest.mock import MagicMock

from faker import Factory
from fastapi.testclient import TestClient
from pytest import MonkeyPatch, fixture as pytest__fixture
from sqlalchemy.orm import Session

from models.bucket import Bucket
from models.user import User
from tests.base import _client  # noqa:F401 pylint:disable=unused-import
from tests.base import session  # noqa:F401 pylint:disable=unused-import
from utils import auth
from utils.auth import create_access_token

from . import URL_API_V1
from .test_users import URL_API_V1_USERS
from .test_users import _user  # noqa:F401 pylint:disable=unused-import

URL_API_V1_BUCKETS: str = f"{URL_API_V1}/buckets"

faker = Factory.create()


@pytest__fixture
def _bucket(session: Session) -> Callable[[User], Bucket]:  # pylint:disable=redefined-outer-name
    def __bucket(_user: User) -> Bucket:
        item = Bucket(
            name=faker.bothify(text="?????", letters=ascii_lowercase),
            user_email=_user.email,
        )
        session.add(item)
        session.commit()
        session.refresh(item)
        return item

    return __bucket


class TestBucketService:
    def test_get_without_credentials(self, _client: TestClient, _user: User, _bucket: Bucket) -> None:
        user = _user()
        _bucket(user)
        response = _client.get(f"{URL_API_V1_BUCKETS}/")
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Not authenticated"

    def test_get_with_wrong_credentials(self, _client: TestClient, _user: User, _bucket: Bucket) -> None:
        user = _user()
        _bucket(user)
        response = _client.get(
            f"{URL_API_V1_BUCKETS}/",
            headers={
                "Authorization": "Bearer JWT",
            },
        )
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Could not decode credentials"

    def test_get_with_expired_credentials(self, _client: TestClient, _user: User, _bucket: Bucket) -> None:
        user = _user()
        _bucket(user)
        token = create_access_token(
            data={
                "sub": user.email,
                "type": "read",
            },
            expires_delta=-timedelta(minutes=15),
        )
        response = _client.get(
            f"{URL_API_V1_BUCKETS}/",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Could not decode credentials"

    def test_get(self, _client: TestClient, _user: User, _bucket: Bucket, monkeypatch: MonkeyPatch) -> None:
        user = _user()
        _bucket(user)
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
        response = _client.get(
            f"{URL_API_V1_BUCKETS}/",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert "name" in data[0]


#    def test_get_with_service_down(
#        self,
#        _client: TestClient,
#        _stock: Stock,
#        _user: User,
#        monkeypatch: MonkeyPatch,
#        requests_mock: Mocker,
#    ) -> None:
#        stock = _stock()
#        requests_mock.get(
#            ALPHA_VANTAGE_URL,
#            status_code=503,
#        )
#        user = _user()
#        monkeypatch.setattr(auth, "get_user", MagicMock(return_value=user))
#        response = _client.post(
#            f"{URL_API_V1_USERS}/login/",
#            json={
#                "email": user.email,
#                "password": "123456",
#            },
#        )
#        assert response.status_code == 200
#        data = response.json()
#        assert "login" in data
#        assert "token" in data["login"]
#        token = data["login"]["token"]
#        response = _client.get(
#            f"{URL_API_V1_STOCKS}/{stock.code}/",
#            headers={
#                "Authorization": f"Bearer {token}",
#            },
#        )
#        assert response.status_code == 503

#    def test_get_with_different_keys(
#        self,
#        _client: TestClient,
#        _stock: Stock,
#        _user: User,
#        monkeypatch: MonkeyPatch,
#        requests_mock: Mocker,
#    ) -> None:
#        stock = _stock()
#        requests_mock.get(
#            ALPHA_VANTAGE_URL,
#            text=dumps(
#                {
#                    "Time Series (Daily)": {
#                        "2023-01-10": {
#                            "1. open": "130.96",
#                            "2. high": "133.8494",
#                            "3. low": "130.34",
#                            "4. close": "132.89",
#                        },
#                        "2023-01-09": {
#                            "1. open": "127.27",
#                            "2. high": "133.44",
#                            "3. low": "127.15",
#                            "4. close": "132.99",
#                        },
#                    }
#                }
#            ),
#        )
#        # we can try to get some api keys to test cache
#        for iterator in range(1, 10):  # pylint:disable=unused-variable
#            user = _user()
#            monkeypatch.setattr(auth, "get_user", MagicMock(return_value=user))
#            response = _client.post(
#                f"{URL_API_V1_USERS}/login/",
#                json={
#                    "email": user.email,
#                    "password": "123456",
#                },
#            )
#            assert response.status_code == 200
#            data = response.json()
#            assert "login" in data
#            assert "token" in data["login"]
#            token = data["login"]["token"]
#            response = _client.get(
#                f"{URL_API_V1_STOCKS}/{stock.code}/",
#                headers={
#                    "Authorization": f"Bearer {token}",
#                },
#            )
#            assert response.status_code == 200
#            data = response.json()
#            assert "code" in data
#            assert data["code"] == stock.code
#            assert data["name"] == stock.name
#            assert data["price"] == {"high": 133.8494, "low": 130.34, "open": 130.96, "variation": -0.1}

#    def test_get_with_same_key(
#        self,
#        _client: TestClient,
#        _stock: Stock,
#        _user: User,
#        monkeypatch: MonkeyPatch,
#        requests_mock: Mocker,
#    ) -> None:
#        stock = _stock()
#        requests_mock.get(
#            ALPHA_VANTAGE_URL,
#            text=dumps(
#                {
#                    "Time Series (Daily)": {
#                        "2023-01-10": {
#                            "1. open": "130.96",
#                            "2. high": "133.8494",
#                            "3. low": "130.34",
#                            "4. close": "132.89",
#                        },
#                        "2023-01-09": {
#                            "1. open": "127.27",
#                            "2. high": "133.44",
#                            "3. low": "127.15",
#                            "4. close": "132.99",
#                        },
#                    }
#                }
#            ),
#        )
#        user = _user()
#        monkeypatch.setattr(auth, "get_user", MagicMock(return_value=user))
#        # we can try to do some calls with same api key
#        response_codes_raw = []
#        for iterator in range(1, 100):  # pylint:disable=unused-variable
#            response = _client.post(
#                f"{URL_API_V1_USERS}/login/",
#                json={
#                    "email": user.email,
#                    "password": "123456",
#                },
#            )
#            assert response.status_code == 200
#            data = response.json()
#            assert "login" in data
#            assert "token" in data["login"]
#            token = data["login"]["token"]
#            response = _client.get(
#                f"{URL_API_V1_STOCKS}/{stock.code}/",
#                headers={
#                    "Authorization": f"Bearer {token}",
#                },
#            )
#            assert response.status_code in [200, 429]
#            response_codes_raw.append(response.status_code)
#        response_codes = Counter(response_codes_raw)
#        assert response_codes[200] > 1
#        assert response_codes[429] > 1
