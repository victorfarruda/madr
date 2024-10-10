from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from jwt import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy import or_, select

from madr.models import User
from madr.schemas import TokenData, UserPublic
from madr.settings import settings
from madr.t_types import T_OAuthSchema, T_Session

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_current_user(token: T_OAuthSchema, session: T_Session):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    db_user = session.scalar(
        select(User).where(or_(User.username == token_data.username, User.email == token_data.username))
    )

    if db_user is None:
        raise credentials_exception
    return db_user


def get_current_active_user(current_user: Annotated[UserPublic, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Inactive user')
    return current_user
