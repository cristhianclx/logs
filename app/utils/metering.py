# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Tuple

from fastapi import Depends, HTTPException, status

from models.user import User
from utils.auth import get_current_active_user
from utils.cache import BaseCache, CacheMixin


class MeteringCache(BaseCache, CacheMixin):
    CACHE_NAME = "metering"

    def _generate_usage_key_per_second(self, api_key: str) -> str:
        return self._generate_key(api_key, datetime.utcnow().strftime("%Y%m%d-%H%M%S"))

    def _generate_usage_key_per_minute(self, api_key: str) -> str:
        return self._generate_key(api_key, datetime.utcnow().strftime("%Y%m%d-%H%M"))

    def increment_api_usage(self, api_key: str) -> dict:
        usage_per_second = self._incr_value(self._generate_usage_key_per_second(api_key))
        usage_per_minute = self._incr_value(self._generate_usage_key_per_minute(api_key))
        return {
            "per_second": usage_per_second,
            "per_minute": usage_per_minute,
        }

    def get_api_usage(self, api_key: str) -> dict:
        usage_per_second = int(self._get_value(self._generate_usage_key_per_second(api_key)) or 0)
        usage_per_minute = int(self._get_value(self._generate_usage_key_per_minute(api_key)) or 0)
        return {
            "per_second": usage_per_second,
            "per_minute": usage_per_minute,
        }


def get_api_usage(
    current_user_with_token: Tuple[User, str, str] = Depends(get_current_active_user)
) -> Tuple[User, str, dict]:
    from settings.active import (  # pylint:disable=import-outside-toplevel
        RATE_THROTTLING_PER_MINUTE,
        RATE_THROTTLING_PER_SECOND,
    )

    current_user, token, _type = current_user_with_token
    usage = MeteringCache().get_api_usage(token)
    if usage["per_second"] >= RATE_THROTTLING_PER_SECOND:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Throttling per second")
    if usage["per_minute"] >= RATE_THROTTLING_PER_MINUTE:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Throttling per minute")
    return current_user, _type, MeteringCache().increment_api_usage(token)
