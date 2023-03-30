# -*- coding: utf-8 -*-

from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from forms.constants import USER_TYPE_READ_WRITE
from forms.user import UserBaseForm, UserForm, UserLoginForm
from services.user import UserService
from settings import ACCESS_TOKEN_EXPIRE_MINUTES
from utils.auth import authenticate_user, create_access_token
from utils.database import get__database

router = APIRouter()

service = UserService()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(item: UserForm, session: Session = Depends(get__database)) -> Any:
    """
    to create a new user with a token
    """
    if service.get(session, item.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already registered",
        )
    user = service.create(session, item)
    context = UserBaseForm.from_orm(user).dict()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.email,
            "type": USER_TYPE_READ_WRITE,
        },
        expires_delta=access_token_expires,
    )
    context["login"] = {
        "token": access_token,
    }
    return context


@router.post("/login/")
def login(item: UserLoginForm, session: Session = Depends(get__database)) -> Any:
    """
    to login and get a token
    """
    user = service.get(session, item.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't exist",
        )
    user = authenticate_user(session, item.email, item.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong credentials",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.email,
            "type": item.type,
        },
        expires_delta=access_token_expires,
    )
    return {
        "login": {
            "token": access_token,
        }
    }
