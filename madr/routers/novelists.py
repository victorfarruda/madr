from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from madr.models import Novelist
from madr.schemas import Message, NovelistList, NovelistPublic, NovelistSchema, NovelistUpdate, UserPublic
from madr.security import get_current_active_user
from madr.t_types import T_Session

router = APIRouter(prefix='/novelists', tags=['novelists'])
T_CurrentActiveUser = Annotated[UserPublic, Depends(get_current_active_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=NovelistPublic)
def create_novelist(novelist: NovelistSchema, session: T_Session, current_user: T_CurrentActiveUser):
    db_novelist: Novelist = Novelist(
        name=novelist.name,
    )
    session.add(db_novelist)
    session.commit()
    session.refresh(db_novelist)

    return db_novelist


@router.get('/', status_code=HTTPStatus.OK, response_model=NovelistList)
def get_all_novelists(session: T_Session, current_user: T_CurrentActiveUser):
    novelists = session.scalars(select(Novelist)).all()
    return {'novelists': novelists}


@router.patch('/{novelist_id}', response_model=NovelistPublic)
def patch_novelist(novelist_id: int, session: T_Session, novelist: NovelistUpdate, current_user: T_CurrentActiveUser):
    db_novelist = session.scalar(select(Novelist).where(Novelist.id == novelist_id))

    if not db_novelist:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Novelist not found.')

    for key, value in novelist.model_dump(exclude_unset=True).items():
        setattr(db_novelist, key, value)

    session.add(db_novelist)
    session.commit()
    session.refresh(db_novelist)

    return db_novelist


@router.get('/{novelist_id}', response_model=NovelistPublic)
def get_novelist(novelist_id: int, session: T_Session, current_user: T_CurrentActiveUser):
    db_novelist = session.scalar(select(Novelist).where(Novelist.id == novelist_id))

    if not db_novelist:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Novelist not found.')

    return db_novelist


@router.delete('/{novelist_id}', response_model=Message)
def delete_novelist(novelist_id: int, session: T_Session, current_user: T_CurrentActiveUser):
    db_novelist = session.scalar(select(Novelist).where(Novelist.id == novelist_id))

    if not db_novelist:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Novelist not found.')

    session.delete(db_novelist)
    session.commit()

    return {'message': 'Novelist has been deleted successfully.'}
