# -*- coding: utf-8 -*-

from typing import Any

from redis import ConnectionPool, StrictRedis

from settings import CACHE_URL

CACHE_EXPIRY_TIME = 60 * 60


class CacheMixin:
    def _generate_key(self, api_key: str, identifier: str) -> str:
        return f"{self.CACHE_NAME}:{api_key}:{identifier}"  # type: ignore [attr-defined]


class BaseCache:
    def __init__(self) -> None:
        self.cache = StrictRedis(
            connection_pool=ConnectionPool.from_url(CACHE_URL), charset="utf-8", decode_responses=True
        )

    def _get_value(self, key: str) -> Any:
        return self.cache.get(key)

    def _set_value(self, key: str, value: Any, timeout: int) -> None:
        self.cache.set(key, value, timeout)

    def _incr_value(self, key: str, amount: int = 1, timeout: int = CACHE_EXPIRY_TIME) -> Any:
        try:
            return self.cache.incr(key, amount)
        except ValueError:
            self._set_value(key, amount, timeout=timeout)
            return amount

    def _delete_value(self, key: str) -> None:
        self.cache.delete(key)

    def clear(self) -> None:
        self.cache.delete(*self.cache.keys("*"))
