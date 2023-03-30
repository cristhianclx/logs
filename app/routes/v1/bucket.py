# -*- coding: utf-8 -*-

from typing import Any, Tuple

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from forms.bucket import BucketForm
from models.user import User
from services.bucket import BucketService
from utils.database import get__database
from utils.metering import get_api_usage

auth_scheme = HTTPBearer()
router = APIRouter()

service = BucketService()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(
    item: BucketForm,
    session: Session = Depends(get__database),
    user_with_api_usage: Tuple[User, str, dict] = Depends(get_api_usage),
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),  # pylint:disable=unused-argument,unused-variable
) -> Any:
    """
    to create a new bucket
    """
    user, user_type, usage = user_with_api_usage  # pylint:disable=unused-argument,unused-variable
    if service.get(session, item.name, user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already registered",
        )
    return service.create(session, item, user)


@router.get("/")
def get_all(
    session: Session = Depends(get__database),
    user_with_api_usage: Tuple[User, str, dict] = Depends(get_api_usage),
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),  # pylint:disable=unused-argument,unused-variable
) -> Any:
    """
    to list buckets
    """
    user, user_type, usage = user_with_api_usage  # pylint:disable=unused-argument,unused-variable
    return service.list(session, user)
