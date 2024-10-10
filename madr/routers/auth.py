from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import or_, select

from madr.models import User
from madr.schemas import TokenSchema
from madr.security import create_access_token, verify_password
from madr.t_types import T_FormData, T_Session

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/token')
def login_for_access_token(form_data: T_FormData, session: T_Session) -> TokenSchema:
    db_user = session.scalar(
        select(User).where(or_(User.username == form_data.username, User.email == form_data.username))
    )

    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    access_token = create_access_token(data={'sub': db_user.username})
    return TokenSchema(access_token=access_token, token_type='bearer')
