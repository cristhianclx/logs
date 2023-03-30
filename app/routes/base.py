# -*- coding: utf-8 -*-

from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get("/ping/", summary="ping")
def ping() -> Any:
    """
    ping status for system, to know everything is working OK
    """
    context = {
        "message": "pong",
    }
    return context
