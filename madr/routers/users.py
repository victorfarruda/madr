from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, select

from madr.models import User
from madr.schemas import UserPublic, UserSchema, UserUpdate
from madr.security import get_current_active_user, get_password_hash
from madr.t_types import T_Session

router = APIRouter(prefix='/users', tags=['users'])
T_CurrentActiveUser = Annotated[UserPublic, Depends(get_current_active_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: T_Session):
    db_user = session.scalar(select(User).where(or_(User.username == user.username, User.email == user.email)))

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )

    hashed_password = get_password_hash(user.password)

    db_user = User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        disabled=user.disabled,
        hashed_password=hashed_password,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/me', response_model=UserPublic)
def get_user(current_user: T_CurrentActiveUser):
    return current_user


@router.patch('/me', response_model=UserPublic)
def patch_user(session: T_Session, user_update: UserUpdate, current_user: T_CurrentActiveUser):
    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(current_user, key, value)

    if user_update.password:
        current_user.hashed_password = get_password_hash(user_update.password)

    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user
