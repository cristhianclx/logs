# -*- coding: utf-8 -*-

from fastapi.testclient import TestClient

from tests.base import _client  # noqa:F401 pylint:disable=unused-import


class TestBase:
    def test_root(self, _client: TestClient) -> None:
        response = _client.get("/")
        assert response.status_code == 200
        assert response.url == "http://testserver/docs"

    def test_robots(self, _client: TestClient) -> None:
        response = _client.get("/robots.txt")
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/plain")
        assert response.text == "User-agent: *\nDisallow: /\n"

    def test_favicon(self, _client: TestClient) -> None:
        response = _client.get("/favicon.ico")
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("image/vnd.microsoft.icon")

    def test_ping(self, _client: TestClient) -> None:
        response = _client.get("/ping/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "pong"
