# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from typing import Any, Tuple

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from models.user import User
from settings import ALGORITHM, SECRET_KEY
from utils.database import get__database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenData(BaseModel):
    username: str


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_user(
    session: Session,
    email: str,
) -> Any:
    from services.user import UserService  # pylint:disable=import-outside-toplevel

    service = UserService()
    user = service.get(session, email)
    if not user:
        return False
    return user


def authenticate_user(
    session: Session,
    email: str,
    password: str,
) -> Any:
    user = get_user(session, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def create_access_token(
    data: dict,
    expires_delta: timedelta = None,
) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get__database),
) -> Tuple[User, str, str]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        type_: str = payload.get("type")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_data = TokenData(username=username)
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not decode credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    user = get_user(session, token_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not authenticate user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user, token, type_


def get_current_active_user(
    current_user_with_token: Tuple[User, str, str] = Depends(get_current_user),
) -> Tuple[User, str, str]:
    current_user, token, type_ = current_user_with_token
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user, token, type_
