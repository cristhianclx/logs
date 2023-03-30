# -*- coding: utf-8 -*-

from fastapi import APIRouter

from .bucket import router as router__bucket
from .log import router as router__log
from .user import router as router__user

router = APIRouter()

router.include_router(
    router__user,
    prefix="/users",
    tags=["users"],
)
router.include_router(
    router__bucket,
    prefix="/buckets",
    tags=["buckets"],
)
router.include_router(
    router__log,
    prefix="/logs",
    tags=["logs"],
)
