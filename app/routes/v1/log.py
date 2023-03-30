# -*- coding: utf-8 -*-

from typing import Any, List, Literal, Tuple

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from forms.log import LogCreateForm
from models.user import User
from repositories.log import LogRepository
from services.bucket import BucketService
from utils.database import get__database
from utils.metering import get_api_usage

auth_scheme = HTTPBearer()
router = APIRouter()

service = BucketService()


@router.get("/")
def get_all(  # pylint:disable=too-many-arguments
    source: str = None,
    page_size: int = None,
    page: int = None,
    order_by: Literal["asc", "desc"] = "asc",
    user_with_api_usage: Tuple[User, str, dict] = Depends(get_api_usage),  # pylint:disable=unused-argument
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),  # pylint:disable=unused-argument
) -> Any:
    """
    to get all logs
    """
    user, user_type, usage = user_with_api_usage  # pylint:disable=unused-variable
    repo = LogRepository(
        email=str(user.email),
        _type=user_type,
    )
    return repo.list(source, page_size, page, order_by)


@router.get("/stats/")
def stats(
    source: str = None,
    user_with_api_usage: Tuple[User, str, dict] = Depends(get_api_usage),  # pylint:disable=unused-argument
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),  # pylint:disable=unused-argument
) -> Any:
    """
    to get all statistics in a bucket
    """
    user, user_type, usage = user_with_api_usage  # pylint:disable=unused-variable
    repo = LogRepository(
        email=str(user.email),
        _type=user_type,
    )
    _stats = repo.stats(source)
    return _stats


@router.post("/{bucket_name}/", status_code=status.HTTP_201_CREATED)
def create_batch(
    bucket_name: str,
    items: List[LogCreateForm],
    session: Session = Depends(get__database),
    user_with_api_usage: Tuple[User, str, dict] = Depends(get_api_usage),  # pylint:disable=unused-argument
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),  # pylint:disable=unused-argument
) -> Any:
    """
    to create logs in a bucket
    """
    user, user_type, usage = user_with_api_usage  # pylint:disable=unused-variable
    bucket = service.get(session, bucket_name, user)
    if not bucket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bucket doesn't exist",
        )
    repo = LogRepository(
        email=str(user.email),
        bucket=bucket_name,
        _type=user_type,
    )
    return repo.create_batch(items)


@router.get("/{bucket_name}/")
def get_all_by_bucket(  # pylint:disable=too-many-arguments
    bucket_name: str,
    source: str = None,
    page_size: int = None,
    page: int = None,
    order_by: Literal["asc", "desc"] = "asc",
    session: Session = Depends(get__database),
    user_with_api_usage: Tuple[User, str, dict] = Depends(get_api_usage),  # pylint:disable=unused-argument
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),  # pylint:disable=unused-argument
) -> Any:
    """
    to get all logs in a bucket
    """
    user, user_type, usage = user_with_api_usage  # pylint:disable=unused-variable
    bucket = service.get(session, bucket_name, user)
    if not bucket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bucket doesn't exist",
        )
    repo = LogRepository(
        email=str(user.email),
        bucket=bucket_name,
        _type=user_type,
    )
    return repo.list(source, page_size, page, order_by)


@router.get("/{bucket_name}/stats/")
def stats_by_bucket(
    bucket_name: str,
    source: str = None,
    session: Session = Depends(get__database),
    user_with_api_usage: Tuple[User, str, dict] = Depends(get_api_usage),  # pylint:disable=unused-argument
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),  # pylint:disable=unused-argument
) -> Any:
    """
    to get all statistics in a bucket
    """
    user, user_type, usage = user_with_api_usage  # pylint:disable=unused-variable
    bucket = service.get(session, bucket_name, user)
    if not bucket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bucket doesn't exist",
        )
    repo = LogRepository(
        email=str(user.email),
        bucket=bucket_name,
        _type=user_type,
    )
    _stats = repo.stats(source)
    return _stats


@router.get("/{bucket_name}/{_id}/")
def get(
    bucket_name: str,
    _id: int,
    session: Session = Depends(get__database),
    user_with_api_usage: Tuple[User, str, dict] = Depends(get_api_usage),  # pylint:disable=unused-argument
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),  # pylint:disable=unused-argument
) -> Any:
    """
    to get a log in a bucket
    """
    user, user_type, usage = user_with_api_usage  # pylint:disable=unused-variable
    bucket = service.get(session, bucket_name, user)
    if not bucket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bucket doesn't exist",
        )
    repo = LogRepository(
        email=str(user.email),
        bucket=bucket_name,
        _type=user_type,
    )
    log = repo.get(_id)
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Log doesn't exist",
        )
    return log
